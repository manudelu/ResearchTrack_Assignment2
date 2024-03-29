#! /usr/bin/env python3

"""
.. module:: NodeC
   :platform: Unix
   :synopsis: Python module for the second assignment of Research Track I course
   
.. moduleauthor:: Manuel Delucchi

A more detailed description of the node:

This node prints the robot speed and the distance from the desired target

Subsribes to:
	/pos_vel
	
"""

import rospy
import math
import time

from assignment_2_2022.msg import RobotMsg

freq = 1.0
last_t = 0

def callback_subscriber(msg):
	"""
	Function that calculates the distance between the robot and the goal and the speed of the robot
	
	*Args*: 
	*msg(RobotMsg)*: Contains the coordinates and velocity of the robot
	
	"""
	global freq, last_t
	# Period expressed in milliseconds [ms]
	period = (1.0/freq) * 1000
	# Get the current time in milliseconds from time()
	current_t = time.time() * 1000
	
	# If enough time is passed since the last time then print distance and velocity
	if current_t - last_t > period:
		# Get the desired position from the ROS parameter server
		des_pos_x = rospy.get_param("des_pos_x")
		des_pos_y = rospy.get_param("des_pos_y")

		# Calculate the distance between the current and the desired position
		distance = math.sqrt(pow(des_pos_x - msg.x, 2) + pow(des_pos_y - msg.y, 2))
			
		# Calculate the velocity   
		vel = math.sqrt(pow(msg.vel_x, 2) + pow(msg.vel_y, 2))
			
		# Print distance and velocity
		print("Distance to the goal: ", distance)
		print("Average speed: ", vel)  
		
		# Update last_t with current_t
		last_t = current_t

if __name__ == '__main__':
	
	# Init the Node
	rospy.init_node("NodeC")
	
	# Setting the rate of publishing chosen in launch file
	freq = rospy.get_param("freq")
	rate = rospy.Rate(freq)
	
	# Subscribe to the RobotMsg topic and pass the info to the callback function
	rospy.Subscriber('/pos_vel', RobotMsg, callback_subscriber)
	
	while not rospy.is_shutdown():
		rate.sleep()
	
	# Keep the node running
	rospy.spin()
	
