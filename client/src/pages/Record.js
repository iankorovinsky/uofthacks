import React, { useState } from 'react';

import { Select, Button, Box, form } from '@chakra-ui/react'
import Camera from '../components/Camera';
import { useImageContext } from '../components/ImageContext';


const Record = () => {
    const [selectedValue, setSelectedValue] = useState('');
    const [searchValue, setSearchValue] = useState('');

    const { imageSrc } = useImageContext();

    const handleSubmit = (e) => {
        e.preventDefault()
        console.log(selectedValue)
    };

    const handleChange = (event) => {
        setSelectedValue(event.target.value);
      };

  return (
    <div className='flex flex-col items-center m-10'>
        <Camera isPhoto={false} />
        <Box as="form" onSubmit={handleSubmit}>
        `  <Select placeholder="Select person" width="480px" onChange={handleChange}> 
                <option value="ian">Ian</option>
                <option value="lucy">Lucy</option>
                <option value="stephen">Stephen</option>
                <option value="william">William</option>
            </Select>
            <Button type="submit" mt={4}>Submit</Button>`
        </Box>
    </div>
  )
}

export default Record
