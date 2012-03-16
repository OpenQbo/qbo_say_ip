#!/usr/bin/python
##############################################################################
# This node makes the robot saying its current IP.
# 
# -> Publishers:     None
# 
# -> Subscribers:    listen/en_sayIP (type: qbo_listen.msg/Listened)                    
#                
# -> Services:       /Qbo/festivalSay (type: qbo_talk.srv/Text2Speach)
#                    /pluginsystem    (type: qbo_system_info.srv/AskInfo)
#
#
##############################################################################
import roslib; roslib.load_manifest('qbo_say_ip')
import rospy
from std_msgs.msg import String
from qbo_listen.msg import Listened
from qbo_system_info.srv import AskInfo
from qbo_talk.srv import Text2Speach

#
# Once the user ask about the robot's IP, we call the pluginsystem service and extract the
# each IP for each possible connection (wlan, eth, etc).
#
# Input:
#        None
#            
# Output:
#        None
#
def sayIP():

  
    rospy.wait_for_service("/pluginsystem");
    
    service_pluginsystem = rospy.ServiceProxy('/pluginsystem', AskInfo)
    
    
    print "uoo uooo"
    info = service_pluginsystem("netconf")
        
    rospy.loginfo(" IP  "+str(info.info))
    ip = str(info.info)
    ip = ip.replace("."," dot ")
        
    ip = ip.replace("eth","ethernet number ")
    ip = ip.replace("wlan","wifi number ")
        
    lines = ip.split("\n")
    print "--"+str(lines)
    for i in range(0,len(lines)):
        words = lines[i].split(" ")
    	if len(words)>=4: # four because the minimun string is "wifi number #"
    	    sentence = str(words[0])+" "+str(words[1])+" "+str(words[2])+"."+str(words[3:])
    	    sentence = sentence.replace("[","")
            sentence = sentence.replace("]","")
            sentence = sentence.replace("'","")
            sentence = sentence.replace(",","")
            print "about to say "+ sentence
            say(sentence)

#
# This function makes the robot to say whatever is given as an input
#
# Input:
#        sentence:    the string you want to be said
#            
# Output:
#        None
#
def say(sentence):
    rospy.wait_for_service("/Qbo/festivalSay")
    festival = rospy.ServiceProxy("/Qbo/festivalSay", Text2Speach  )
    
    festival(sentence)


def init():
    rospy.init_node('qbo_say_ip')    
    rospy.loginfo('QBO sayIP Node launched')    
    sayIP() 


if __name__== "__main__":
    try:
        init()
    except rospy.ROSInterruptException: pass


