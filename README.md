# Coztbote

<img align="right" src="https://i.imgur.com/oyCr3nq.png" width="200">

_Coztbote_ was a university project over a period of 3 weeks. The main purpouse was to deepen the students knowledge about robotics and graphical data analysis. Using Anki's robot _Cozmo_ we simulated a logistics system which involved autonomous driving and face detection techniques. In this project _Cozmo_ plays the role of the mailman delivering packages in a city. The packages are represented by the cubes that come with the _Cozmo_ robot. The lane system was build from white cardbard where as the lane tracks are made from black tape.

# Features
- Autonomous driving on a lane system by analyzing live camera data
  - Support for detecting crosses and curves in the road network
  - Scanning lane for signs to execute specified tasks (stop, turn, deliver ..)
  - Searching the lane system for the matching package recipient 
- Face detection using OpenCV to match packages to a persons face
  - Customized voice output on successful/unsuccessful package delivery
- Automatically return to the package station and process more packages upon successful delivery.
- Scalability
  - The project can be scaled for large lane systems with many crossings and endpoints

# Algorithms

## Lane Keeping

<img align="right" src="https://i.imgur.com/xgrFgMJ.png">

<img align="right" src="https://i.imgur.com/cEcTJhn.gif">

To ensure that the Cozmo robot can follow a line of any shape a correction value is computed. This is done by using the live image data from the _Cozmo_ camera. A still image is taken, binarized and segmented. The upper 1/3 of the frame only contains parts of the lane that are more then 20cm away from _Cozmo_ and therefore not relevant for the correction calculation.  
The lower 2/3 of the image are splitted into three equally sized sections. For each section the geographic center of the black pixels (the lane) is calculated. This gives us three points in total, one for each section. These points are used for the navigation of the robot. These navigation points are used hierarchically, meaning the point in the upper section is used first. In case of light reflections in the upper section the navigation points might not be calculated and the next navigation point one section down is used instead. This ensures a more reliable, less error-prone navigation. The actual correction to the left/right is calculated based on the distance from the navigation point to the section center.

## Crossing Detection

<img align="right" src="https://i.imgur.com/KCwtan8.png">

<img align="right" src="https://i.imgur.com/7aYsKJK.png">

To detect crossings in lane system, the camera frame is first cropped to a smaller section and then identified using pattern matching. The cropped section consists of less pixels an is therefore faster and in the processing stage. The crossing detection goes as follows:

1. Every 10th pixel row of the cropped gets extracted into an array
2. The array is compressed using the [Run-Length-Encoding](https://en.wikipedia.org/wiki/Run-length_encoding) algorithm.
3. Short pattern-changes (White-Black/Black-White) are classified as noise and get removed
4. Identical successive patterns are combined
5. The rarest patterns patterns are removed until only three patterns are left
6. The remaining three patterns can be used to identify every crossing type

These are all possible crossing patterns that _Cozmo_ can handle:

<img align="center" src="https://i.imgur.com/j9rSg5y.png">

## Lane-Sign Detection

<img align="right" src="https://i.imgur.com/4RQo78l.jpg">

To trigger additional behaviours during navigation _"street signs"_ were added. Black squares are placed symmetrical to the left and the right of the lane. Using OpenCV's conture detection these signs are detected and their size gets measured. 
<img align="right" src="https://i.imgur.com/8RauCOt.png" width="300">
One the signs reach a triggerline (orange) on the lower section of the frame, the signs are counted and based on their number a certain task is executed. By default the following sign-based tasks are supported:

- `2` Signs, `1` per Side: Start package station behaviour
- `4` Signs, `2` per Side: Start face matching process
- `6` Signs, `3` per Side: Cozmo turns 180 degrees

# Installation

## Requirements
### Requiremented Hardware

The following hardware is required to setup this project:

- Anki's Cozmo robot
- WLAN-ready Android or iOS device with the Cozmo App installed
  - USB Connection cable
- Computer running Windows or Linux
 
### Required Software

The following software is required to run this project:

- [Python3](https://www.python.org/) to run the main project
- [pipenv](https://pipenv.readthedocs.io/en/latest/) for the dependency installation. Alternativly `pip` can be used too.

### Required Materials

A test track with white ground and black lines for the lanes. It is recommended to have white barriers around the track to reduce the change of noise detections. During the project assignment the following track was used:

<img align="center" src="https://i.imgur.com/tCibXdc.jpg">

## Installation Procedure

To install and run this project on either windows or linx:
1. Clone repository
2. Navigate in the projects directory and install all dependencies with `pipenv install`
3. Connect Tablet with Cozoms WLAN Hotspot
  - For Android phones enable USB debugging
4. Connect phone/tablet with the computer and start the Cozmo App
5. Enable SDK Mode in the Cozmo App
6. Place cozmo on the test track and start the project on your computer by executing `python core.py`

# References

The documentation for this project can be found [here](https://wiki.h-da.de/fbi/west/index.php/R2M2_-_Gruppe_4)
