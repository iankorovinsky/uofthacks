import React, { useRef, useState } from 'react';
import './Camera.css'

const Camera = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [flash, setFlash] = useState(false);
  const [photoTaken, setPhotoTaken] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);

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

  const takePhoto = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // You can save the image from here, display it, or send it to a server
    const imageSrc = canvas.toDataURL('image/png');
    console.log(imageSrc);

    setFlash(true);
    setPhotoTaken(true);
    setTimeout(() => {
      setFlash(false);
    }, 1000);

    setTimeout(() => {
        setPhotoTaken(false);
      }, 2000);
  };

  return (
    <div className="camera-container">
      <div className="video-wrapper">
        <video ref={videoRef} width="640" height="480" />
        {flash && <div className="flash-overlay"></div>}
      </div>
      <div className='flex justify-around'>
        {cameraActive ? (
            <button onClick={stopVideo}>Stop Camera</button>
        ) : (
            <button onClick={startVideo}>Start Camera</button>
        )}
      <button onClick={takePhoto}>Take Photo</button>
    </div>
      <canvas ref={canvasRef} width="640" height="480" style={{ display: 'none' }} />
      {photoTaken && <div className="photo-taken-message">Photo Taken</div>}
    </div>
  );
};

export default Camera;
