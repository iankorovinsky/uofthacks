import cv2
import streamlit as st
import numpy as np

# Create a Streamlit window
st.title("Real-Time Webcam Feed")

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    st.error("Error: Webcam not found or cannot be accessed.")
else:
    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            st.error("Error: Failed to read a frame from the webcam.")
            break

        # Display the frame in Streamlit
        st.image(frame, channels="BGR", use_column_width=True)

    # Release the webcam and close the Streamlit app when done
    cap.release()