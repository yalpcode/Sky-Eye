import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import { useNavigate } from 'react-router-dom';
import "./index.scss";

const fileTypes = ["MOV", "MP4"];

function DragDrop({ setVideoFile }) {
    const [dragActive, setDragActive] = React.useState(false);
    const inputRef = React.useRef(null);

    const to = useNavigate();

    const handleFile = (file) => {
        setVideoFile(file);
        to('/video-processor');
    }

    const handleDrag = function (e) {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = function (e) {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0])
        }
    };

    const handleChange = function (e) {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0])
        }
    };

    const onButtonClick = () => {
        inputRef.current.click();
    };

    return (
        <div>
            <div className="name">
                <h1 className="name__text">DroneAI</h1>
            </div>
            <div className="form">
                <div className="input-form">
                    <p className="upload-file-text">Upload file</p>
                    <form id="form-file-upload" onDragEnter={handleDrag} onSubmit={(e) => e.preventDefault()}>
                        <input ref={inputRef} type="file" id="input-file-upload" multiple={true} onChange={handleChange} accept="video/*" />
                        <label id="label-file-upload" htmlFor="input-file-upload" className={dragActive ? "drag-active" : ""}>
                            <svg width="227" height="269" viewBox="0 0 227 269" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M81.25 204H145.75C154.619 204 161.875 196.744 161.875 187.875V107.25H187.514C201.865 107.25 209.121 89.835 198.962 79.6762L124.949 5.6625C123.457 4.16765 121.685 2.9817 119.734 2.17252C117.784 1.36335 115.692 0.946838 113.581 0.946838C111.469 0.946838 109.378 1.36335 107.427 2.17252C105.476 2.9817 103.704 4.16765 102.213 5.6625L28.1988 79.6762C18.04 89.835 25.135 107.25 39.4862 107.25H65.125V187.875C65.125 196.744 72.3812 204 81.25 204ZM16.75 236.25H210.25C219.119 236.25 226.375 243.506 226.375 252.375C226.375 261.244 219.119 268.5 210.25 268.5H16.75C7.88125 268.5 0.625 261.244 0.625 252.375C0.625 243.506 7.88125 236.25 16.75 236.25Z" fill="#8CB676" />
                            </svg>
                            <div>
                                <p className="input-text">Drag and drop your file here or </p>
                                <button className="upload-button" onClick={onButtonClick}>browse</button>
                            </div>
                        </label>
                        {dragActive && <div id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}></div>}
                    </form>
                </div>
            </div>
        </div>
    );
};

export default DragDrop;

