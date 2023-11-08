from __future__ import print_function

import time
from timeit import default_timer as timer
from sr.robot import *

R  = Robot()

def detect_boxes(unplaced_boxes, placed_boxes):
    '''
    A function designed to update unplaced_boxes for any undetected boxes while the robot is moving.

    Args: 
    -> unplaced_boxes(int): A list containing the codes of the unplaced boxes
    -> placed_boxes(int): A list containing the codes of the placed boxes

    Output: None
    '''
    for box in R.see():
        if ((box.info.code not in unplaced_boxes) and (box.info.code not in placed_boxes)):
            unplaced_boxes.append(box.info.code)
    return 0

def scan_for_closest_box(speed, seconds, desired_angular_disp, unplaced_boxes, placed_boxes):
    '''
    Angular_velocity= ang-disp/time
    '''
    actual_angular_disp = 0
    i, min_code, min_dist, min_rot_y = 0, 0, 0, 0
    while (actual_angular_disp < desired_angular_disp):
        turn(speed, seconds)
        i, min_code, min_dist, min_rot_y = detect_closest_box(i, min_code, min_dist, min_rot_y)
        detect_boxes(unplaced_boxes, placed_boxes)
        actual_angular_disp = actual_angular_disp + (speed * seconds)
    actual_angular_disp = 0
    while (actual_angular_disp < (desired_angular_disp*2)):
        turn(-speed, seconds)
        i, min_code, min_dist, min_rot_y = detect_closest_box(i, min_code, min_dist, min_rot_y)
        detect_boxes(unplaced_boxes, placed_boxes)
        actual_angular_disp = actual_angular_disp + (speed * seconds)
    actual_angular_disp = 0
    while (actual_angular_disp < desired_angular_disp):
        turn(speed, seconds)
        i, min_code, min_dist, min_rot_y = detect_closest_box(i, min_code, min_dist, min_rot_y)
        detect_boxes(unplaced_boxes, placed_boxes)
        actual_angular_disp = actual_angular_disp + (speed * seconds)
    return min_code, min_dist, min_rot_y

def detect_closest_box(i, min_code, min_dist, min_rot_y):
    '''
    '''
    for box in R.see():
        if (i == 0):
            min_code = box.info.code
            min_dist = box.dist
            min_rot_y = box.rot_y
            i = i + 1
            continue
        if (box.dist <= min_dist):
            min_code = box.info.code
            min_dist = box.dist
            min_rot_y = box.rot_y
    return i, min_code, min_dist, min_rot_y

def find_box(target_box):
    '''
    '''
    dist, rot_y = -1, -1
    for box in R.see():
        if (box.info.code == target_box):
            dist = box.dist
            rot_y = box.rot_y
    return dist, rot_y

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

def move_to_target(target_box, angle_threshold, distance_threshold):
    '''
    '''
    dist, rot_y = find_box(target_box)
    if (dist == -1 and rot_y == -1):
        exit(-1)
    while (dist >= distance_threshold):
        if (rot_y < (-angle_threshold)):
            turn(-15,0.05)
        elif (rot_y > angle_threshold):
            turn(15,0.05)
        else:
            drive(60,0.05)
    dist, rot_y = find_box()

def main():
    unplaced_boxes = [] # Create a list codes of the unplaced box 
    placed_boxes = [] # Create a list of codes of the placed box 
    a_th = 2.0 # Threshold for the control of the orientation
    d_th = 0.4 # Threshold for the control of the linear distance

    # Scan for the closest box and mark it as the prime box to which we bring the other boxes
    min_code, min_dist, min_rot_y = scan_for_closest_box(15, 0.05, 12.0, unplaced_boxes, placed_boxes)
    unplaced_boxes.remove(min_code)
    placed_boxes.append(min_code)

    # Take the first box in the undetected boxes list and move towards it
    # When the robot is near the box grab it
    # Find the prime box and move towards it
    # When the robot is near the prime box release the target and back the robot up a bit

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

# Exceptions: The robot does not detect any boxes

main()

'''
while 1:
    pass
'''