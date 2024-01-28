import React, { useState, useEffect } from 'react';

import './Record.css'; 

import { Select, Button, Box, form } from '@chakra-ui/react'
import Camera from '../components/Camera';
import { useImageContext } from '../components/ImageContext';
import { useFormContext } from '../components/FormContext';


const Record = () => {
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
    const [selectedValue, setSelectedValue] = useState('');
    const [searchValue, setSearchValue] = useState('');

    const { imageSrc } = useImageContext();
    const { formSrc } = useFormContext();

    const handleChange = (event) => {
        setSelectedValue(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault()
        formSrc.append('person', selectedValue);
        for (let [key, value] of formSrc.entries()) {
            console.log(`${key}:`, value);
        }

        const res = callUpload(formSrc)
        console.log(res)
    }

    const callUpload = async (req) => {
        const res = await fetch(' http://127.0.0.1:2000/api/upload', {
            method: 'POST',
            body: req
        });

        const res_data = res.json()

        console.log(res_data)

        return res_data
    };

  return (
    <div className='flex flex-col items-center m-10'>
    <Camera isPhoto={false} />
    <Box as="form" onSubmit={handleSubmit} display="flex" flexDirection="column" alignItems="center" w="100%">
        <Select placeholder="Select person" width="480px" onChange={handleChange} mb={4}>
            <option value="IAN">Ian</option>
            <option value="LUCY">Lucy</option>
            <option value="STEPHEN">Stephen</option>
            <option value="WILLIAM">William</option>
        </Select>
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
</div>
  )
}

export default Record
