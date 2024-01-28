import { Routes, Route, BrowserRouter } from "react-router-dom";
import React, { Suspense } from "react";
import { AnimatePresence } from 'framer-motion'

import { ChakraProvider } from '@chakra-ui/react';

import { ImageProvider } from './components/ImageContext';
 
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Create from './pages/Create'
import Record from './pages/Record'
import Gallery from "./pages/Gallery";

const App = () => {
  return (
    <div className="App bg-white">
    <ChakraProvider>
      <ImageProvider>
        <BrowserRouter>
            <Suspense fallback={<div>Page Loading...</div>}>
            <Navbar />
            <AnimatePresence
            mode='wait'>
              <Routes>
                <Route path="/" exact element={<Home />} />
                <Route path="/create" exact element={<Create />} />
                <Route path="/record" exact element={<Record />} />
                <Route path="/gallery" exact element={<Gallery />} />
              </Routes>
            </AnimatePresence>
            </Suspense>
        </BrowserRouter>
      </ImageProvider>
    </ChakraProvider>
  </div>
  )
}

export default App
