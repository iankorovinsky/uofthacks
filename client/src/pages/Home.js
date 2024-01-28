import { Card, Modal } from 'antd';
import React, { useState } from 'react';

import memoriesData from '../memories.json';

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
      <Card.Meta title={name} description={context} />
    </Card>
  );
}

function App() {
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedMemory, setSelectedMemory] = useState(null);

  const openModal = (memory) => {
    setSelectedMemory(memory);
    setModalVisible(true);
  };

  const closeModal = () => {
    setSelectedMemory(null);
    setModalVisible(false);
  };

  return (
    <div className="App">
      <div className="memory-grid" style={{
          display: 'flex',
          flexWrap: 'wrap',
        }}>
        {memoriesData.memories.map((memory, index) => (
          <MemoryCard key={index} memory={memory} onClick={() => openModal(memory)} />
        ))}
      </div>

      <Modal
        visible={modalVisible}
        onCancel={closeModal}
        title={selectedMemory && selectedMemory.name}
        footer={null}
      >
        {selectedMemory && (
          <>
            {selectedMemory.filename && (selectedMemory.filename.endsWith('.mp4') ? (
        <video controls width="100%" style={{height: "300px"}}>
          <source src={"/media/joint/" + selectedMemory.filename} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      ) : (
        <img src={"/media/photo/" + selectedMemory.filename} alt="Memory" style={{ maxWidth: '100%' }} />
      ))}
    
          </>
        )}
      </Modal>
    </div>
  );
}

export default App;
