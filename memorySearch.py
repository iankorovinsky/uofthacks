import streamlit as st
import cohere

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('COHERE_API_KEY')

# Initialize Cohere client
co = cohere.Client(api_key)
# Example dictionary mapping descriptions to videos
video_dict = {
    "Ian sleeping on the ground at a hackathon.": "Video 4 URL",
    "William doing karaoke with Ian at Deltahacks": "https://cdn.discordapp.com/attachments/1189032378354651216/1195977651509264425/IMG_7435.mov?ex=65bf2e7c&is=65acb97c&hm=1530129896a85d0c0e69473fa8bc333fa51370a70b22e70a357ae9d0ceaa578a&",
    "William and Ian doing karaoke at a hackathon.": "https://cdn.discordapp.com/attachments/1176251472791478300/1200606493028909217/PXL_20240127_010105877.mp4?ex=65c6caee&is=65b455ee&hm=8e83f1ca999ed2f9af718848b9ed9680edc222a1a66ef3bf0899e69e1fbf2753&",
    "William exploring the Creepy UofT Engineering building with Ian and Lucy": "Video 6 URL",
    "William going to UoftHacks, hackathon with 500+ hackers!": "https://cdn.discordapp.com/attachments/1189032378354651216/1200595671460360222/IMG_8044.mov?ex=65c6c0da&is=65b44bda&hm=0e3011747c6562b1fcc2af8a6f335b73111e5306a07ad078707906e84b367cd6&",
    "William doing karaoke at Hack the Valley": "https://cdn.discordapp.com/attachments/1176251472791478300/1200181987307176097/IMG_4867.mov?ex=65c53f94&is=65b2ca94&hm=5060449bd85e32575c6c01799a0f14d7eaec8fb73c26ec2b2eec734d8f72c746&",
    # Add more descriptions and corresponding video URLs as needed
}

video_descriptions = [key for key in video_dict.keys()]

def rerank_descriptions(prompt, descriptions):
    response = co.rerank(
        query=prompt,
        documents=descriptions,
        top_n=3,  # Fetching top 3 relevant descriptions
        model="rerank-multilingual-v2.0"
    )
    return response

def main():
    st.title("Find Nostalgic Videos")
    
    user_prompt = st.text_input("Enter your nostalgic prompt (e.g., '90s music', 'old cartoons', etc.):")
    if st.button('Find Videos'):
        if user_prompt:
            # Get the top 3 reranked video descriptions
            top_descriptions = rerank_descriptions(user_prompt, video_descriptions)
            st.write("Top 3 Relevant Videos:")
            columns = st.columns(3)

            for i, rerank_result in enumerate(top_descriptions, 1):
                description = rerank_result.document['text']
                relevance_score = rerank_result.relevance_score
                video_url = video_dict.get(description, "Video URL not found")

                # Display the video in a column
                with columns[i - 1]:
                    st.write(f"{i}. Description: {description}")
                    st.write(f"Relevance: {relevance_score}")
                    st.video(video_url)

if __name__ == "__main__":
    main()
