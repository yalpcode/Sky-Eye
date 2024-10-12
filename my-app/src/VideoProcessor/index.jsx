import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import "./index.scss";

class VideoProcessor extends React.Component {
    constructor(props) {
        super(props);

        this.playerRef = React.createRef();
        this.videoRef = React.createRef();
        this.canvasRef = React.createRef();
        this.isPlaying = false;
        this.videoUrl = URL.createObjectURL(props.videoFile);
    }

    componentDidMount = () => {
        if (this.props.videoFile) {
            const playerElement = this.playerRef.current;
            const videoElement = this.videoRef.current;
            const canvasElement = this.canvasRef.current;
            const context = canvasElement.getContext('2d');
            canvasElement.width = playerElement.offsetWidth * 0.8;
            canvasElement.height = canvasElement.width * videoElement.offsetHeight / videoElement.offsetWidth;

            context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

            const frame = context.getImageData(0, 0, canvasElement.width, canvasElement.height);

            context.putImageData(frame, 0, 0);

            videoElement.onplay = () => {
                const drawFrame = () => {
                    if (!videoElement.paused && !videoElement.ended) {
                        context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

                        const frame = context.getImageData(0, 0, canvasElement.width, canvasElement.height);
                        console.log(frame.data);

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
                <canvas className="new-video" ref={this.canvasRef} width="50%" height="50%" />
                <button className="bth-pause" onClick={this.pause}> ➡️ </button>
            </div>
        );
    };
}

export default VideoProcessor;

