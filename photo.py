import cv2

def get_photo(timestamp):
    # Load the video file
    video_path = f'media/joint/joint_{timestamp}.avi'  # Replace with your .avi file path
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
    else:
        # Get the total number of frames in the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Calculate the frame number for the middle frame
        middle_frame_number = total_frames // 2

        # Set the current frame position to the middle frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_number)

        # Read the middle frame
        ret, frame = cap.read()

        if ret:
            # Save the middle frame as an image
            cv2.imwrite(f'media/photo/photo_{timestamp}.jpg', frame)
            print("Middle frame saved as .jpg.")
        else:
            print("Error: Could not read the middle frame.")

        # Release the video capture object
        cap.release()
