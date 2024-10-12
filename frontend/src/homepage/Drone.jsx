import React, { useState, useRef, useEffect, useLayoutEffect } from "react";
import "./index.scss";
import { useInterval } from 'react-use'
import droneImage from './drone.png'

function randint(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function Drone(args) {
    const screenWidth = args.screenWidth
    const screenHeight = args.screenHeight

    const [x1, setX1] = useState(0);
    const [y1, setY1] = useState(0);

    useInterval(() => {
        setX1(randint(0, screenWidth - 400));
        setY1(randint(0, screenHeight - 300));
    }, randint(1000, 2000));

    return (
        <div className="drone1" style={{
            position: 'absolute'
        }}>
            <img
                className="flying1"
                src={droneImage}
                style={{
                    position: 'absolute',
                    transition: 'transform 3s ease',
                    transform: `translate(${x1}px, ${y1}px)`
                }}
            />
        </div>
    );
}

export default Drone