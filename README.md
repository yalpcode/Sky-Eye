# Sky Eye
<h1 align="center">Hello!<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h4 align="center">This is a neural network that recognizes flying objects, classifies them and plots their trajectory and the vector of their intended movement(using YOLOv11, for Ministry of Industry and Trade)</h4>

## Description
We have developed a website where the user can upload any video and then see selected and classified flying objects on it. The system will not just show the user where the plane, helicopter or drone is located, but will also track its movement by drawing a flight path, and even predict where it will fly next.

As a stack of technologies, we used:
- YOLOv11: A pre-trained neural network that recognizes and classifies objects in a video.
- OpenCV: a library for working with videos.
- FastAPI: a framework for creating a backend. 
- React: a framework for user interface development.

All components are combined in a Docker container, which makes our solution convenient to deploy and use.

The uniqueness of our solution lies in the fact that we not only select objects and assign them to a certain class, but also analyze their movement: we build a flight path and predict the direction of movement.

## Authors
- <a href="https://github.com/krup4" target="_blank">Krupnov Pavel</a> <br/>
- <a href="https://github.com/yalpcode" target="_blank">Erguchev Alexander</a><br/>
- <a href="https://github.com/D1ffic00lt" target="_blank">Filinov Dmitry</a><br/>
- <a href="https://github.com/limness" target="_blank">Tsyrkunov Andrew</a><br/>
- <a href="https://github.com/bigpurota" target="_blank">Tsember Andrew</a><br/>

## Installation
Clone this repository:
```
git clone https://github.com/yalpcode/droneAI
```
Go to it: 
```
cd droneAI
```
Run:
```
docker compose up
```
