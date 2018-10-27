# Coztbote


<img align="right" src="https://i.imgur.com/oyCr3nq.png" width="200">
_Coztbote_ was a university project over a period of 3 weeks. The main purpouse was to deepen the students knowledge about robotics and graphical data analysis. Using Anki's robot _Cozmo_ we simulated a logistics system which involved autonomous driving and face detection techniques. In this project _Cozmo_ plays the role of the mailman delivering packages in a city.


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

The documentation for this project can be found [here](https://wiki.h-da.de/fbi/west/index.php/R2M2_-_Gruppe_4)
