from __future__ import print_function

import time
from timeit import default_timer as timer
from sr.robot import *

R  = Robot()

def detect_boxes(unplaced_boxes, placed_boxes):
    '''
    A function designed to update unplaced_boxes for any undetected boxes while the robot is moving.

    Args: 
    -> unplaced_boxes(list[int]): A list containing the codes of the unplaced boxes
    -> placed_boxes(list[int]): A list containing the codes of the placed boxes

    Return: None
    '''
    for box in R.see():
        if ((box.info.code not in unplaced_boxes) and (box.info.code not in placed_boxes)):
            unplaced_boxes.append(box.info.code)
    return 0


def scan_for_closest_box(speed, seconds, desired_angular_disp, unplaced_boxes, placed_boxes):
    '''
    A function that pans the robot left and right by a certain displacement to find the box closest to it.

    Args:
    -> speed (double): The speed of the wheels
	-> seconds (double): The time interval
    -> desired_angular_disp (double): The (approximate) angular displacement by which the robot should rotate about in both directions
    -> unplaced_boxes(list[int]): A list containing the codes of the unplaced boxes
    -> placed_boxes(list[int]): A list containing the codes of the placed boxes

    Return:
    -> min_code(int): The code of the box closest to the robot
    -> min_dist(double): The distance of the robot to the box closes to it
    -> min_rot_y(double): The anglular difference between the robot and the box closest to it
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
    A function that compares the distances of previously seen and currently visible boxes encountered during a single call of 
    the function scan_for_closest_box, and returns the code of the one closest to the robot.

    Args:
    -> i(int): A flag that denotes whether detect_closest_box is being called for the first time
    -> min_code(int): The code of the box that has been closest to the robot by far
    -> min_dist(double): The distance of the robot to the box assumed to be the closest
    -> min_rot_y(double): The angle between the robot and the box assumed to be the closest

    Return:
    -> i(int): A flag that denotes whether detect_closest_box was called for the first time
    -> min_code(int): The code of the box that has been closest to the robot by far
    -> min_dist(double): The distance of the robot to the box assumed to be the closest
    -> min_rot_y(double): The angle between the robot and the box assumed to be the closest
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
    A function that returns the distance and angle of a desired box from the robot.

    Args:
    -> target_box(int): The code of the box to be found

    Output:
    -> dist(double): The distance between the robot and the box
    -> rot_y(double): The angle between the robot and the box
    '''
    dist, rot_y = -1, -1 
    for box in R.see():
        if (box.info.code == target_box):
            dist = box.dist
            rot_y = box.rot_y
            break
    return dist, rot_y


def drive(speed, seconds):
    """
    Function for setting a linear velocity.
    
    Args: 
    -> speed (double): The speed of the wheels
	-> seconds (double): The time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    return 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity.
    
    Args:
    -> speed (double): The speed of the wheels
	-> seconds (double): The time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    return 0


def move_to_target(target_box, angle_threshold, distance_threshold):
    '''
    A function that finds and then moves the robot to a particular target box to within a certain angular and distance threshold.

    Args:
    -> target_box(int): The code of the box the robot should be moved to
    -> angle_threshold(double): The value by which the difference between the robots orientation and target point should not be exceeded
    -> distance_threshold(double): The minimum distance from the target box that the robot should move up to before it stops motion

    Return:
    -> 1: Denotes that the robot has reached the box
    -> -1: Denotes that the box could not be found
    '''
    actual_ang_disp, dist, rot_y = 0, -1, -1
    while (actual_ang_disp < 120.0):
        dist, rot_y = find_box(target_box)
        if (dist != -1 and rot_y != -1):
            break
        turn(15, 0.05)
        actual_ang_disp= actual_ang_disp + (15 * 0.05)
    if (dist == -1 and rot_y == -1):
        return -1
    while (dist >= distance_threshold):
        if (rot_y < (-angle_threshold)):
            turn(-15,0.01)
        elif (rot_y > angle_threshold):
            turn(15,0.01)
        else:
            drive(60,0.05)
        dist, rot_y = find_box(target_box)
        if (dist == -1 and rot_y == -1):
            desired_angular_disp = 30
            actual_angular_disp = 0
            while (actual_angular_disp < desired_angular_disp):
                turn(15, 0.02)
                dist, rot_y = find_box(target_box)
                if (dist != -1 and rot_y != -1):
                    break
                actual_angular_disp = actual_angular_disp + (15 * 0.05)
            actual_angular_disp = 0
            while (actual_angular_disp < desired_angular_disp*2):
                turn(-15, 0.02)
                dist, rot_y = find_box(target_box)
                if (dist != -1 and rot_y != -1):
                    break
                actual_angular_disp = actual_angular_disp + (15 * 0.05)
            actual_angular_disp = 0
            while (actual_angular_disp < desired_angular_disp):
                turn(15, 0.02)
                dist, rot_y = find_box(target_box)
                if (dist != -1 and rot_y != -1):
                    break
                actual_angular_disp = actual_angular_disp + (15 * 0.05)
    return 1


def main():
    '''
    The main function that controls the overall robot behaviour.

    Args: None

    Return: None
    '''
    unplaced_boxes = [] # Create a list codes of the unplaced box 
    placed_boxes = [] # Create a list of codes of the placed box 
    a_th = 2.0 # Threshold for the control of the orientation
    d_th = 0.4 # Threshold for the control of the linear distance
    prime_d_th = 0.53
    grabbed_box = 0 # Variable to depict the code of the box currently held by the robot

    # Scan for the closest box and mark it as the prime box to which we bring the other boxes
    min_code, min_dist, min_rot_y = scan_for_closest_box(15, 0.05, 12.0, unplaced_boxes, placed_boxes)
    unplaced_boxes.remove(min_code)
    placed_boxes.append(min_code)

    while (len(unplaced_boxes) != 0):
        # Take the first box in the undetected boxes list and move towards it
        for box in unplaced_boxes:
            status = move_to_target(box, a_th, d_th)
            if status == 1:
                # When the robot is near the box grab it
                R.grab()
                grabbed_box = box
                break
        # Find the prime box and move towards it
        move_to_target(min_code, a_th, prime_d_th)
        # When the robot is near the prime box release the target and back the robot up a bit
        R.release()
        prime_d_th = prime_d_th + 0.05
        placed_boxes.append(grabbed_box)
        unplaced_boxes.remove(grabbed_box)
        drive(-60, 0.5)
    else:
        print('Finished placing all the boxes at the target!')


main()
