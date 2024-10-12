import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import "./index.scss";
import axios from 'axios';

function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

function convertBlobToBinaryString(blob) {
    return '$binary' + btoa(String.fromCharCode.apply(null, new Uint8Array(blob)));
}
class VideoProcessor extends React.Component {
    constructor(props) {
        super(props);

        this.playerRef = React.createRef();
        this.videoRef = React.createRef();
        this.canvasRef = React.createRef();
        this.newVideoRef = React.createRef();
        this.pauseRef = React.createRef();
        this.isPlaying = false;
        this.videoUrl = URL.createObjectURL(props.videoFile);
        this.state = {
            currentSvgIndex: 0,
        };
        this.svgs = [
            // Первый SVG 
            <svg width="50" height="50" viewBox="0 0 218 230" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M199.42 84.7801C204.903 87.696 209.49 92.049 212.688 97.3725C215.887 102.696 217.576 108.789 217.576 115C217.576 121.21 215.887 127.304 212.688 132.627C209.49 137.951 204.903 142.304 199.42 145.22L53.1492 224.76C29.5966 237.581 0.666748 220.912 0.666748 194.551V35.4601C0.666748 9.08758 29.5966 -7.56934 53.1492 5.22875L199.42 84.7801Z" fill="#D2D2D2" />
            </svg>,
            // Второй SVG
            <svg width="50" height="50" viewBox="0 0 185 217" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M31 216.125C47.9125 216.125 61.75 202.288 61.75 185.375V31.625C61.75 14.7125 47.9125 0.875 31 0.875C14.0875 0.875 0.25 14.7125 0.25 31.625V185.375C0.25 202.288 14.0875 216.125 31 216.125ZM123.25 31.625V185.375C123.25 202.288 137.087 216.125 154 216.125C170.913 216.125 184.75 202.288 184.75 185.375V31.625C184.75 14.7125 170.913 0.875 154 0.875C137.087 0.875 123.25 14.7125 123.25 31.625Z" fill="#D2D2D2" />
            </svg>

        ];
    }

    detect = (canvasElement, context_video) => {
        canvasElement.toBlob(async (blob) => {
            const formData = new FormData();
            formData.append('frame', blob);

            axios.post('http://127.0.0.1:8000/api/v0/video/frame/detect', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': 'Bearer *',
                    'Access-Control-Allow-Origin': '*',
                }
            })
                .then(response => {
                    const imageURL = `data:image/jpeg;base64,${response.data['image']}`;

                    const img = new Image();
                    img.onload = () => {
                        if (this.isPlaying) {
                            context_video.drawImage(img, 0, 0, canvasElement.width, canvasElement.height);
                        }
                        URL.revokeObjectURL(imageURL);
                    };
                    img.src = imageURL;
                })
                .catch(error => {
                    console.error('Ошибка отправки кадра:', error);
                });
        }, 'image/jpeg')
    }

    componentDidMount = () => {
        if (this.props.videoFile) {
            const playerElement = this.playerRef.current;
            const videoElement = this.videoRef.current;
            const canvasElement = this.canvasRef.current;
            const newVideoElement = this.newVideoRef.current;
            const pauseElement = this.pauseRef.current;
            const context = canvasElement.getContext('2d');
            const context_video = newVideoElement.getContext('2d');
            canvasElement.width = playerElement.offsetWidth * 0.8;
            canvasElement.height = canvasElement.width * videoElement.offsetHeight / videoElement.offsetWidth;
            newVideoElement.width = canvasElement.width;
            newVideoElement.height = canvasElement.height;

            pauseElement.style.left = `${-newVideoElement.width / 2 + 50}px`;
            pauseElement.style.top = `${newVideoElement.height - 80}px`;

            context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

            const frame = context.getImageData(0, 0, canvasElement.width, canvasElement.height);

            context.putImageData(frame, 0, 0);

            videoElement.onplay = () => {
                const drawFrame = () => {
                    if (!videoElement.paused && !videoElement.ended) {
                        context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

                        const frame = context.getImageData(0, 0, canvasElement.width, canvasElement.height);

                        this.detect(canvasElement, context_video);

                        context.putImageData(frame, 0, 0);

                        requestAnimationFrame(drawFrame);
                    }
                };
                drawFrame();
            };
        }
    }

    pause = () => {
        if (this.isPlaying) {
            this.videoRef.current.pause();
            this.isPlaying = false;
        } else {
            this.videoRef.current.play();
            this.isPlaying = true;
        }
    }

    handleClick = () => {
        const nextIndex = (this.state.currentSvgIndex + 1) % this.svgs.length;
        this.setState({ currentSvgIndex: nextIndex });
        this.pause()
    };

    render = () => {
        return (
            <div className="video-player-zone" ref={this.playerRef}>
                <video
                    ref={this.videoRef}
                    className="video"
                    controls
                >
                    <source src={this.videoUrl} type={this.props.videoFile.type} />
                    Your browser does not support the video tag.
                </video>
                <div className='player'>
                    <button className="bth-pause" ref={this.pauseRef} onClick={this.handleClick}>
                        {this.svgs[this.state.currentSvgIndex]} {/* Отображаем текущий SVG */}
                    </button>
                    <canvas className="get-frame" ref={this.canvasRef} width="50%" height="50%" />
                    <canvas className="new-video" ref={this.newVideoRef} width="50%" height="50%" />
                </div>
            </div>
        );
    };
}

export default VideoProcessor;

