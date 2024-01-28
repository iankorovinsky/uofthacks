import sounddevice as sd
import soundfile as sf
import keyboard
import queue
import threading
import time
import cv2
from moviepy.editor import *

# Parameters for audio recording
samplerate = 44100  # Sample rate in Hertz
channels = 2        # Number of audio channels
timestamp = time.time()
audio_filename = f'media/audio/audio_{timestamp}.wav'  # Filename to save the audio

# Parameters for video recording
video_filename = f'media/video/video_{timestamp}.avi'  # Filename to save the video

# Create a queue to hold the audio data
q = queue.Queue()

# Flag to control recording state
recording = True

def audio_callback(indata, frames, time, status):
    """Callback function for audio recording."""
    if status:
        print(status)
    q.put(indata.copy())

def record_audio():
    """Function to record audio."""
    global recording
    try:
        with sd.InputStream(samplerate=samplerate, channels=channels, callback=audio_callback):
            with sf.SoundFile(audio_filename, mode='x', samplerate=samplerate, channels=channels) as file:
                print('Recording audio... Press "q" to stop.')
                while recording:
                    file.write(q.get())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print('Audio recording has been stopped.')
        # Ensure the stream is stopped
        sd.stop()

def record_video():
    """Function to record video."""
    global recording
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    print('Recording video... Press "q" to stop.')
    while recording:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print('Video recording has been stopped.')

def stop_recording():
    """Function to stop recording."""
    global recording
    recording = False

def combine_audio_video(timestamp):
    """Combine audio and video into a single file."""
    audio_file = f'media/audio/audio_{timestamp}.wav'  # Filename to save the audio
    # Parameters for video recording
    video_file = f'media/video/video_{timestamp}.avi'  # Filename to save the video
    final_filename = f'final_output_{timestamp}.mp4'
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(f"media/joint/{final_filename}", codec="libx264")
    print('Audio and video have been merged. Final file:', final_filename)
    return timestamp

def main():
    global recording
    global timestamp
    # Parameters for audio recording
    global samplerate
    global channels
    global audio_filename
    global video_filename
    samplerate = 44100  # Sample rate in Hertz
    channels = 2        # Number of audio channels
    timestamp = time.time()
    audio_filename = f'media/audio/output_audio_{timestamp}.wav'  # Filename to save the audio

    # Parameters for video recording
    video_filename = f'media/video/output_video_{timestamp}.avi'  # Filename to save the video

    # Create a queue to hold the audio data
    q = queue.Queue()
    # Start the audio and video recording in separate threads
    audio_thread = threading.Thread(target=record_audio)
    video_thread = threading.Thread(target=record_video)

    audio_thread.start()
    video_thread.start()

    # Set a hook for the 'q' key to stop recording
    keyboard.add_hotkey('q', stop_recording)

    # Wait for the recording threads to finish
    audio_thread.join()
    video_thread.join()

    # Additional wait to ensure the files are released
    time.sleep(1)
    recording = True

    # Combine audio and video
    result= combine_audio_video(timestamp)
    return result
