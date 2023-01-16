#!/usr/bin/python

import rospy
from std_msgs.msg import Header
from nav_msgs.msg import Odometry
from gazebo_msgs.srv import GetModelState, GetModelStateRequest
from tf import TransformBroadcaster

rospy.init_node('odom_pub')

odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
tb = TransformBroadcaster()

rospy.wait_for_service('/gazebo/get_model_state')

get_model_srv = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

odom = Odometry()

header = Header()
header.frame_id = 'odom'

model = GetModelStateRequest()
model.model_name = 'mobility_base'

r = rospy.Rate(2)

while not rospy.is_shutdown():

    result = get_model_srv(model)

    odom.pose.pose = result.pose
    odom.twist.twist = result.twist

    header.stamp = rospy.Time.now()
    odom.header = header
    odom.child_frame_id = 'base_footprint'
    odom_pub.publish(odom)
    position = (result.pose.position.x, result.pose.position.y, result.pose.position.z)
    orientation = (result.pose.orientation.x, result.pose.orientation.y, result.pose.orientation.z, result.pose.orientation.w)
    tb.sendTransform(position, orientation, rospy.Time.now(), 'base_footprint', '/odom')

    r.sleep()




