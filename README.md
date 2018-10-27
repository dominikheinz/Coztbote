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
The lower 2/3 of the image are splitted into three equally sized sections. For each section the geographic center of the black pixels (the lane) is calculated. This gives us three points in total, one for each section. These points are used for the navigation of the robot.



# Installation

# Requirements

# References

The documentation for this project can be found [here](https://wiki.h-da.de/fbi/west/index.php/R2M2_-_Gruppe_4)
