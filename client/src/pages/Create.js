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
        setSearchValue(searchTerm)
        console.log(imageSrc)
    };

    const handleSubmit = (e) => {
        e.preventDefault()
        console.log(selectedValue)
        console.log(imageSrc)
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
        const res = await fetch('http://127.0.0.1:2000/api/search', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(req)
        });

        const res_data = res.json()

        return res_data
    };

  return (
    <div className='flex flex-col items-center m-10'>
        <SearchBar onSearch={handleSearch} />
        <Camera isPhoto={true} />


    </div>
  )
}

export default Create
