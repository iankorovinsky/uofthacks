import os
from flask import Flask, request, jsonify
import cohere
from flask_cors import CORS
from dotenv import load_dotenv
import weaviate

load_dotenv()
COHERE_API_KEY = os.environ['COHERE_API_KEY']

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

print("Setup initialized")

@app.route('/api/', methods=["POST", "GET"])
def test():
    return jsonify({'results': 'Reached sample endpoint!'})


@app.route('/api/add', methods=["POST", "GET"])
def add():
    client.batch.configure(batch_size=10)
    print()
    with client.batch as batch:
        properties = {
            "file_name": request.form['File Name'],
            "transcription": request.form['Transcription'],
            "video_context": request.form['Context'],
            "people": request.form['People'],
            "location": request.form['Location']
        }
        batch.add_data_object(
            data_object=properties,
            class_name="Video"
        )
    return jsonify({'results': 'Successfully added new video embedding!'})

@app.route('/api/branch', methods=["POST", "GET"])
def branch():
    query = request.form['query']
    print(f"Query: {query}")
    response = (
        client.query
        .get("Video", ["file_name", "transcription", "video_context", "people", "location"])
        .with_near_text({"concepts": [query]})
        .with_limit(3)
        .do()
    )
    
    responses = response["data"]["Get"]["Video"]
    print(responses)
    return jsonify({'results': responses})


if __name__ == '__main__':
    app.run(debug=True, port=2000)