import React from 'react'
import Camera from '../components/Camera';
import SearchBar from '../components/SearchBar';


const Create = () => {
    const handleSearch = (searchTerm) => {
        console.log("Searching for:", searchTerm);
        // Implement your search logic here
    };

  return (
    <div className='flex flex-col items-center m-10'>
        <SearchBar onSearch={handleSearch} />
        <Camera />
    </div>
  )
}

export default Create
