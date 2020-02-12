#!/usr/bin/env python

import rospy
import smach
import smach_ros
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State
from sensor_msgs.msg import BatteryState
from mavros_msgs.msg import Mavlink


# precland_msg =  Mavlink(
#     header=header,
#     is_valid=True,
#     len=len(mavmsg.get_payload()),
#     seq=mavmsg.get_seq(),
#     sysid=mavmsg.get_srcSystem(),
#     compid=mavmsg.get_srcComponent(),
#     msgid=mavmsg.get_msgId(),
#     checksum=mavmsg.get_crc(),
#     payload64=convert_to_payload64(mavmsg.get_payload())
#     )

TOL = 0.5
MAX_TIME_DISARM = 15
CONFIG = {"mavros_local_position_pub" : "/mavros/setpoint_position/local",
                "mavros_velocity_pub" : "/mavros/setpoint_velocity/cmd_vel",
                "mavros_local_atual" : "/mavros/local_position/pose",
                "mavros_state_sub" : "/mavros/state",
                "mavros_arm" : "/mavros/cmd/arming",
                "mavros_set_mode" : "/mavros/set_mode",
                "mavros_battery_sub" : "/mavros/battery"}
class MAV:
    
                #"bebop_velocity_pub" : "/bebop/setpoint_velocity/cmd_vel"}

    def __init__(self, mav_name, mav_type="mavros"):
        #rospy.init_node("MAV_" + mav_name)
        self.rate = rospy.Rate(20)

        self.drone_pose = PoseStamped()
        self.goal_pose = PoseStamped()
        self.goal_vel = TwistStamped()
        self.drone_state = State()
        self.battery = BatteryState()
        ############## Publishers ###############
        self.local_position_pub = rospy.Publisher(CONFIG[mav_type + "_local_position_pub"], PoseStamped, queue_size = 20)
        self.velocity_pub = rospy.Publisher(CONFIG[mav_type + "_velocity_pub"],  TwistStamped, queue_size=5)

        self.mavlink_pub = rospy.Publisher('/mavlink/to', Mavlink, queue_size=1)
        ########## Subscribers ##################
        self.local_atual = rospy.Subscriber(CONFIG[mav_type + "_local_atual"], PoseStamped, self.local_callback)
        self.state_sub = rospy.Subscriber(CONFIG[mav_type + "_state_sub"], State, self.state_callback)
        self.battery_sub = rospy.Subscriber("/mavros/battery", BatteryState, self.battery_callback)
        ############# Services ##################
        self.arm = rospy.ServiceProxy(CONFIG[mav_type + "_arm"], mavros_msgs.srv.CommandBool)
        self.set_mode = rospy.ServiceProxy(CONFIG[mav_type + "_set_mode"], mavros_msgs.srv.SetMode)




    ###### Callback Functions ##########
    def state_callback(self, state_data):
        self.drone_state = state_data

    def battery_callback(self, bat_data):
        self.battery = bat_data

    def local_callback(self, local):
        self.drone_pose.pose.position.x = local.pose.position.x
        self.drone_pose.pose.position.y = local.pose.position.y
        self.drone_pose.pose.position.z = local.pose.position.z
    ####### Set Position and Velocity ################
    def set_position(self, x, y, z):
        self.goal_pose.pose.position.x = x
        self.goal_pose.pose.position.y = y
        self.goal_pose.pose.position.z = z
        self.local_position_pub.publish(self.goal_pose)
        self.rate.sleep()

    def set_vel(self, x, y, z, roll=0, pitch=0, yaw=0):
        self.goal_vel.twist.linear.x = x
        self.goal_vel.twist.linear.y = y
        self.goal_vel.twist.linear.z = z

        self.goal_vel.twist.angular.x = roll
        self.goal_vel.twist.angular.y = pitch
        self.goal_vel.twist.angular.z = yaw
        self.velocity_pub.publish(self.goal_vel)

    def chegou(self):
        if (abs(self.goal_pose.pose.position.x - self.drone_pose.pose.position.x) < TOL) and (abs(self.goal_pose.pose.position.y - self.drone_pose.pose.position.y) < TOL) and (abs(self.goal_pose.pose.position.z - self.drone_pose.pose.position.z) < TOL):
            return True
        else:
            return False

    def takeoff(self, height):
        velocity = 1
        part = velocity/60.0
        rospy.loginfo("OFFBOARD MODE SETUP")
        while not self.drone_state.armed:
            rospy.logwarn("ARMING DRONE")
            self.set_position(0,0,0)
            self.arm(True)
            self.rate.sleep()
        
            if self.drone_state != "OFFBOARD":
                rospy.loginfo("SETTING OFFBOARD FLIGHT MODE")
                self.set_mode(custom_mode = "OFFBOARD")

        t=0
        t += 150*part
        while not rospy.is_shutdown() and self.drone_pose.pose.position.z <= height:
            rospy.loginfo('Executing State TAKEOFF')

            if self.drone_state != "OFFBOARD":
                rospy.loginfo("SETTING OFFBOARD FLIGHT MODE")
                self.set_mode(custom_mode = "OFFBOARD")

            if not self.drone_state.armed:
                rospy.logwarn("ARMING DRONE")
                self.arm(True)
            else:
                rospy.loginfo("DRONE ARMED")

            if t < height:
                rospy.logwarn('TAKING OFF AT ' + str(velocity) + ' m/s')
                self.set_position(0, 0, t)
                t += part
            else:
                self.set_position(0, 0, height)

            rospy.loginfo('Position: (' + str(self.drone_pose.pose.position.x) + ', ' + str(self.drone_pose.pose.position.y) + ', '+ str(self.drone_pose.pose.position.z) + ')')
            self.rate.sleep()

        self.set_position(0, 0, height)

        return "done"


    def RTL(self):
        velocity = 0.3
        ds = velocity/60.0

        self.rate.sleep()
        height = self.drone_pose.pose.position.z
        rospy.loginfo('Position: (' + str(self.drone_pose.pose.position.x) + ', ' + str(self.drone_pose.pose.position.y) + ', ' + str(self.drone_pose.pose.position.z) + ')')

        self.set_position(0,0,height)
        self.rate.sleep()
        rospy.loginfo('Position: (' + str(self.drone_pose.pose.position.x) + ', ' + str(self.drone_pose.pose.position.y) + ', ' + str(self.drone_pose.pose.position.z) + ')')
        rospy.loginfo('Goal Position: (' + str(self.goal_pose.pose.position.x) + ', ' + str(self.goal_pose.pose.position.y) + ', ' + str(self.goal_pose.pose.position.z) + ')')


        while not self.chegou():
            rospy.loginfo('Executing State RTL')
            rospy.loginfo("STARING HOME")
            self.set_position(0,0,height)
            self.rate.sleep()

        t=0
        self.set_position(0,0,height-ds)
        self.rate.sleep()

        init_time = rospy.get_rostime().secs
        while not (self.drone_pose.pose.position.z < -0.1) and rospy.get_rostime().secs - init_time < (height/velocity)*1.3: #20% tolerance in time
            rospy.loginfo('Executing State RTL')

            rospy.loginfo('Height: ' + str(abs(self.drone_pose.pose.position.z)))
            ################# Velocity Control #################
            self.set_vel(0, 0, -velocity, 0, 0, 0)
            #################### Position Control ##############
            # if not self.chegou():
            #     rospy.logwarn ('LANDING AT ' + str(velocity) + 'm/s')
            #     if t <= height:
            #         t += ds
            #     self.set_position(0,0,height - t)
            #     self.rate.sleep()
            #
            # else:
            #     if t <= height:
            #         t += ds
            #         self.set_position(0,0,height - t)
            #     else:
            #         self.set_position(0,0,0)
            #     self.rate.sleep()
            ####################################################

        rospy.logwarn("DESARMANDO DRONE ")
        self.arm(False)
        return "succeeded"

    def precision_landing(self):
          if self.drone_state != "AUTO.PRECLAND":
              for count in range(3):
                rospy.loginfo("SETTING PRECISION LANDING FLIGHT MODE")
                self.set_mode(custom_mode = "AUTO.PRECLAND")
                rospy.loginfo(self.drone_state)

    def land(self):
        velocity = 0.3
        height = self.drone_pose.pose.position.z
        init_time = rospy.get_rostime().secs
        while not (self.drone_pose.pose.position.z < -0.1) and rospy.get_rostime().secs - init_time < (height/velocity)*1.2: #20% tolerance in time
            rospy.loginfo('Landing!')
            rospy.loginfo('Height: ' + str(abs(self.drone_pose.pose.position.z)))
            ################# Velocity Control #################
            self.set_vel(0, 0, -0.3, 0, 0, 0)

    def _disarm(self):
        rospy.logwarn("DISARM MAV ")
        if drone_pose.pose.position.z < TOL:
            for i in range(3):
                rospy.loginfo('Drone height' + str(drone_pose.pose.position.z))
                self.arm(False)
        else:
            rospy.logwarn("Altitude too high for disarming!")
            self.land()
            self.arm(False)

if __name__ == '__main__':
    mav = MAV("1") #MAV name
    mav.takeoff(3)
    mav.RTL()
