from math import pi

class RobotState: 
    """  Defines the object robot. 
    - xR
    - yR
    - thetaR 
    - old_xR
    - old_yR
    - old_thetaR
    - distance_wheel_center 
    - wheel_radius"""
    
    def __init__(self):
        """ class constructor Robot """
        self.xR=0
        self.yR=0
        self.thetaR=1.570 
        self.old_xR=0
        self.old_yR=0
        self.old_thetaR=0
        self.distance_wheel_center=0.025
        self.wheel_radius=0.08
        
    
    
    
