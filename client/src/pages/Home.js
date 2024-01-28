import { Card, Modal } from 'antd';
import React, { useState, useEffect } from 'react';

import memoriesData from '../memories.json';
import background from './backdrop.png';
import './Home.css'; // Adjust the path if necessary



const { Meta } = Card;

/*
const backgroundImage = {
  backgroundImage: `url(${background})`,
  backgroundSize: 'cover',
  backgroundRepeat: 'repeat-y',
  backgroundAttachment: 'fixed',
  height: '100vh', // Ensures the div is at least as tall as the viewport
  width: '100vw', // Ensures the div is at least as wide as the viewport
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
};
*/


function MemoryCard({ memory, onClick }) {
  const { name, transcription, filename, context } = memory;
  const cardStyle = {
    maxWidth: '400px',
    maxHeight: '800px'
  };


  const cardTitle = (
    <div>
      <h2>{name}</h2>
    </div>
  );
  console.log(filename)
  return (
    <Card
      className='m-6 shadow-2xl'
      hoverable
      onClick={onClick}
      style={cardStyle}
      cover={filename && (filename.endsWith('.mp4') ? (
        <video controls width="100%" style={{height: "300px"}}>
          <source src={"/media/joint/" + filename} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      ) : (
        <img src={"/media/photo/" + filename} alt="Memory" style={{ maxWidth: '100%' }} />
      ))}
    >
      <Card.Meta title={name} description={context.substring(0, 200) + "..."} />
    </Card>
  );
}

function App() {
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedMemory, setSelectedMemory] = useState(null);
  const bubbleColors = [
    'rgba(102, 153, 255, 0.7)', // Shade of Blue
    'rgba(255, 153, 204, 0.7)', // Shade of Pink
    'rgba(204, 153, 255, 0.7)', // Shade of Purple
  ];
  
  useEffect(() => {
    const bubbleArea = document.querySelector('.App');
    const createBubble = () => {
      const bubble = document.createElement('span');
      var size = Math.random() * 60;
      
      bubble.style.width = 20 + size + 'px';
      bubble.style.height = 20 + size + 'px';
      bubble.style.left = Math.random() * window.innerWidth + 'px';
      // Choose a random color from the bubbleColors array
      bubble.style.background = bubbleColors[Math.floor(Math.random() * bubbleColors.length)];
  
      bubbleArea.appendChild(bubble);
  
      setTimeout(() => {
        bubble.remove();
      }, 4000);
    };
  
    // Create bubbles at intervals
    const bubbleInterval = setInterval(createBubble, 500);
  
    return () => clearInterval(bubbleInterval); // Cleanup on component unmount
  }, []);
  // end of bubbles

  const openModal = (memory) => {
    setSelectedMemory(memory);
    setModalVisible(true);
  };

  const closeModal = () => {
    setSelectedMemory(null);
    setModalVisible(false);
  };

  return (
    /* <div className="App" style={backgroundImage}> */
    <div className="App">
      <div className="memory-grid" style={{
          display: 'flex',
          flexWrap: 'wrap',
        }}>
        <div className='flex justify-center w-full'>
          <div className="grid grid-cols-3 gap-4">
          {memoriesData.memories.map((memory, index) => (
              <MemoryCard key={index} memory={memory} onClick={() => openModal(memory)} />
          ))}
          </div>
        </div>
      </div>

      <Modal
        visible={modalVisible}
        onCancel={closeModal}
        title={selectedMemory && selectedMemory.name}
        footer={null}
      >
        {selectedMemory && (
          <>
            
      <Card cover={selectedMemory.filename && (selectedMemory.filename.endsWith('.mp4') ? (
        <video controls width="100%" style={{height: "300px"}}>
          <source src={"/media/joint/" + selectedMemory.filename} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      ) : (
        <img src={"/media/photo/" + selectedMemory.filename} alt="Memory" style={{ maxWidth: '100%' }} />
      ))}>
          <Card.Meta title="Context" description={selectedMemory.context} />
          <br />
          <Card.Meta title="Transcription" description={selectedMemory.transcription} />
          <br />
          <Card.Meta title="People" description={selectedMemory.people} />
          <br />
          <Card.Meta title="Location" description={selectedMemory.location} />
          <br />
          <Card.Meta title="Timestamp" description={selectedMemory.timestamp} />                </Card>
        </>
        )}
      </Modal>
    </div>
  );
}

export default App;
