import os
from flask import Flask, request, jsonify
import cohere
from flask_cors import CORS
from dotenv import load_dotenv
import weaviate
import transcription
import recorder as rc
import photo
import requests
import email_send
import asyncio
import nft
import eyes
import json
import webbrowser
import time
import cv2

"""

SETUP

"""

load_dotenv()
COHERE_API_KEY = os.environ['COHERE_API_KEY']
co = cohere.Client(os.environ['COHERE_API_KEY'])
transcription.init()
email_send.init()

client = weaviate.Client(
    url = os.environ['DB_URL'],  
    auth_client_secret=weaviate.AuthApiKey(api_key=os.environ['WEAVIATE_API_KEY']), 
    additional_headers = {
        "X-Cohere-Api-Key": os.environ['COHERE_API_KEY']
    }
)

print("Starting setup...")

app = Flask(__name__)
CORS(app, origins='http://localhost:2000')
co = cohere.Client(os.environ['COHERE_API_KEY'])

API_KEY = os.environ['GEOLOCATION_API_KEY']
GEOLOCATION_URL = f'https://api.ipgeolocation.io/ipgeo?ip=138.51.76.67&apiKey={API_KEY}'

print("Setup initialized")

"""

CORE APIS CALLED BY FRONTEND

"""

#Takes in an image description
#Returns a list of file_names
@app.route('/api/search', methods=["POST", "GET"])
def search():
    imagetext = request.form['imagetext']
    filenames = query(imagetext)
    print(filenames)
    return jsonify({'results': filenames})

#Takes in a timestamp and a person string
#Outputs success JSON
@app.route('/api/upload', methods=["POST", "GET"])
def upload():
    #Step 0: save blob

    # Save the blob as an MP4 file
    blob_data = request.form['blob']
    timestamp = time.time()
    with open(f'media/joint/joint_{timestamp}.mp4', 'wb') as file:
        file.write(blob_data)

    # Save the blob as an MP3 file
    with open(f'media/audio/audio_{timestamp}.wav', 'wb') as file:
        file.write(blob_data)

    # Load the video
    video_capture = cv2.VideoCapture(f'media/joint/joint_{timestamp}.mp4')

    # Read the first frame
    success, frame = video_capture.read()

    if success:
        # Save the first frame as an image
        cv2.imwrite(f'media/photo/photo_{timestamp}.jpg', frame)

    video_capture.release()
    
    #Step 1: get timestamp + people
    filename = f"joint_{timestamp}.mp4"
    person = request.form['person']
    people = []
    people.append(person)
    #Step 2: open image and transcribe
    context = vision(timestamp)
    print("context:")
    print(context)
    #Step 3: transcription
    transcription = transcribe(timestamp)
    print("transcription:")
    print(transcription)
    #step 4: location
    location = get_location()
    print(location)
    #step 5: embed
    print("Adding embedding")
    text = add(filename, transcription, context, person, location)
    print("Added embedding")
    #step 6: nft
    print("Starting NFT")
    name = "Memory with " + person + ", #" + str(timestamp)
    description = context
    imageName = filename
    link = nonfungibletokens(name, description, imageName)
    link = json.loads(link)["transaction_details"]["blockExplorer"]
    print(link)
    print("Ended NFT")

    webbrowser.open_new_tab(link)
    #step 7: append to json
    print("Starting JSON")
    # Load the existing data
    with open('memories.json', 'r') as file:
        data = json.load(file)

    # Append new data
    new_item = {"name": name,
        "transcription": transcription,
        "context": context,
        "people": person,
        "location": location,
        "filename": filename,
        "timestamp": timestamp}
    data['memories'].append(new_item)

    # Save the updated data
    with open('memories.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Ended JSON")


    #step 8: email
    print("Starting email")
    email(people, link)
    print("Ended email")
    return jsonify({'': 'success'})


"""

BACKEND PROCESSES

"""

@app.route('/api/get_location', methods=["POST", "GET"])
def get_location():
    user_ip = "138.51.76.67"  # Get user's IP address
    response = requests.get(GEOLOCATION_URL)
    data = response.json()
    print("----")
    print(data)

    if response.status_code == 200:
        location = data.get('city') + " " + data.get('country_name')
        return location
    else:
        return jsonify({'error': 'Could not get location'}), 500

@app.route('/api/vision', methods=["POST", "GET"])
def vision(timestamp):
    text = eyes.main(timestamp)
    return text
    
@app.route('/api/', methods=["POST", "GET"])
def test():
    return jsonify({'results': 'Reached sample endpoint!'})

@app.route('/api/weaviateinit', methods=["POST", "GET"])
def weaviateinit():    
    video_obj = {
        "class": "Video2",
        "vectorizer": "text2vec-cohere",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        "moduleConfig": {
            "text2vec-cohere": {},
            "generative-cohere": {}  # Ensure the `generative-cohere` module is used for generative queries
        }
    }

    client.schema.create_class(video_obj)
    return jsonify({'status':'success initializing'})


@app.route('/api/add', methods=["POST", "GET"])
def add(filename, transcription, context, people, location):
    client.batch.configure(batch_size=10)
    with client.batch as batch:
        properties = {
            "file_name": filename,
            "transcription": transcription,
            "video_context": context,
            "people": people,
            "location": location
        }
        batch.add_data_object(
            data_object=properties,
            class_name="Video2"
        )
    return jsonify({'results': 'Successfully added new video embedding!'})

@app.route('/api/query', methods=["POST", "GET"])
def query(text):
    query = text
    print(f"Query: {query}")
    response = (
        client.query
        .get("Video2", ["file_name", "transcription", "video_context", "people", "location"])
        .with_near_text({"concepts": [query]})
        .with_limit(3)
        .do()
    )
    print(response)
    responses = response["data"]["Get"]["Video2"]
    urls = []
    for item in responses:
        urls.append(item["file_name"])
    return urls

@app.route('/api/transcribe', methods=["POST", "GET"])
def transcribe(timestamp):
    filepath = f"audio_{timestamp}.wav"
    text = transcription.transcriber(filepath)
    return text

@app.route('/api/recorder', methods=["POST", "GET"])
def recorder():
    timestamp = rc.main()
    photo.get_photo(timestamp)
    return jsonify({'results': timestamp})

@app.route('/api/email', methods=["POST", "GET"])
def email(name, link):
    email_send.email_request(name, link)
    return jsonify({'results': 'success'})

@app.route('/api/nft', methods=["POST", "GET"])
def nonfungibletokens(name, description, imageName):
    text = asyncio.run(nft.mintNFT(name, description, imageName))
    return text

if __name__ == '__main__':
    app.run(debug=True, port=2000)