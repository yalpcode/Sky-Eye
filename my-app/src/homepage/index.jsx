import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import "./index.scss";

const fileTypes = ["MOV", "MP4"];

async function sendPostRequest(url, data, redirectUrl) {
    try {
        const formData = new FormData();
        formData.append('file', data.file[0]);

        const response = await fetch(url, {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            console.log('Успешный POST-запрос:', result);
            window.location.href = redirectUrl;
        } else {
            console.error('Ошибка POST-запроса:', response.status);
        }
    } catch (error) {
        console.error('Ошибка POST-запроса:', error);
    }
}

function DragDrop() {
    // drag state
    const [dragActive, setDragActive] = React.useState(false);
    // ref
    const inputRef = React.useRef(null);

    // handle drag events
    const handleDrag = function (e) {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    // triggers when file is dropped
    const handleDrop = function (e) {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            sendPostRequest("/get_files", { "file": e.dataTransfer.files }, "/ok")
        }
    };

    // triggers when file is selected with click
    const handleChange = function (e) {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            sendPostRequest("/get_files", { "file": e.target.files }, "/ok")
        }
    };

    // triggers the input when the button is clicked
    const onButtonClick = () => {
        inputRef.current.click();
    };

    return (
        <form className="input-form" id="form-file-upload" onDragEnter={handleDrag} onSubmit={(e) => e.preventDefault()}>
            <input ref={inputRef} type="file" id="input-file-upload" multiple={true} onChange={handleChange} accept="video/*"/>
            <label id="label-file-upload" htmlFor="input-file-upload" className={dragActive ? "drag-active" : ""}>
                <div>
                    <p>Drag and drop your file here or</p>
                    <button className="upload-button" onClick={onButtonClick}>Upload a file</button>
                </div>
            </label>
            {dragActive && <div id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}></div>}
        </form>
    );
};

export default DragDrop;

