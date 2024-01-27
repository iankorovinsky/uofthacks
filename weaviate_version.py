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
CORS(app, origins='http://localhost:3000')
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
    #Step 1: get timestamp + people
    timestamp = request.form['timestamp']
    person = request.form['person']
    people = []
    people.append(person)
    #Step 2: open image and transcribe
    image_text = vision(timestamp)
    #Step 3: transcription
    audio_text = transcribe(timestamp)
    #step 4: location
    location = 
    #step 5: embed
    
    #step 6: nft
    #step 7: append to json
    #step 8: email
    return jsonify({'results': 'success'})


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
        return jsonify({
            'ip': user_ip,
            'country': data.get('country_name'),
            'state': data.get('state_prov'),
            'city': data.get('city'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'organization': data.get('organization')
        })
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
def add():
    client.batch.configure(batch_size=10)
    with client.batch as batch:
        properties = {
            "file_name": request.form['filename'],
            "transcription": request.form['transcription'],
            "video_context": request.form['context'],
            "people": request.form['people'],
            "location": request.form['location']
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
def email():
    email_send.email_request(request.form['names'], request.form['link'])
    return jsonify({'results': 'success'})

@app.route('/api/nft', methods=["POST", "GET"])
def nonfungibletokens():
    text = nft.mintNFT(request.form['name'], request.form['description'], request.form['imageUrl'])
    return jsonify({'results': text})

if __name__ == '__main__':
    app.run(debug=True, port=2000)