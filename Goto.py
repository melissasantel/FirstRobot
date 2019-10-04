from math import pi, sqrt
import control as Ct
import pypot.dynamixel
import time
import Robot as R
import cv2 as cv
import os

class GoTo: 
    """ Defines the displacement of our robot at a known point. We recover the 
    coordinates at the definition of this point. 
    - xC
    - yC
    thetaC """  
    
    def __init__(self, xC, yC, thetaC):
        """ class Goto constructor """
        self.xC = float(xC)
        self.yC = float(yC)
        self.thetaC = float(thetaC)
        
    def calcul_dist(self,xR, yR):
        """This function allow to get the distance to do"""
        return sqrt(pow((self.xC-xR),2)+pow((self.yC-yR),2))
        
    def calcul_angle_of_deplacement(self,thetaR):
        """This function allow to get the right angle for the robot to turn """
        delta_angle = (thetaR-self.thetaC)
        angle_i = delta_angle%pi
        if delta_angle<0:
           angle_i =-angle_i
        return angle_i
    
    def forward(self,linear_speed,angular_speed):
        """ This function give the order to the robot forward """
        global dxl_io
        
        [speed_wheelR, speed_wheelL]= Ct.forward_kinematics(linear_speed, angular_speed)
        print("Vitesse des roues droite et gauche ",speed_wheelR, speed_wheelL)
        [rpm_wheelR, rpm_wheelL]= Ct.convert_rads_to_rpm(speed_wheelR, speed_wheelL)
        print("Vitesse en RPM", rpm_wheelR, rpm_wheelL)

        dxl_io.set_moving_speed({1:50,2:50})
        
    def get_wheels_speed(self):
        """ Get the speed of the robot wheels """
        [rpm_wheelR, rpm_wheelL] = dxl_io.get_moving_speed([1,2])
        [speed_wheelR, speed_wheelL] = Ct.convert_rpm_to_rads(rpm_wheelR, rpm_wheelL)
        return [speed_wheelR, speed_wheelL]
    
    def calcul_robot_state(self,delta_time):
        """ Calcul the position of the robot in its onw referential and on world referential """
        global robot
        
        [speed_wheelR, speed_wheelL] = self.get_wheels_speed()
        [linear_speed, angular_speed]=Ct.direct_kinematics(speed_wheelR, speed_wheelL)
        [dx,dy,dTheta] = Ct.odom(linear_speed, angular_speed,delta_time,speed_wheelR, speed_wheelL)
        robot.old_xR = robot.xR
        robot.old_YR = robot.yR
        robot.old_thetaR =robot.thetaR
        [xR, yR, thetaR] = Ct.tick_odom(robot.xR, robot.yR, robot.thetaR,dx,dy,dTheta)
        return [xR, yR, thetaR]
        
    def max_rotation_index(self, p):
        """ Calcul de coefficient of rotation """
        max_p = 1
        if p>max_p: 
            return 1
        return p
        
    def run(self):
        """ Function to go to a point x,y,theta """
        global robot
        
        robot = R.RobotState()
        t0=time.time()
        
        ports = pypot.dynamixel.get_available_ports()
        if not ports:
            exit('no port')
        
        global dxl_io
        dxl_io = pypot.dynamixel.DxlIO(ports[0])
            
        distance_to_do = self.calcul_dist(robot.xR,robot.yR)
        print("******Distance à réaliser********",distance_to_do)

        angle_i = self.calcul_angle_of_deplacement(robot.thetaR) 
        print("******Angle de rotation******", angle_i)
        
        #First the robot rotate
        linear_speed = 0
        p = 0.5
        angular_speed = angle_i*self.max_rotation_index(p)
        print("******Vitesse Angulaire*****", angular_speed)

        #Calcul the vitesse of wheels
        self.forward(linear_speed, angular_speed)
        #dxl_io.set_moving_speed({1:rpm_wheelR,2:rpm_wheelL})
        dxl_io.set_moving_speed({1:50,2:60})
        t1=time.time()
        delta_time=t1-t0

        while distance_to_do > 0.01:
            time.sleep(0.010)
            t0=time.time()
            [robot.xR, robot.yR, robot.thetaR] = self.calcul_robot_state(delta_time)
            t1=time.time()
            distance_to_do = self.calcul_dist(robot.xR,robot.yR)
            angle_i = self.calcul_angle_of_deplacement(robot.thetaR)
            linear_speed = 0.05
            angular_speed = angle_i*self.max_rotation_index(p)
            #Calcul the vitesse of wheels
            self.forward(linear_speed, angular_speed)
            delta_time = t1-t0
            print(delta_time)
 
        self.stop()
    
    def stop(self):
        """ This function permit to stop de robot """
        dxl_io.set_moving_speed({1:0,2:0})

