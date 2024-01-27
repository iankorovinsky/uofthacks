import streamlit as st
import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

# Function to encode the uploaded image
def encode_image(uploaded_file):
    # Convert the file to bytes and encode it in base64
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# Function to get the image description from OpenAI's API
def get_image_description(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def main():
    st.title("Image Description using GPT-4 Vision")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the image
        st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
        st.write("")

        # Encode the image and get the description
        base64_image = encode_image(uploaded_file)
        description_response = get_image_description(base64_image)

        # Display the response
        st.write("Description of the image:")
        st.json(description_response)

if __name__ == "__main__":
    main()
