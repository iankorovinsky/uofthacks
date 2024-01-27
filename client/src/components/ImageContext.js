// ImageContext.js
import React, { createContext, useState, useContext } from 'react';

const ImageContext = createContext();

export const useImageContext = () => useContext(ImageContext);

export const ImageProvider = ({ children }) => {
  const [imageSrc, setImageSrc] = useState(null);

  return (
    <ImageContext.Provider value={{ imageSrc, setImageSrc }}>
      {children}
    </ImageContext.Provider>
  );
};
