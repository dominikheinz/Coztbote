<script src="//yihui.name/js/math-code.js"></script>
<!-- Just one possible MathJax CDN below. You may use others. -->
<script async
  src="//mathjax.rstudio.com/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

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

To ensure that the Cozmo robot can follow a line of any shape a correction value is computed. This is done by using the live image data from the _Cozmo_ camera. A still image is taken, binarized and segmented. The lower `$\frac{2}{3}$` of the image

# Installation

# Requirements

# References

The documentation for this project can be found [here](https://wiki.h-da.de/fbi/west/index.php/R2M2_-_Gruppe_4)
