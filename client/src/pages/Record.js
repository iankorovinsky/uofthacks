import React, { useState } from 'react';

import { Select, Button, Box, form } from '@chakra-ui/react'
import Camera from '../components/Camera';
import { useImageContext } from '../components/ImageContext';
import { useFormContext } from '../components/FormContext';


const Record = () => {
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
        <Button type="submit" colorScheme='green'>Submit</Button>
    </Box>
</div>
  )
}

export default Record
