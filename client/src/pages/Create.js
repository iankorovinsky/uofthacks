import React, { useState } from 'react';
import Camera from '../components/Camera';
import SearchBar from '../components/SearchBar';

import { Select, Button, Box, form } from '@chakra-ui/react'
import { useImageContext } from '../components/ImageContext';

import axios from 'axios';

const Create = () => {
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
          setText(content)

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
    <Box as="form" onSubmit={handleSubmit} w="100%" display="flex" justifyContent="center" mt={4}>
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

export default Create
