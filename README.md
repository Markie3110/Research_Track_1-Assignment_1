Research Track 1 - Assignment 1 Solution
================================
The following repository contains the solution to the first assignment for the Research Track 1 Course, found in the Robotics Masters Programme at the University of Genoa, Italy. The problem statement along with any necessary files can be found at *https://github.com/CarmineD8/python_simulator*. Within the linked repository is a simulator that is capable of depicting a differential drive robot and some boxes in an arena. The goal of the assignment is to program the robot with the help of some predefined functions such that it can detect all the boxes within the arena space, and move them to a single position. The position can be arbitary and it is for the programmer to decide how they want to carry out the execution.

Table of Contents
----------------------
1. [How to Install](https://github.com/Markie3110/Research_Track_1-Assignment_1/tree/master#how-to-install)
2. [How to run](https://github.com/Markie3110/Research_Track_1-Assignment_1/tree/master#how-to-run)
3. [Robot API](https://github.com/Markie3110/Research_Track_1-Assignment_1/tree/master#robot-api)
4. Code Explanation
5. Alternative Solution

How to Install
----------------------
To download the repsitory's contents to your local system you can do one of the following:

1. Using git from your local system
To download the repo using git simply go to your terminal and go to the directory you want to save the project in. Type the following command to clone the repository to your local folder:
```bash
$ git clone "https://github.com/Markie3110/Research_Track_1-Assignment_1"
```

2. Download the .zip from Github
In a browser go to the repository on Github and download the .zip file availabe in the code dropdown box found at the top right. Unzip the file to access the contents.

How to Run
----------------------
To run the solution go to robot-sim in your local system and type the following:
```bash
python3 run.py assignment.py
```

Robot API
---------

Although already explained in the *[Problem Statement Repo](https://github.com/CarmineD8/python_simulator)*, the explanation for the Robot API is repeated here given that the entire code is dependent on its functionalities. 

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

Code Explanation
----------------------
Test for pesudo
**FUNCTION** detect_boxes(UnplacedBoxesList, PlacedBoxesList)  
>    '''  
>	   A function designed to update a list keeping track of the boxes the robot has seen but not yet grabbed.  
>	   '''  
>	   **FOR** every Box visible to the robot **THEN**  
>		      Add code of Box to UnplacedBoxesList if not in UnplacedBoxesList and PlacedBoxesList  
>	   **ENDFOR**
>**ENDFUNCTION**
