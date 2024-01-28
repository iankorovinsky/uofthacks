// FormContext.js
import React, { createContext, useState, useContext } from 'react';

const FormContext = createContext();

export const useFormContext = () => useContext(FormContext);

export const FormProvider = ({ children }) => {
  const [formSrc, setFormSrc] = useState(null);

  return (
    <FormContext.Provider value={{ formSrc, setFormSrc }}>
      {children}
    </FormContext.Provider>
  );
};
