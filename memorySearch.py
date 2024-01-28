import io
import requests
import streamlit as st
import cohere
import cv2
import streamlit as st
import requests
import base64
import os
from dotenv import load_dotenv
from cohere.responses.chat import StreamEvent

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('COHERE_API_KEY')

# Initialize Cohere client
co = cohere.Client(api_key)
# Example dictionary mapping descriptions to videos
video_dict = {
    "Ian sleeping on the ground at a hackathon, lying on the floor of the auditorium.": "https://media.discordapp.net/attachments/1161450447807193091/1200673767542771782/IMG_8059.jpg?ex=65c70995&is=65b49495&hm=42ce11fbddd04798e3a114200b9b9a9424dd8b49f7751aa95499df53eefb2e2f&=&format=webp&width=712&height=948",
    "William doing karaoke with Ian at Deltahacks": "https://cdn.discordapp.com/attachments/1189032378354651216/1195977651509264425/IMG_7435.mov?ex=65bf2e7c&is=65acb97c&hm=1530129896a85d0c0e69473fa8bc333fa51370a70b22e70a357ae9d0ceaa578a&",
    "William and Ian doing karaoke at a hackathon.": "https://cdn.discordapp.com/attachments/1176251472791478300/1200606493028909217/PXL_20240127_010105877.mp4?ex=65c6caee&is=65b455ee&hm=8e83f1ca999ed2f9af718848b9ed9680edc222a1a66ef3bf0899e69e1fbf2753&",
    "Ian passed out at Uofthacks. sleeping on the ground at a hackathon, lying on the floor of the auditorium.": "https://media.discordapp.net/attachments/1161450447807193091/1200849740103946330/IMG_8066.jpg?ex=65c7ad78&is=65b53878&hm=1824e9129057179a3879b4b4b578727891b148b6b893f097f1ae6c59f53aaf0c&=&format=webp&width=712&height=948",
    "Stephen passed out at uofthacks. sleeping on the ground at a hackathon, lying on the floor of the auditorium.": "https://media.discordapp.net/attachments/1161450447807193091/1200849741282562128/IMG_8067.jpg?ex=65c7ad79&is=65b53879&hm=820b524d55c38295b0b38f8b341d5b7949699c23366e999655beae63b0eec39d&=&format=webp&width=712&height=948",
    "MYhal 150 at 4am": "https://media.discordapp.net/attachments/1161450447807193091/1200849742008168468/IMG_8069.jpg?ex=65c7ad79&is=65b53879&hm=54287f172d53baad3efd3beaac7312127a685e85d7d8dc7ea820e0fd4d4b7608&=&format=webp&width=1265&height=948",
    "Teddy.ai saying daddy at deltahacks and making the crowd laugh": "https://cdn.discordapp.com/attachments/1161450447807193091/1200673768171901030/IMG_1642.mov?ex=65c70995&is=65b49495&hm=dc4eeab2139b33123cdfad649edee5cb3a2db18e52a51a25db8f08e22e589f92&",
    "UoftHacks found this random party at Skule": "https://cdn.discordapp.com/attachments/1161450447807193091/1200673768633290762/IMG_8053.mov?ex=65c70995&is=65b49495&hm=50b9d58e42f21e4e33a644eb1f4a31405be4e2bcb08bc1d12e49cf8295f51afc&",
    "William going to UoftHacks, hackathon with 500+ hackers!": "https://cdn.discordapp.com/attachments/1189032378354651216/1200595671460360222/IMG_8044.mov?ex=65c6c0da&is=65b44bda&hm=0e3011747c6562b1fcc2af8a6f335b73111e5306a07ad078707906e84b367cd6&",
    "William doing karaoke at Hack the Valley": "https://cdn.discordapp.com/attachments/1176251472791478300/1200181987307176097/IMG_4867.mov?ex=65c53f94&is=65b2ca94&hm=5060449bd85e32575c6c01799a0f14d7eaec8fb73c26ec2b2eec734d8f72c746&",
    "spicy noodle challenge at Deltahacks": "https://media.discordapp.net/attachments/1189032378354651216/1195874662073241682/IMG_7429.jpg?ex=65bece91&is=65ac5991&hm=8ce7cdb1c7cb2e580abdc950836c5e44b2e54a71d5af6da8f0802537cfd5f878&=&format=webp&width=712&height=948",
    
    # games 
    "Subway surfers": "https://cdn.discordapp.com/attachments/1161450447807193091/1200871868035514468/cutteryt.mp4?ex=65c7c214&is=65b54d14&hm=93df2e0525ff8c8aaaa48852ed473033d16743c9a6f136ae5dc2b9bc1b02b280&",
    "Animal Jam": "https://cdn.discordapp.com/attachments/1155327631361835119/1200878781242540083/Epic_trading_party_Animal_jam.mp4?ex=65c7c884&is=65b55384&hm=2ab843be6ec16411a876ed7aa938f4767ea6b4519b39db56be70976544f1df67&",
    "Pokemon Red & Blue": "https://cdn.discordapp.com/attachments/1155327631361835119/1200880623456358543/Pokemon_Red_for_Game_Boy_HD_Full_Playthrough.mp4?ex=65c7ca3b&is=65b5553b&hm=8b1c6759debf7aff0c1a9765851dec2dba0ed9081ca33bca3cfcf33a14422b74&",
    "Super smash wii": "https://cdn.discordapp.com/attachments/807724582705954857/1200881519611363359/Super_Smash_Bros_Brawl_Gameplay_Wii.mp4?ex=65c7cb11&is=65b55611&hm=e02f6499f4a0841fd63f11b1f3590fe5ab5d755be4789b1f2543ac2992ae297a&",
    "Mario Kart Wii": "https://cdn.discordapp.com/attachments/807724582705954857/1200882080368840764/Mario_Kart_Wii_-_Longplay_Wii.mp4?ex=65c7cb97&is=65b55697&hm=dc058c7f2666e5a569075c89702134307dcf1e2e83b72e84d76666d79f33d0b2&",
    "Minecraft": "https://cdn.discordapp.com/attachments/807724582705954857/1200882607303442462/Minecraft_DR_TRAYAURUS_COFFEE_SHOP_Custom_Mod_Adventure.mp4?ex=65c7cc14&is=65b55714&hm=2e9e30722091b3c006eb5a603563ffb4855833614b122da1d7b52346404e85b7&",
    
    # william nostalgia
    "juice": "https://lh3.googleusercontent.com/pw/ABLVV85848VP21JSbNvLzP93ere8zA2x5fLNal9JBdg__zz6xLItmBg0OS_1CjqlJCxhVN7Cyp84i-JikRWeTfhBy2DupnLMfcxXmX6A4fR6Xo12yD665IE7vWEuSszlpgo4JJJfoOSejVRmMdKaT_2Z_nmEq-Z9OXr7F_FFNkcYqCMmkPoVFSoYLyDxF25wf_HcbuDq54_VLGKOMVtbqTuwe3ZmWsf_laN-acxKs3R98y8qGEzQBgNK0LQXgt0TnVPvwXTvq36-N8vmbGPhzDfpbNb1GbRbkFqb8rCVaB5FwoA4_UkARPp6ku7ZH9tWwp5BgP_WaY28yed27UfGSYUs0vP38cX7p8cLWaoRQJg4qNz8-VoQXnxmrzYXzzR79hcd0oPbl6FllkrPo2TIeW4u0Cf8OBuUKL4_FU5RSfQ7_dU8hJT71umQt2Iat14lrE5kzBQz5gDs0jesvzmh-zgOckl3YAwu9431gqoSr-fO8ld1MxUSkX9nD-5ah8kn42UfpelcHeDUFjRgI67Yzzwdh5_X_Gv_EUU6g7jh3NEeuDDr1Az4p8IYKO-SPMQkPAuhMeOd59AvN57nncFa-iO6P1p9foXn5IQNlzJlXcZdQzMrONoZQJpuYa5B3E3PljHz0HirKDYbqbHpszQRQSeHBJk-F2vgmwLcGYL2-P4gqGt7ub_EwMfUrtm9IjN1QHBgCP9W5WPY70-aS6uHABI6ggUf89QY87V78J8F3ln3zH3Ke3-gvfSGb6wa5u2jC6EDzUSyKa9rBd9AAoHEIOspxOppofmllDOh6o7lxlFRKBBk4QMk5FiV6ZGwdidOG0rGsLelUGOvPqfCCy3uEhLa7BQFBbh6pm5EiY82ULwhfykPmy4VXJ0ZLFxRzrFvgwkyclti9AcipsiDGOhEZCwCSPGvJd0j56eZa2KaAsSby3giy8RpXZiTwaADJF3c3usY-ri9WUT72KRuXMV-gsZo4nTGOpO_b9r8-Dx_Az9gTxn2xKapcFdFgGs--mucS68jTvK6vKmXXecBpdQiF43kU1E44hAMjpsomdeSp7JtKpcYG_7jI1VlUZ3SHdO1uDIJnOrl-mRJZS5nU-zupD6Ols4OV6VXNK0g1vgeJvNUdEE=w804-h1430-s-no-gm?authuser=2",
    "teddy bear hackathon. cute teddy bear": "https://media.discordapp.net/attachments/1195521115926302771/1196488559801139281/IMG_7464.jpg?ex=65c10a4e&is=65ae954e&hm=8060ecec870d0b7acaefc9d158005d7fe28088dd81912fa612d882b866baedb7&=&format=webp&width=1265&height=948",
 
    # Add more descriptions and corresponding video URLs as needed
    "club penguin game holiday party 2010 walkthrough": "https://discord.com/channels/@me/1155327631361835119/1200873151018565773",
    "Movie Star Planet": "https://cdn.discordapp.com/attachments/807724582705954857/1200884797799677952/MSP_-_VIP_.mp4?ex=65c7ce1f&is=65b5591f&hm=c0cb862a515e91b1be235ccf5b6eb6a7a666b1a1ee066ae854e4691eb3e073d0&",
    "Fantage": "https://cdn.discordapp.com/attachments/807724582705954857/1200885273005916250/Fantage_Fashon_Show.mp4?ex=65c7ce90&is=65b55990&hm=edb19938412399091f0bff69179bcf5967f6a5c8b69e64dc1891765e9240bd04&",

    # cartoons
    "Caillou theme song": "https://cdn.discordapp.com/attachments/807724582705954857/1200898043873087508/Caillou_Theme_Song.mp4?ex=65c7da75&is=65b56575&hm=78b21def6969bad7444f2fdf0613afffbb6a0574024409c8ae202c30faccbfc6&",
    "Powerpuff Girls": "https://cdn.discordapp.com/attachments/807724582705954857/1200898924307824790/The_Powerpuff_Girls_Theme_Song_Cartoon_Network.mp4?ex=65c7db47&is=65b56647&hm=9949da7be6969f257f1bdea9412e7ac15858194363da2f55b7fb610520fb7c8d&",
    "Tom and Jerry": "https://cdn.discordapp.com/attachments/807724582705954857/1200898044506411161/Tom_Jerry_in_italiano_Un_po_di_aria_fresca_WB_Kids.mp4?ex=65c7da75&is=65b56575&hm=ee40c2d65aaa65848a0ce319f8d1c6249bacec5a59823611703974c5c56fcd68&",

    # nostaglic anime

    # music
    "Spice Girls Wannabe 90s throwback music": "https://cdn.discordapp.com/attachments/807724582705954857/1200890907076083792/Spice_Girls_-_Wannabe_Official_Music_Video.mp4?ex=65c7d3cf&is=65b55ecf&hm=c1598eaa291f4e42cc5d25d96f961a77f9e579b266921ac2b80d82d2511db7e4&",
    "Everyime We Touch Cascada 2000s music": "https://cdn.discordapp.com/attachments/807724582705954857/1200892200414883983/Cascada_-_Everytime_We_Touch_Official_video.mp4?ex=65c7d504&is=65b56004&hm=e2cf40d6d86d4ff148d1cf9f410acf67fb6ceb355af4265697368be0d1a42d95&",
    "Britney Spears - Sometime 90s throwback": "https://cdn.discordapp.com/attachments/807724582705954857/1200894113504038953/Britney_Spears_-_Sometimes_Official_HD_Video.mp4?ex=65c7d6cc&is=65b561cc&hm=6b0fbbf8b0a626b2765838fdeb33b3f90b9a917716ac0cbf60a14081e6fe55f3&",
    "90s throwback Mariah Carey, Boyz II Men - One Sweet Day 90s throwback": "https://cdn.discordapp.com/attachments/807724582705954857/1200893579296510053/Mariah_Carey_Boyz_II_Men_-_One_Sweet_Day_Official_Video.mp4?ex=65c7d64c&is=65b5614c&hm=9414e5b45a7e40b4e7dd14de65c48009ea32cd56e4f3245e90bd70dbcfc8d169&",

    "Windows 7": "https://cdn.discordapp.com/attachments/807724582705954857/1200883155951943721/R.I.P_Windows_7.mp4?ex=65c7cc97&is=65b55797&hm=63d45fc211d26f71d75a376a924e4eeb1a5c02867cecfdff25f46a972064d1c5&",
    "Windows XP": "https://cdn.discordapp.com/attachments/807724582705954857/1200883802302591096/it_s_2005_you_Startup_a_Windows_XP_professional.mp4?ex=65c7cd31&is=65b55831&hm=49cdd6043025ca32c97e14c3b4279e95f5564df7e16f36aa71485a982fcd52a5&",

    # plushies
    "Lucy got her first large squishmellow! Very cute plushie teddy bear.": "https://media.discordapp.net/attachments/807724582705954857/1200886252363337738/IMG_0967_Original.jpg?ex=65c7cf79&is=65b55a79&hm=878039b5949b2678415c0b23a88a64fc0f456b453ca28b8febbe075cf7d4a5da&=&format=webp&width=1712&height=1284",
    "Family trip to China (got a baymax plush!) Cute teddy": "https://media.discordapp.net/attachments/807724582705954857/1200886253554520186/IMG_4718_Original.jpg?ex=65c7cf7a&is=65b55a7a&hm=e5b1658d91375a085a6ce42d1bb5e9170fb12ed2623b3f58447e61ff45f47a98&=&format=webp&width=1424&height=1284",
    "Teddy bear plushie photo shoot": "https://media.discordapp.net/attachments/807724582705954857/1200886254003302600/IMG_0124_Original.jpg?ex=65c7cf7a&is=65b55a7a&hm=9fd110faebfa11bfa1cf6cba5033d321664c5eb1d90c686fac74dddededc1c41&=&format=webp&width=1712&height=1284",
    "Stuffed animals from Secret Santa": "https://media.discordapp.net/attachments/807724582705954857/1200888331869892618/IMG_3648_Original.jpg?ex=65c7d169&is=65b55c69&hm=cbbf07393b386533119394fe142bd5ef1299654fe50aa0b6c19c142b3a5d48cb&=&format=webp&width=962&height=1282",
    # Add more descriptions and corresponding video URLs as needed
    "3 y.o. Lucy at Tiananmen Square with dog plush": "https://media.discordapp.net/attachments/807724582705954857/1200886254435303434/IMG_1086_Original.jpg?ex=65c7cf7a&is=65b55a7a&hm=657819b3638ecb83127d5a195d8060227c132e9e8c84ad32aa5b46b8966a052c&=&format=webp&width=1712&height=1284",
}

# Convert video_dict to the desired format
memory_documents = [{"description": desc, "url": url} for desc, url in video_dict.items()]

video_descriptions = [key for key in video_dict.keys()]

def rerank_descriptions(prompt, descriptions):
    response = co.rerank(
        query=prompt,
        documents=descriptions,
        top_n=3,  # Fetching top 3 relevant descriptions
        model="rerank-english-v2.0"
    )
    return response

# Function to generate chat response using Cohere
def generate_chat_response(message, documents):
    response = co.chat(model="command", message=message, documents=documents)
    return response.text

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
                        "text": "Write a short concise description of what is in this image?"
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
        "max_tokens": 50
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json()

# Initialize a Python variable to store the text value
text_value = "..."

# Function to encode an image as base64
def encode_image_webcam(image):
    image_pil = Image.fromarray(image)
    buffered = io.BytesIO()
    image_pil.save(buffered, format="JPEG")  # You can choose a different format if needed
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def main():
    st.title("Nostalg.ai")
    
    

    # User input
    user_message = st.sidebar.text_input("Chat with your memories: ")

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        st.error("Error: Webcam not found or cannot be accessed.")
    else:
        if st.button("Take Image"):
            camera_port = 0 
            ramp_frames = 30 
            camera = cap
            retval, im = camera.read()
            for i in range(ramp_frames):
                temp = camera.read()
            # Read a frame from the webcam
            ret, frame = cap.read()

            # Check if the frame was read successfully
            if not ret:
                st.error("Error: Failed to read a frame from the webcam.")

            # Convert the frame from BGR to RGB color channel order
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Display the frame in Streamlit with the RGB color channel order
            st.image(frame_rgb, channels="RGB", use_column_width=True)

            uploaded_file = frame_rgb

            if uploaded_file is not None:
                # Display the image
                st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
                st.write("")

                # Encode the image and get the description
                base64_image = encode_image_webcam(uploaded_file)
                description_response = get_image_description(base64_image)

                # Display the response
                st.write("Description of the image:")
                # st.json(description_response)

                user_prompt = description_response["choices"][0]["message"]["content"]
                st.write(user_prompt)

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
                            if ".mov" in video_url or ".mp4" in video_url:
                                st.video(video_url)  # Display the video

                            # Check if video_url contains ".jpg"
                            elif ".jpg" in video_url:
                                st.image(video_url)  # Display the image

                            else:
                                st.write("File retrieval error.")

        # Release the webcam and close the Streamlit app when done
        cap.release()
    
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
        # st.json(description_response)

        user_prompt = description_response["choices"][0]["message"]["content"]
        st.write(user_prompt)

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
                    if ".mov" in video_url or ".mp4" in video_url:
                        st.video(video_url)  # Display the video

                    # Check if video_url contains ".jpg"
                    elif ".jpg" in video_url:
                        st.image(video_url)  # Display the image

                    else:
                        st.write("File retrieval error.")

    # Chat history
    chat_history = []

    if st.sidebar.button("Send"):
        if user_message:
            # Add user message to chat history
            chat_history.append({"role": "user", "message": user_message})

            # Initialize a Streamlit text element
            text_element = st.sidebar.empty()
            text_element.text("Searching...")

            response = ""

            for event in co.chat(model="command", message=user_message, stream=True, documents=memory_documents, prompt_truncation="AUTO"):
                if event.event_type == StreamEvent.TEXT_GENERATION:
                    response += event.text
                    text_element.text(response)
                elif event.event_type == StreamEvent.CITATION_GENERATION:
                    print(event.citations)
                elif event.event_type == StreamEvent.STREAM_END:
                    print(event.finish_reason)

            # Generate a chatbot response
            # response_message = generate_chat_response(user_message, memory_documents)

            # Add chatbot response to chat history
            chat_history.append({"role": "chatbot", "message": response})

    user_prompt = st.text_input("Enter your nostalgic prompt (e.g., 'plushies', 'karaoke', 'hackathons', 'sleeping'):")
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
                    if ".mov" in video_url or ".mp4" in video_url:
                        st.video(video_url)  # Display the video

                    # Check if video_url contains ".jpg"
                    elif ".jpg" in video_url:
                        st.image(video_url)  # Display the image

                    else:
                        st.write("File retrieval error.")


if __name__ == "__main__":
    main()
