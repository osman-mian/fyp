#!/usr/bin/env python
import rospy
import roslib; roslib.load_manifest('ardrone_python')
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist, Vector3

if __name__ == '__main__':
    rospy.init_node('example_node', anonymous=True)
    
    # publish commands (send to quadrotor)
    pub_velocity = rospy.Publisher('/cmd_vel', Twist)
    pub_takeoff = rospy.Publisher('/ardrone/takeoff', Empty)
    pub_land = rospy.Publisher('/ardrone/land', Empty)
    pub_reset = rospy.Publisher('/ardrone/reset', Empty)
    
    print("ready!")
    rospy.sleep(1.0)
    
    print("takeoff..")
    pub_takeoff.publish(Empty())
    rospy.sleep(5.0)

    speed=0.5
    
    interval = 1;
    x=0
    
    while x != 8:
        print("Select an option\n")
        print("1: Move Forward\n")
        print("2: Move Backwards\n")
        print("3: Strafe Left\n")
        print("4: Strafe Right\n")
        print("5: Rise Up\n")
        print("6: Come Down\n")
        print("7: Set Interval\n")
        print("8: Land\n")
    
        x = int(input("Enter your command: "))
    
        if x==1:
        	print("Move Forward")
        	pub_velocity.publish(Twist(Vector3(speed,0,0),Vector3(0,0,0)))
        	rospy.sleep(interval)
        	pub_velocity.publish(Twist(Vector3(0.0,0,0),Vector3(0,0,0)))
        elif x==2:
        	print("Going Back")
        	pub_velocity.publish(Twist(Vector3(-speed,0,0),Vector3(0,0,0)))
        	rospy.sleep(interval)
        	pub_velocity.publish(Twist(Vector3(0.0,0,0),Vector3(0,0,0)))
        elif x==3:
        	print("Strafe Left..")
        	pub_velocity.publish(Twist(Vector3(0.0,speed,0),Vector3(0,0,0)))
        	rospy.sleep(interval)
        	pub_velocity.publish(Twist(Vector3(0.0,0,0),Vector3(0,0,0)))
        elif x==4:
        	print("Strafe Right..")
        	pub_velocity.publish(Twist(Vector3(0.0,-speed,0),Vector3(0,0,0)))
        	rospy.sleep(interval)
        	pub_velocity.publish(Twist(Vector3(0.0,0,0),Vector3(0,0,0)))
        elif x==5:
        	print("Going Up")
        	pub_velocity.publish(Twist(Vector3(0.0,0,speed),Vector3(0,0,0)))
        	rospy.sleep(interval)
        	pub_velocity.publish(Twist(Vector3(0.0,0,0),Vector3(0,0,0)))
        elif x==6:
        	print("Going Down")
        	pub_velocity.publish(Twist(Vector3(0.0,0,-speed),Vector3(0,0,0)))
        	rospy.sleep(interval)
        	pub_velocity.publish(Twist(Vector3(0.0,0,0),Vector3(0,0,0)))
        elif x==7:
           interval = int(input("Enter execution duration: "))



    print("stop..")
    pub_velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,0)))
    rospy.sleep(3.0)
    
    print("land..")
    pub_land.publish(Empty())
    
    print("done!")
