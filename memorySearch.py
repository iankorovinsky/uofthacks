import streamlit as st
import cohere

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
    "Ian sleeping on the ground at a hackathon.": "https://media.discordapp.net/attachments/1161450447807193091/1200673767542771782/IMG_8059.jpg?ex=65c70995&is=65b49495&hm=42ce11fbddd04798e3a114200b9b9a9424dd8b49f7751aa95499df53eefb2e2f&=&format=webp&width=712&height=948",
    "William doing karaoke with Ian at Deltahacks": "https://cdn.discordapp.com/attachments/1189032378354651216/1195977651509264425/IMG_7435.mov?ex=65bf2e7c&is=65acb97c&hm=1530129896a85d0c0e69473fa8bc333fa51370a70b22e70a357ae9d0ceaa578a&",
    "William and Ian doing karaoke at a hackathon.": "https://cdn.discordapp.com/attachments/1176251472791478300/1200606493028909217/PXL_20240127_010105877.mp4?ex=65c6caee&is=65b455ee&hm=8e83f1ca999ed2f9af718848b9ed9680edc222a1a66ef3bf0899e69e1fbf2753&",
    "Ian passed out at Uofthacks": "https://media.discordapp.net/attachments/1161450447807193091/1200849740103946330/IMG_8066.jpg?ex=65c7ad78&is=65b53878&hm=1824e9129057179a3879b4b4b578727891b148b6b893f097f1ae6c59f53aaf0c&=&format=webp&width=712&height=948",
    "Stephen passed out at uofthacks": "https://media.discordapp.net/attachments/1161450447807193091/1200849741282562128/IMG_8067.jpg?ex=65c7ad79&is=65b53879&hm=820b524d55c38295b0b38f8b341d5b7949699c23366e999655beae63b0eec39d&=&format=webp&width=712&height=948",
    "MYhal 150 at 4am": "https://media.discordapp.net/attachments/1161450447807193091/1200849742008168468/IMG_8069.jpg?ex=65c7ad79&is=65b53879&hm=54287f172d53baad3efd3beaac7312127a685e85d7d8dc7ea820e0fd4d4b7608&=&format=webp&width=1265&height=948",
    "Teddy.ai saying daddy at deltahacks and making the crowd laugh": "https://cdn.discordapp.com/attachments/1161450447807193091/1200673768171901030/IMG_1642.mov?ex=65c70995&is=65b49495&hm=dc4eeab2139b33123cdfad649edee5cb3a2db18e52a51a25db8f08e22e589f92&",
    "UoftHacks found this random party at Skule": "https://cdn.discordapp.com/attachments/1161450447807193091/1200673768633290762/IMG_8053.mov?ex=65c70995&is=65b49495&hm=50b9d58e42f21e4e33a644eb1f4a31405be4e2bcb08bc1d12e49cf8295f51afc&",
    "William going to UoftHacks, hackathon with 500+ hackers!": "https://cdn.discordapp.com/attachments/1189032378354651216/1200595671460360222/IMG_8044.mov?ex=65c6c0da&is=65b44bda&hm=0e3011747c6562b1fcc2af8a6f335b73111e5306a07ad078707906e84b367cd6&",
    "William doing karaoke at Hack the Valley": "https://cdn.discordapp.com/attachments/1176251472791478300/1200181987307176097/IMG_4867.mov?ex=65c53f94&is=65b2ca94&hm=5060449bd85e32575c6c01799a0f14d7eaec8fb73c26ec2b2eec734d8f72c746&",
    "spicy noodle challenge at Deltahacks": "https://media.discordapp.net/attachments/1189032378354651216/1195874662073241682/IMG_7429.jpg?ex=65bece91&is=65ac5991&hm=8ce7cdb1c7cb2e580abdc950836c5e44b2e54a71d5af6da8f0802537cfd5f878&=&format=webp&width=712&height=948",
    # games 
    "Subway surfers": "https://cdn.discordapp.com/attachments/1161450447807193091/1200871868035514468/cutteryt.mp4?ex=65c7c214&is=65b54d14&hm=93df2e0525ff8c8aaaa48852ed473033d16743c9a6f136ae5dc2b9bc1b02b280&",
    "Pokemon Red & Blue": "",
    "Super smash wii": "",

    "Mario Kart Wii": "",
    "Minecraft": "",
    "Windows 7": "",
    "Windows XP": "",

    # william nostalgia
    "juice": "https://lh3.googleusercontent.com/pw/ABLVV85848VP21JSbNvLzP93ere8zA2x5fLNal9JBdg__zz6xLItmBg0OS_1CjqlJCxhVN7Cyp84i-JikRWeTfhBy2DupnLMfcxXmX6A4fR6Xo12yD665IE7vWEuSszlpgo4JJJfoOSejVRmMdKaT_2Z_nmEq-Z9OXr7F_FFNkcYqCMmkPoVFSoYLyDxF25wf_HcbuDq54_VLGKOMVtbqTuwe3ZmWsf_laN-acxKs3R98y8qGEzQBgNK0LQXgt0TnVPvwXTvq36-N8vmbGPhzDfpbNb1GbRbkFqb8rCVaB5FwoA4_UkARPp6ku7ZH9tWwp5BgP_WaY28yed27UfGSYUs0vP38cX7p8cLWaoRQJg4qNz8-VoQXnxmrzYXzzR79hcd0oPbl6FllkrPo2TIeW4u0Cf8OBuUKL4_FU5RSfQ7_dU8hJT71umQt2Iat14lrE5kzBQz5gDs0jesvzmh-zgOckl3YAwu9431gqoSr-fO8ld1MxUSkX9nD-5ah8kn42UfpelcHeDUFjRgI67Yzzwdh5_X_Gv_EUU6g7jh3NEeuDDr1Az4p8IYKO-SPMQkPAuhMeOd59AvN57nncFa-iO6P1p9foXn5IQNlzJlXcZdQzMrONoZQJpuYa5B3E3PljHz0HirKDYbqbHpszQRQSeHBJk-F2vgmwLcGYL2-P4gqGt7ub_EwMfUrtm9IjN1QHBgCP9W5WPY70-aS6uHABI6ggUf89QY87V78J8F3ln3zH3Ke3-gvfSGb6wa5u2jC6EDzUSyKa9rBd9AAoHEIOspxOppofmllDOh6o7lxlFRKBBk4QMk5FiV6ZGwdidOG0rGsLelUGOvPqfCCy3uEhLa7BQFBbh6pm5EiY82ULwhfykPmy4VXJ0ZLFxRzrFvgwkyclti9AcipsiDGOhEZCwCSPGvJd0j56eZa2KaAsSby3giy8RpXZiTwaADJF3c3usY-ri9WUT72KRuXMV-gsZo4nTGOpO_b9r8-Dx_Az9gTxn2xKapcFdFgGs--mucS68jTvK6vKmXXecBpdQiF43kU1E44hAMjpsomdeSp7JtKpcYG_7jI1VlUZ3SHdO1uDIJnOrl-mRJZS5nU-zupD6Ols4OV6VXNK0g1vgeJvNUdEE=w804-h1430-s-no-gm?authuser=2",
    "teddy bear hackathon": "https://media.discordapp.net/attachments/1195521115926302771/1196488559801139281/IMG_7464.jpg?ex=65c10a4e&is=65ae954e&hm=8060ecec870d0b7acaefc9d158005d7fe28088dd81912fa612d882b866baedb7&=&format=webp&width=1265&height=948",
    "Alina hugging teddy bear": "https://lh3.googleusercontent.com/pw/ABLVV87nSyHfokDbc-02ou_ZCIiKxw1JssCcobTxszlCeKfDyxVjxjlcamQ8PTAS9j4Ui3qpGQIBZMoXvS42jRAtc_WfAO9jhFVwNDGcpYInIu8Uj1vd64SMMw1X701uYvd3_3DYNyfoKsttzH5G1wLCeV407_RlNUdk9pHaY-Eaq4E5Tx4jnhr0ojZMp1MPl5dmlCbK82rRa-xHYDoGaYM71hOSpoJXNoznQ3jpC48q1FBtL2vzEgJVE7SNLoHzAruUOFjX5-bC7FXoBB02H60IZ-VZkQWi_TjaaOq5EalMFeRqsqN2xUnBDQVF-BOleUFOxUg_EEWIHVEgBik7NjlQyIsjM8NQ5Ng2aWiED0OOx4__m-nA7gQwYfhgdtCPozoNB1Cav95wJTPHsHFOXTu3n0i_MNfpdh_2-88l4YTcl8Nq9P2lZp53dL94VvMryg8KKAiyXoAoOZ5azKvRW8xA-OLrqPIPgXWHDO1N6q38JkzZ-ershGdPmuBjBlE6r6ghKAqp7M4dO9lxk5OEHNx2LDVNOyEMhz1HYVEwZYFkk4DYghnoKWuI7MbRajCk9yhgMa_63uvJJCcblaPxTFmtFzcEhA2HHD9bXWKOJTPRmbzeqAM6df_DqA1VLfbGiXXVdlj3x8IP693fA8KntWjo7RJRE_oCNs9ceAg9Ga32cUmaYTb4NXcpKn-xQIml8uPjh2U1zXMQ0b2jKbR1jrB-fcjnYatf9xJDVVzoOJ4F4eIxQagHL09eUqPHNXn2FLNd_gMh90EG29khpr7g7RnhaxkoDYfKHIeUesTqOsBVN-KMo1ipI0Ct43P1TIdgwaoBtrjUQnkpg878nhfNzIt2APAgyPRXaG1EjhppucwdxRkKn5WmJAzi8y137Jun-dNbfjLLM-uKSfc4bjZyQWFp2tvlzXxwSO-TqKNQVcbZtHO4zEHEs3_i9aWnmpk7fER5murvMHsiFEzjiN1Uw5PDAYaWqvVzkSEGQmI-104klbd9-_SnqK72CWMCC3zVY6tOBtF6g_b3Vl5t4n_F4QYbW8jrbPa4tHKTlrdHUYFd76GtwJ8e25LN2fPEzsRmO8wi-g0IeuMRZF2xFu_-dcHlU6z_q9F_os8rId6ltdwxhX4G=w1080-h1430-s-no-gm?authuser=2",

    # Add more descriptions and corresponding video URLs as needed
    "Animal Jam": "https://cdn.discordapp.com/attachments/1155327631361835119/1200878781242540083/Epic_trading_party_Animal_jam.mp4?ex=65c7c884&is=65b55384&hm=2ab843be6ec16411a876ed7aa938f4767ea6b4519b39db56be70976544f1df67&",
    "Pokemon Red & Blue": "https://cdn.discordapp.com/attachments/1155327631361835119/1200880623456358543/Pokemon_Red_for_Game_Boy_HD_Full_Playthrough.mp4?ex=65c7ca3b&is=65b5553b&hm=8b1c6759debf7aff0c1a9765851dec2dba0ed9081ca33bca3cfcf33a14422b74&",
    "Super smash wii": "https://cdn.discordapp.com/attachments/807724582705954857/1200881519611363359/Super_Smash_Bros_Brawl_Gameplay_Wii.mp4?ex=65c7cb11&is=65b55611&hm=e02f6499f4a0841fd63f11b1f3590fe5ab5d755be4789b1f2543ac2992ae297a&",
    "Mario Kart Wii": "https://cdn.discordapp.com/attachments/807724582705954857/1200882080368840764/Mario_Kart_Wii_-_Longplay_Wii.mp4?ex=65c7cb97&is=65b55697&hm=dc058c7f2666e5a569075c89702134307dcf1e2e83b72e84d76666d79f33d0b2&",
    "Minecraft": "https://cdn.discordapp.com/attachments/807724582705954857/1200882607303442462/Minecraft_DR_TRAYAURUS_COFFEE_SHOP_Custom_Mod_Adventure.mp4?ex=65c7cc14&is=65b55714&hm=2e9e30722091b3c006eb5a603563ffb4855833614b122da1d7b52346404e85b7&",
    "club penguin game holiday party 2010 walkthrough": "https://discord.com/channels/@me/1155327631361835119/1200873151018565773",
    "Movie Star Planet": "https://cdn.discordapp.com/attachments/807724582705954857/1200884797799677952/MSP_-_VIP_.mp4?ex=65c7ce1f&is=65b5591f&hm=c0cb862a515e91b1be235ccf5b6eb6a7a666b1a1ee066ae854e4691eb3e073d0&",
    "Fantage": "https://cdn.discordapp.com/attachments/807724582705954857/1200885273005916250/Fantage_Fashon_Show.mp4?ex=65c7ce90&is=65b55990&hm=edb19938412399091f0bff69179bcf5967f6a5c8b69e64dc1891765e9240bd04&",

    # music
    "Spice Girls Wannabe 90s throwback music": "https://www.youtube.com/watch?v=gJLIiF15wjQ&ab_channel=SpiceGirlsVEVO",
    "Everyime We Touch Cascada 2000s music": "https://cdn.discordapp.com/attachments/807724582705954857/1200892200414883983/Cascada_-_Everytime_We_Touch_Official_video.mp4?ex=65c7d504&is=65b56004&hm=e2cf40d6d86d4ff148d1cf9f410acf67fb6ceb355af4265697368be0d1a42d95&",
    "Britney Spears - Sometimes": "https://cdn.discordapp.com/attachments/807724582705954857/1200894113504038953/Britney_Spears_-_Sometimes_Official_HD_Video.mp4?ex=65c7d6cc&is=65b561cc&hm=6b0fbbf8b0a626b2765838fdeb33b3f90b9a917716ac0cbf60a14081e6fe55f3&",
    "90s throwback Mariah Carey, Boyz II Men - One Sweet Day": "https://cdn.discordapp.com/attachments/807724582705954857/1200893579296510053/Mariah_Carey_Boyz_II_Men_-_One_Sweet_Day_Official_Video.mp4?ex=65c7d64c&is=65b5614c&hm=9414e5b45a7e40b4e7dd14de65c48009ea32cd56e4f3245e90bd70dbcfc8d169&",


    "Windows 7": "https://cdn.discordapp.com/attachments/807724582705954857/1200883155951943721/R.I.P_Windows_7.mp4?ex=65c7cc97&is=65b55797&hm=63d45fc211d26f71d75a376a924e4eeb1a5c02867cecfdff25f46a972064d1c5&",
    "Windows XP": "https://cdn.discordapp.com/attachments/807724582705954857/1200883802302591096/it_s_2005_you_Startup_a_Windows_XP_professional.mp4?ex=65c7cd31&is=65b55831&hm=49cdd6043025ca32c97e14c3b4279e95f5564df7e16f36aa71485a982fcd52a5&",

    # plushies
    "Lucy got her first large squishmellow!": "https://media.discordapp.net/attachments/807724582705954857/1200886252363337738/IMG_0967_Original.jpg?ex=65c7cf79&is=65b55a79&hm=878039b5949b2678415c0b23a88a64fc0f456b453ca28b8febbe075cf7d4a5da&=&format=webp&width=1712&height=1284",
    "Family trip to China (got a baymax plush!)": "https://media.discordapp.net/attachments/807724582705954857/1200886253554520186/IMG_4718_Original.jpg?ex=65c7cf7a&is=65b55a7a&hm=e5b1658d91375a085a6ce42d1bb5e9170fb12ed2623b3f58447e61ff45f47a98&=&format=webp&width=1424&height=1284",
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
        model="rerank-multilingual-v2.0"
    )
    return response

# Function to generate chat response using Cohere
def generate_chat_response(message, documents):
    response = co.chat(model="command", message=message, documents=documents)
    return response.text



# Initialize a Python variable to store the text value
text_value = "..."



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
                    if ".mov" in video_url or ".mp4" in video_url:
                        st.video(video_url)  # Display the video

                    # Check if video_url contains ".jpg"
                    elif ".jpg" in video_url:
                        st.image(video_url)  # Display the image

                    else:
                        st.write("File retrieval error.")

    # User input
    user_message = st.sidebar.text_input("Chat with your memories: ")

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


if __name__ == "__main__":
    main()
