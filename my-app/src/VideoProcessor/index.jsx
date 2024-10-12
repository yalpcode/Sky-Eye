import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

class VideoProcessor extends React.Component {
    // canvasRef = useRef(null);
    // videoUrl = null;

    constructor(props) {
        super(props);

        this.videoUrl = URL.createObjectURL(props.videoFile);
    }


    render = () => {
        return (
            <div>
                <video
                    className="video"
                    // autoload="metadata"
                    width="100%"
                    controls
                >
                    <source src={this.videoUrl} type={this.props.videoFile.type} />
                    Your browser does not support the video tag.
                </video>
                {/* <canvas ref={this.canvasRef} width="640" height="360" /> */}
            </div>
        );
    };
}

export default VideoProcessor;

