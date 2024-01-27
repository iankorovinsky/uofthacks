import streamlit as st
import cohere

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('COHERE_API_KEY')

# Initialize Cohere client
co = cohere.Client(api_key)

# Example list of video descriptions
video_descriptions = [
    "A nostalgic tour of 90s video games and consoles.",
    "Compilation of classic TV show intros from the 80s.",
    "Documentary about the evolution of mobile phones.",
    "Ian sleeping on the ground at a hackathon.",
    "William and Ian doing karaoke at a hackathon.",
    "William exploring the Creepy UofT Engineering building with Ian and Lucy",
    "William going to a haunted house at Canada's Wonderland.",
    "William doing karaoke with Xavier at UW",
    "William and Ian coding for 24h at deltahacks to win $800 in FLOW tokens",
    # ... add more descriptions as needed ...
]

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
            top_videos = rerank_descriptions(user_prompt, video_descriptions)
            print(top_videos)
            st.write("Top 3 Relevant Videos:")
            for i, video in enumerate(top_videos, 1):
                st.write(f"{i}. {video}")
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()
