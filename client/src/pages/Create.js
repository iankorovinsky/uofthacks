import React, { useState, useEffect } from 'react';
import { Card, Modal } from 'antd';
import Camera from '../components/Camera';
import SearchBar from '../components/SearchBar';
import './Record.css'; 
import { Select, Button, Box, form } from '@chakra-ui/react';
import { useImageContext } from '../components/ImageContext';

import memoriesData from '../display_memories.json';

import axios from 'axios';

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
  

const Create = () => {
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

      
    const [selectedValue, setSelectedValue] = useState('');
    const [searchValue, setSearchValue] = useState('');
    const [text, setText] = useState('');

    const { imageSrc } = useImageContext();

    const apiKey = "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"

    const handleSearch = (searchTerm) => {
        console.log(searchTerm)
        setText(searchTerm)
    };

    const handleSubmit = (e) => {
        e.preventDefault()

        const formData = new FormData();
        formData.append('imagetext', text);

        const res = callSearch(formData)
        console.log(res)
    };

    const handleChange = (event) => {
        setSelectedValue(event.target.value);
    };

    const handleUpload = async (e) => {
        e.preventDefault()
        const headers = {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${apiKey}`
          };
    
          
        const payload = {
          model: "gpt-4-vision-preview",
          messages: [
            {
              role: "user",
              content: [
                { type: "text", text: "What’s in this image?" },
                { type: "image_url", image_url: { url: imageSrc } }
              ]
            }
          ],

          max_tokens: 300
        };
    
        try {
          const response = await axios.post('https://api.openai.com/v1/chat/completions', payload, { headers });
          const response_data = response.data
          
          const content = response_data["choices"][0]["message"]["content"]
          console.log(content)
          setText(content)

          console.log("handling submit")
          handleSubmit()

          const req = {
            form: { 
                "imagetext": text 
            }
          }

          const res = callSearch(req)
          console.log(res)

        } catch (error) {
          console.error(error);
        }
    };

    const callSearch = async (req) => {
        const res = await fetch(' http://127.0.0.1:2000/api/search', {
            method: 'POST',
            body: req
        });

        const res_data = res.json()

        console.log(res_data)

        return res_data
    };

  return (
    <div className='flex flex-col items-center'>
        <div className='flex flex-col items-center mt-10 mx-10'>
            <SearchBar onSearch={handleSearch} />
            <Camera isPhoto={true} />
        </div>
        <Box as="form" onSubmit={handleSubmit} className='mr-96'> 
        <Button
        type="submit"
        style={{
            backgroundColor: '#6f86d6', // A vibrant blue shade
            color: 'white' // Assuming you want the text color to be white
        }}
        >
        Submit
        </Button>
        </Box>

        <div className="memory-grid" style={{
          display: 'flex',
          flexWrap: 'wrap',
        }}>
        <div className='flex justify-center w-full'>
          <div className="grid grid-cols-3 gap-4">
          {memoriesData.display_memories.map((memory, index) => (
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
          <Card.Meta title="Timestamp" description={selectedMemory.timestamp} /> </Card>
        </>
        )}
      </Modal>
</div>
  )
}



export default Create
