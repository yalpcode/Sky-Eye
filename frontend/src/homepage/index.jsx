import React, { useState, useRef, useEffect, useLayoutEffect } from "react";
import { useNavigate } from 'react-router-dom';
import "./index.scss";
import { useInterval } from 'react-use'
import droneImage from './drone.png'
import Drone from "./Drone";


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

    const [screenWidth, setScreenWidth] = useState(0);
    const [screenHeight, setScreenHeight] = useState(0);

    useEffect(() => {
        const handleResize = () => {
            setScreenWidth(window.innerWidth);
            setScreenHeight(window.innerHeight);
        };

        window.addEventListener('resize', handleResize);
        handleResize(); // Вызываем при начальной загрузке

        return () => window.removeEventListener('resize', handleResize);
    }, []);

    console.log(screenHeight, screenWidth)

    return (
        <div>
            <div className="name">
                <span className="drone">SKY </span>
                <span className="ai">EYE</span>
            </div>
            <Drone screenHeight = {screenHeight} screenWidth = {screenWidth} ></Drone>
            <Drone screenHeight = {screenHeight} screenWidth = {screenWidth} ></Drone>
            <Drone screenHeight = {screenHeight} screenWidth = {screenWidth} ></Drone>
            <Drone screenHeight = {screenHeight} screenWidth = {screenWidth} ></Drone>
            <Drone screenHeight = {screenHeight} screenWidth = {screenWidth} ></Drone>
            <Drone screenHeight = {screenHeight} screenWidth = {screenWidth} ></Drone>
            <Drone screenHeight = {screenHeight} screenWidth = {screenWidth} ></Drone>
            <Drone screenHeight = {screenHeight} screenWidth = {screenWidth} ></Drone>
            <div className="form">
                <div className="input-form">
                    <p className="upload-file-text">Upload file</p>
                    <form id="form-file-upload" onDragEnter={handleDrag} onSubmit={(e) => e.preventDefault()}>
                        <input ref={inputRef} type="file" id="input-file-upload" multiple={true} onChange={handleChange} accept="video/*" />
                        <label id="label-file-upload" htmlFor="input-file-upload" className={dragActive ? "drag-active" : ""}>
                            <svg width="83" height="98" viewBox="0 0 83 98" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M29.6429 74.3748H53.3571C56.6179 74.3748 59.2857 71.7169 59.2857 68.4685V38.937H68.7121C73.9886 38.937 76.6564 32.5582 72.9214 28.8372L45.7093 1.72726C45.1608 1.17973 44.5093 0.745333 43.7921 0.448946C43.0749 0.15256 42.3061 0 41.5296 0C40.7532 0 39.9844 0.15256 39.2672 0.448946C38.55 0.745333 37.8985 1.17973 37.35 1.72726L10.1379 28.8372C6.40286 32.5582 9.01143 38.937 14.2879 38.937H23.7143V68.4685C23.7143 71.7169 26.3821 74.3748 29.6429 74.3748ZM5.92857 86.1874H77.0714C80.3321 86.1874 83 88.8452 83 92.0937C83 95.3422 80.3321 98 77.0714 98H5.92857C2.66786 98 0 95.3422 0 92.0937C0 88.8452 2.66786 86.1874 5.92857 86.1874Z" fill="#ECECEC" />
                            </svg>
                        </label>
                        <div className="text">
                            <p className="input-text">Drag and drop your file here or browse</p>
                            <p className="summarize">Once uploaded, the video will be processed by a neural network. You will see recognized flying objects.</p>
                        </div>
                        {dragActive && <div id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}></div>}
                    </form>
                </div>
            </div>
        </div>
    );
};

export default DragDrop;
