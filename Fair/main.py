import controller as pd
import rospy
import roslib
import roslib; roslib.load_manifest('ardrone_python')

from ardrone_autonomy.msg import Navdata
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Empty
import numpy as np
from Queue import Queue

import pose_matrix as poses
import average_window

################################################
t=0
code=pd.UserCode()


#ORIENTATION
roll_mat = np.array([[1,0,0], [0,1,0],[0,0,1]])
pitch_mat = np.array([[1,0,0], [0,1,0],[0,0,1]])
yaw_mat = np.array([[1,0,0], [0,1,0],[0,0,1]])
###############################################


#start state
st=pd.State()
st.position = np.array([[0],[0],[0]])
st.velocity =  np.array([[0],[0],[0]])


position_local = np.array([[0],[0],[0]])


#target state
target=pd.State()
target.position = np.array([[-40],[0],[0]])
target.velocity =  np.array([[0],[0],[0]])


##############################################

pub_velocity = rospy.Publisher('/cmd_vel', Twist)
pub_takeoff = rospy.Publisher('/ardrone/takeoff', Empty)
pub_land = rospy.Publisher('/ardrone/land', Empty)
pub_reset = rospy.Publisher('/ardrone/reset', Empty)


window=5
v_q = Queue(window)
############################################

def callback(navdata):
	global t
	global st
	global pub_velocity
	global code
	global position_local
	global target
	global v_q
	#compute time since last call
	t2=t
	t = navdata.header.stamp.to_sec()
	dt= t-t2

	if v_q.full():

		v_q.get()
		v_q.put(np.array([[navdata.vx],[navdata.vy],[navdata.vz]]))

		roll_mat = poses.calculate_roll_pose(navdata.rotX);
		pitch_mat = poses.calculate_pitch_pose(navdata.rotY);
		yaw_mat = poses.calculate_yaw_pose(navdata.rotZ);
	
		pose=np.dot(np.dot(roll_mat,pitch_mat),yaw_mat);

		#get local distance co-ordinates
		position_local= dt *  average_window.getAverage(v_q,window) #np.array([[navdata.vx],[navdata.vy],[navdata.vz]])
		#print(st.position)
	
		st.position = st.position + (np.dot(pose,position_local))
		st.velocity = np.dot(pose,average_window.getAverage(v_q,window))

		#print	st.position
		#print "-************-\n"
	#	print pose
	

	

		#compute PD
		u =	code.compute_control_command(st,target);
	
	
		#reconvert to local
	
		local_command= np.dot(pose.T,u)
	

		#print(dt)
		print(local_command)
		#cmdvel.publish(local_command);

		print("--------------")
	else:
		v_q.put(np.array([[navdata.vx],[navdata.vy],[navdata.vz]]))

	
########################################	

def main():

	rospy.init_node('example_node', anonymous=True)
	rospy.Subscriber("/ardrone/navdata", Navdata, callback)

	rospy.spin()
	print("Fine!")

main()
