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
The solution to the assignment was broken down into steps. Actions that are carried out repeatedly were coded into several functions that are called from a main function that controls the overall robot behaviour. In general the code works by first having the robot turn clockwise and counterclockwise to note down the codes of all boxes visible to it at the moment in its internal memory, as well as to mark the box closest to it. The position of this box, which we shall call the prime box, will be the one we bring all of the other boxes to. After finding the prime, the robot searches for every box stored in its memory and transports them to the prime. Once the robot places a box at the target, the robot updates its internal memory to reflect this change. The robot has also been programmed to keep on looking for new boxes it may have missed in the intial search, as it carries out its tasks. If any such box is detected, it is added to the list. Once all the boxes the robot has come across have been transported to the prime, the program ends.  
Given below is the pseudocode for the various functions:  


### detect_boxes ###
<pre>
<b>FUNCTION</b> detect_boxes(UnplacedBoxesList, PlacedBoxesList):
	'''
	A function designed to update a list keeping track of the boxes the robot has seen but not yet grabbed.
	'''
	<b>FOR</b> every Box visible to the robot <b>THEN</b>
		Add code of Box to UnplacedBoxesList if not in UnplacedBoxesList and PlacedBoxesList
	<b>ENDFOR</b>
<b>ENDFUNCTION</b>
</pre>


### scan_for_closest_box ###
<pre>
	<b>FUNCTION</b> scan_for_closest_box(DesiredAngularDisp, UnplacedBoxesList, PlacedBoxesList)
	 '''
	 A function that pans the robot left and right by a certain displacement to find the box closest to it.
	 '''
	 <b>SET</b> Flag to 0
	 <b>SET</b> MinimumCode to -1
	 <b>SET</b> MinimumDist to 0
	 <b>SET</b> MinimumRot to 0
	 <b>CALL</b> detect_closest_box() to rotate the robot left and find the closest box
	 <b>SET</b> Flag to 1
	 <b>SET</b> MinimumCode, MinimumDist, MinimumRot to the code, distance and rotation of the closest box
	 <b>CALL</b> detect_closest_box() to rotate the robot right and compare the current closest box distance with distances of newly detected boxes
	 <b>SET</b> MinimumCode, MinimumDist, MinimumRot to the code, distance and rotation of the closest box
	 <b>CALL</b> detect_closest_box() to return the robot to a neutral position
<b>RETURN</b> MinimumCode
</pre>



### detect_closest_box ###
<pre>
	<b>FUNCTION</b> detect_closest_box(Flag, MinimumCode, MinimumDist, MinimumRot, Speed, Seconds, DesiredAngularDisp, UnplacedBoxesList, PlacedBoxesList)
	'''
	A function that rotates the robot  in one direction by a certain angular displacement and compares the distances of the various boxes it sees to find the closest one.
	'''
	<b>SET</b> ActualAngularDisp to 0
	<b>WHILE</b> ActualAngularDisp is less than DesiredAngularDisp <b>THEN</b>
		<b>FOR</b> every Box visible to the robot <b>THEN</b>
			<b>IF</b> Flag is 0 <b>THEN</b>
				Set the MinimumCode, MinimumDist, MinimumRot to the code, dist and rot of the box currently visible
			<b>ENDIF</b>
			<b>IF</b> distance of Box is less than distance of the box currently visible <b>THEN</b>:
				Set the MinimumCode, MinimumDist, MinimumRot to the code, dist and rot of the box currently visible
			<b>ENDIF</b>
		<b>ENDFOR</b>
		<b>CALL</b> turn() to rotate the robot with a certain speed for a certain number of seconds
		<b>CALL</b> detect_boxes() to find previously unseen boxes
		<b>COMPUTE</b> ActualAngularDisplacement as ActualAngularSpeed + (Seconds * Absolute value of Speed)
	<b>ENDWHILE</b>
<b>RETURN</b> Flag, MinimumCode, MinimumDist, MinimumRot
</pre>


### drive ###
<pre>
	FUNCTION drive(Speed, Seconds)
	'''
	Function for setting a linear velocity.
	'''
	Set the robots left and right motors velocity to Speed
	Wait for duration Seconds
	Set the robots left and right motors velocity to 0
ENDFUNCTION
</pre>



### turn ###
<pre>
	FUNCTION turn(Speed, Seconds)
	'''
	Function for setting a linear velocity.
	'''
	Set the robots left velocity to Speed
	Set the robots right motors velocity to -Speed
	Wait for duration Seconds
	Set the robots left and right motors velocity to 0
ENDFUNCTION
</pre>


### find_box ###
<pre>
	FUNCTION find_box (TargetBox, Speed, Seconds, DesiredAngularDisp)
	'''
	A function that looks for the desired box by rotating the robot with an angular displacement 
	as a limit and returning its distance and angle from the robot if found.
	'''
	SET ActualAngularDisp to 0
	SET Found to 0
	Set Dist to 0
	Set RotY to 0
	WHILE ActualAngularDisp is less than DesiredAngularDisp
		FOR every Box visible to the robot:
			IF code of Box is TargetBox THEN
				SET Dist, RotY to distance, rotation of the box currently visible
				SET Found as 1
				BREAK for loop
			ENDIF
		ENDFOR
		IF Found is 1 THEN
			BREAK while loop
		ENDIF
	 	CALL turn to turn the robot with a certain speed for a certain number of seconds
		COMPUTE ActualAngularDisp as ActualAngularDisp + (Speed * Seconds) 
	ENDWHILE
RETURN Found, Dist, RotY
</pre>


### move_to_target ###
FUNCTION move_to_target(TargetBox, AngleThreshold, DistanceThreshold, UnplacedBoxes, PlacedBoxes)
	'''
	A function that finds and then moves the robot to a particular target box to within a certain angular and distance threshold.
	'''
	DECLARE Distance
	DECLARE Rotation
	CALL find_box to point the robot to the direction of TargetBox and to SET Distance and Rotation to the distance and rotation of TargetBox
	IF FOUND is 0 THEN:
		RETURN -1
	ENDIF
	WHILE Distance is greater than DistanceThreshold
		IF Rotation is less than -AngleThreshold THEN
			CALL turn to turn the robot clockwise
			CALL detect_boxes to find previously unseen boxes 
		ELIF Rotation is greater than AngleThreshold THEN:
			CALL turn to turn the robot counterclockwise
			CALL detect_boxes to find previously unseen boxes
		ELSE:
			CALL drive to move the robot forward 
			CALL detect_boxes to find previously unseen boxes
		ENDIF
		CALL find_box to point the robot to the direction of TargetBox and to SET Distance and Rotation to the distance and rotation of TargetBox
		IF Found is 0 THEN
			CALL find_box to pan the robot clockwise till a certain displacement and find TargetBox
		ENDIF
		IF Found is 0 THEN
			CALL find_box to pan the robot counterclockwise till a certain displacement and find TargetBox
		ENDIF
		IF Found is 0 THEN
			CALL find_box to return the robot to its neutral position
		ENDIF
	ENDWHILE
RETURN 1


### main ###
<pre>
	FUNCTION main
	DECLARE UnplacedBoxesList
	DECLARE PlacedBoxesList
	SET AngularThreshold to 2
	SET DistanceThreshold to 0.4
	SET PlacementThreshold to 0.53
	SET GrabbedBox to 0

	CALL scan_for_closest_box to find the boxes near the robot by panning it left and right and adding them to UnplacedBoxesList
	SET MinCode as code of the box closest to the robot 
	IF MinCode is -1 THEN:
		Exit function as no boxes visible
	ENDIF
	MOVE MinCode to PlacedBoxesList
	REMOVE MinCode from UnplacedBoxesList
	
	WHILE UnplacedBoxesList is not empty 
		FOR every Box in UnplacedBoxesList
			CALL move_to_target to move the robot to the location of Box
			IF robot at Box location THEN
				Grab the box
				SET GrabbedBox as code of Box
				BREAK for loop
			ELIF Box not visible to the robot THEN
				MOVE Box to the back of UnplacedBoxesList
			ENDIF
		ENDFOR
		CALL move_to_target to move the robot to the location of box with code MinCode
		Release the grabbed box
		COMPUTE PlacementThreshold as SUM of PlacementThreshold and 0.05
		REMOVE GrabbedBox from UnplacedBoxesList
		ADD GrabbedBox to PlacedBoxesList
	ENDWHILE
ENDFUNCTION
</pre>
