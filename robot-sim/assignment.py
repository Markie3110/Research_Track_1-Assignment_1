from __future__ import print_function

import time
from sr.robot import *

R = SimRobot()

def detect_tokens(unplaced_boxes, placed_boxes):
    '''
    A function designed to update unplaced_boxes for any undetected tokens while the robot is moving.

    Args: 
    -> unplaced_boxes(int): A list containing the codes of the unplaced boxes
    -> placed_boxes(int): A list containing the codes of the placed boxes

    Output: None
    '''
    for token in R.see():
        if ((token.info.code not in unplaced_boxes) and (token.info.code not in placed_boxes)):
            unplaced_boxes.append(token.info.code)
    return 0

def scan(speed, seconds):
    '''
    '''
    turn(speed, seconds)
    detect_closest_token()
    turn(-speed, seconds*2)
    detect_closest_token
    turn(speed, seconds)
    time.sleep(seconds)
    return 0

def detect_closest_token(min_code, min_dist, min_rot_y):
    '''
    '''
    i = 0
    for token in R.see():
        if (i == 0):
            min_code = token.info.code
            min_dist = token.dist
            min_rot_y = token.rot_y
            i = i + 1
            continue
        if (token.dist <= min_dist):
            min_code = token.index.code
            min_dist = token.dist
            min_rot_y = token.rot_y_
    return 0

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    return 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    return 0


def main():
    unplaced_boxes = [] # Create a list of unplaced token codes
    placed_boxes = [] # Create a list of placed token codes
    min_code, min_dist, min_rot_y = 0, 0, 0 
# The robot is continously scaning while moving for any new undetected tokens

# Have the robot pan left with a certain speed for a certain number of seconds to detect new boxes and their distances
# Have the robot pan right as before to detect new tokens and distances

# Find the token with the closest position and mark it as the prime token
# Place the prime token code in the placed token list

# Extract the tokens the robot can see
# Take the first token 
# -> If the length of the list is not 0 and the token is not in placed token
# -> Get its distance and angle

# Move the robot to the target tokens position
# Grab the token
# Rotate the robot counterclockwise until it finds the prime token
# Get the prime tokens position and angle
# Move the robot to the prime tokens position within a threshold

# Release the token and have the robot back up by a certain distance
# Move the token code to the placed token list
# Check if unplaced token list is empty
# -> Yes then exit the program and print an exit message
# -> No, repeat the program

while 1:
    pass
'''
1 - 2
2- 4
3- 6
[1, 2, 3]
[]
[2, 4, 6]
-----------
[2, 3]
[1]

'''