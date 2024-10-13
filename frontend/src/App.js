import React, { useState } from "react";

import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Routes, useParams, useSearchParams } from 'react-router-dom';
import DragDrop from "./homepage";
import VideoProcessor from "./VideoProcessor";
import "./App.css";

function App() {
    const [videoFile, setVideoFile] = useState(null);

    return (
        <div className="App">
            <BrowserRouter> { }
                <Routes>
                    <Route path='/' element={<DragDrop setVideoFile={setVideoFile} />} />
                    <Route path='/video-processor' element={<VideoProcessor videoFile={videoFile} />} />
                </Routes>
            </BrowserRouter>
        </div >
    );
}

export default App;
