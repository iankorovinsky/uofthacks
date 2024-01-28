import React, { useRef, useState } from 'react';
import { Button } from "@chakra-ui/button"

import './component-styles/Camera.css'
import { useImageContext } from './ImageContext';
import { useFormContext } from './FormContext';

const Camera = ({ isPhoto }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [flash, setFlash] = useState(false);
  const [photoTaken, setPhotoTaken] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);

  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  const { setImageSrc } = useImageContext();
  const { setFormSrc } = useFormContext();

  const startVideo = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      setStream(stream);
      videoRef.current.play();
    } catch (err) {
      console.error("Error accessing the camera: ", err);
    }

    setCameraActive(true);
  };

  const stopVideo = () => {
    console.log("stopping camera")
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setCameraActive(false);
      console.log("stopping stream")
    }
  };

  const takePhoto = ({ showFlash = true, showMessage = true, saveLocally = false, upload = false }) => {
    if(cameraActive) {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
        // You can save the image from here, display it, or send it to a server
        if(saveLocally) {
            canvas.toBlob((blob) => {
                savePhotoLocally(blob);
              }, 'image/png');
        }

        if(upload) {
            canvas.toBlob((blob) => {
                const formData = new FormData();
                formData.append('photo', blob, 'photo.png');

                for (let [key, value] of formData.entries()) {
                    console.log(`${key}:`, value);
                }
              }, 'image/png');

              
        }

        const imageSrc = canvas.toDataURL('image/png');
        setImageSrc(imageSrc)
        
        if(showFlash) {
            setFlash(true);
        }

        if(showMessage) {
            setPhotoTaken(true);
        }

        setTimeout(() => {
          setFlash(false);
        }, 1000);
    
        setTimeout(() => {
            setPhotoTaken(false);
        }, 2000);
    }
  };

  const takeVideo = ({ save = false }) => {
    takePhoto({ showFlash: false, showMessage: false, saveLocally: false, upload: true })
    if (cameraActive && videoRef.current) {
      if (isRecording) {
        // Stop recording
        mediaRecorder.stop();
        setIsRecording(false);
      } else {
            // Start recording
            const options = { mimeType: "video/webm" };
            const recorder = new MediaRecorder(videoRef.current.srcObject, options);
            let chunks = [];
    
            recorder.ondataavailable = event => chunks.push(event.data);
            recorder.onstop = async () => {
            const blob = new Blob(chunks, { type: "video/webm" });
            chunks = [];
    
            // Here you can handle the blob, e.g., upload it to the server
    
            uploadVideo(blob);
        };
        recorder.start();
        setMediaRecorder(recorder);
        setIsRecording(true);
      }
    }
  };  

  const uploadVideo = async (videoBlob) => {
    const formData = new FormData();
    formData.append('blob', videoBlob);

    setFormSrc(formData)
  };


  const savePhotoLocally = async (blob) => {
    if ('showSaveFilePicker' in window) {
      try {
        // Create a handle to the new file on the file system.
        const fileHandle = await window.showSaveFilePicker({
          suggestedName: 'photo.png',
          types: [{
            description: 'PNG image file',
            accept: { 'image/png': ['.png'] },
          }],
        });
  
        // Create a FileSystemWritableFileStream to write to.
        const writableStream = await fileHandle.createWritable();
  
        // Write the contents of the blob to the file.
        await writableStream.write(blob);
  
        // Close the file and write the contents to disk.
        await writableStream.close();
  
        alert('Photo saved successfully!');
      } catch (error) {
        console.error('Error saving file:', error);
      }
    } else {
      alert('Your browser does not support the File System Access API.');
    }
  };  

  const saveFileLocally = async (blob) => {
    if ('showSaveFilePicker' in window) {
      try {
        // Create a handle to the new file on the file system.
        const fileHandle = await window.showSaveFilePicker({
          suggestedName: 'video.webm',
          types: [{
            description: 'WebM video file',
            accept: { 'video/webm': ['.webm'] },
          }],
        });
  
        // Create a FileSystemWritableFileStream to write to.
        const writableStream = await fileHandle.createWritable();
  
        // Write the contents of the blob to the file.
        await writableStream.write(blob);
  
        // Close the file and write the contents to disk.
        await writableStream.close();
  
        alert('Video saved successfully!');
      } catch (error) {
        console.error('Error saving file:', error);
      }
    } else {
      alert('Your browser does not support the File System Access API.');
    }
  };
  
  

  return (
    <div className="camera-container">
      <div className={`video-wrapper`}>
        <video ref={videoRef} width="640" height="480" />
        {flash && <div className="flash-overlay"></div>}
      </div>
      <div className='flex justify-around m-5'>
        
        {cameraActive ? (
            <Button onClick={stopVideo}>Stop Camera</Button>
        ) : (
            <Button onClick={startVideo}>Start Camera</Button>
        )}
        {isPhoto ? ( 
            <Button onClick={takePhoto}>Take Photo</Button>
         ) : (
            <div>
                {isRecording ? (
                    <Button onClick={takeVideo}>Stop Video</Button>
                ) : (
                    <Button onClick={takeVideo}>Take Video</Button>
                )}
            </div>
        )}
    </div>
      <canvas ref={canvasRef} width="640" height="480" style={{ display: 'none' }} />
      {photoTaken && <div className="photo-taken-message">Photo Taken</div>}
    </div>
  );
};

export default Camera;
