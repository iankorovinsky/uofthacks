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
    "A nostalgic tour of 90s video games and consoles.": "Video 1 URL",
    "Compilation of classic TV show intros from the 80s.": "Video 2 URL",
    "Documentary about the evolution of mobile phones.": "Video 3 URL",
    "Ian sleeping on the ground at a hackathon.": "Video 4 URL",
    "William and Ian doing karaoke at a hackathon.": "Video 5 URL",
    "William exploring the Creepy UofT Engineering building with Ian and Lucy": "Video 6 URL",
    "William going to a haunted house at Canada's Wonderland.": "Video 7 URL",
    "William doing karaoke with Xavier at UW": "Video 8 URL",
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
            for i, rerank_result in enumerate(top_descriptions, 1): 
                # Accessing attributes
                description = rerank_result.document['text']  # Get the text attribute
                index = rerank_result.index  # Get the index attribute
                relevance_score = rerank_result.relevance_score  # Get the relevance_score attribute

                video_url = video_dict.get(description, "Video URL not found")  # Get the corresponding video URL
                st.write(f"{i}. Description: {description}")
                st.write(f"Relevance: {relevance_score}. Video URL: {video_url}")
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()
