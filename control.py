import os
from math import cos,sin,pi, sqrt, tan
import sched, time
import pypot.dynamixel
import time

"""s = sched.scheduler(time.time, time.sleep)
vD=0 #Vitesse roue gauche
vG=0 #vitesse roue droite
vL=0 #Vitesse lineaire en m/s
vA=0 #Vitesse angulaire en rad/s
xM=0
yM=0
thetaM=0
#xR,yR,thetaR=0
rayonRoue=0.025
distance2Roues=0.08"""

def convert_rpm_to_rads(rpm_wheelR, rpm_wheelL):
    """Convert rpm to rad per seconde"""
    speed_wheelR = 2*pi*rpm_wheelR/60
    speed_wheelL = 2*pi*rpm_wheelL/60
    if speed_wheelR<0:
       speed_wheelR = -speed_wheelR
    if speed_wheelR<0:
        speed_wheelR = -speed_wheelR
    return [speed_wheelR, speed_wheelL]

def convert_rads_to_rpm(speed_wheelR, speed_wheelL):
    """Convert rad per seconde to rpm"""
    rpm_wheelR = 60*speed_wheelR/(2*pi)
    rpm_wheelL = 60*speed_wheelL/(2*pi)
    return [rpm_wheelR, rpm_wheelL]

def direct_kinematics(speed_wheelR, speed_wheelL):
    """ Cette fonction permet de calculer la vitesse lineaire vitesseLin et la vitesse angulaire
    vitesseAng du robot en fonction des vitesses des roues gauches et droites, respectivement vitesseG
    et vitesseD"""

    wheel_radius =0.025
    distance_wheel_center = 0.08

    linear_speed= wheel_radius*(speed_wheelR+speed_wheelL)/2
    angular_speed = wheel_radius*(speed_wheelR-speed_wheelL)/2*distance_wheel_center
    print ("Vitesse Lineaire = %.3f, Vitesse Angulaire = %.3f" % (linear_speed,angular_speed))
    return [linear_speed,angular_speed]

def odom(linear_speed,angular_speed,dTime,speed_wheelR,speed_wheelL):
    """Permet de calculer la nouvelle position (dx,dy,dtheta) du robot dans son repere"""
    wheel_radius =0.025
    distance_wheel_center = 0.08
    
    Theta = angular_speed*dTime
    dx =(wheel_radius/2)*(cos(Theta)*speed_wheelR+cos(Theta)*speed_wheelL)
    dy = (wheel_radius/2)*(sin(Theta)*speed_wheelR+sin(Theta)*speed_wheelL)
    dTheta=(wheel_radius/2)*(speed_wheelR/distance_wheel_center -speed_wheelL/distance_wheel_center)
 
    print ("Coordonnee du robot: x = %.3f, y = %.3f, theta= %.3f" % (dx, dy, dTheta))
    return[dx,dy,dTheta]
   # s.enter(0.2, 1, odom, (direct_kinematics(vitesseD,vitesseG),0.2,))

def tick_odom(old_xR,old_yR,old_thetaR,dx,dy,dTheta):
    """Permet de calculer la nouvelle position du robot dans le repere du "monde" """
    xR = old_xR+dx
    yR = old_yR+dy
    thetaR = old_thetaR+dTheta
    print ("Nouvelle coordonnee dans le monde: x = %.3f, y = %.3f, theta = %.3f" %(xR, yR, thetaR))
    return [xR, yR, thetaR]

def forward_kinematics(linear_speed, angular_speed):
    """ Calcule les vitesse linéaire et angulaire en fonction des vitesses des roues"""
    
    distance_wheel_center = 0.08
    wheel_radius = 0.025
    
    speed_wheelL = (linear_speed+distance_wheel_center*angular_speed)/wheel_radius
    speed_wheelD = (linear_speed-distance_wheel_center*angular_speed)/wheel_radius
    return [speed_wheelD, speed_wheelL]

