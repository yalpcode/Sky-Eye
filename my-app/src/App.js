import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";

import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Routes, useParams, useSearchParams } from 'react-router-dom';
import DragDrop from "./homepage";

function App() {
  // ... (внутри функции App нет логики, поэтому здесь нет комментариев)

  return (
    <div className="App"> 
      <BrowserRouter> {/* BrowserRouter только один, вокруг Routes */}
        <Routes> 
          <Route path='/' element={<DragDrop />} /> 
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

