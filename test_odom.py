import os
import control as ctrl
import pypot.dynamixel
import time

def test_odom():
    xR=0
    yR=0
    thetaR=0
    while True:
        ports = pypot.dynamixel.get_available_ports()
        if not ports:
            exit('no port')
            
        dxl_io = pypot.dynamixel.DxlIO(ports[0])
        dxl_io.disable_torque([1,2])
        # dxl_io.enable_torque([1,2])
        # dxl_io.set_moving_speed({1:5,2:-5})
        [rpm_wheelR,rpm_wheelL]=dxl_io.get_moving_speed([1,2])
        [speed_wheelR, speed_wheelL]=ctrl.convert_rpm_to_rads(rpm_wheelR, rpm_wheelL)
        [linear_speed,angular_speed]=ctrl.direct_kinematics(speed_wheelR, speed_wheelL)
        [dx,dy,dTheta]=ctrl.odom(linear_speed, angular_speed,0.05,speed_wheelR,speed_wheelL)
        [xR, yR,thetaR]=ctrl.tick_odom(xR, yR, thetaR,dx,dy,dTheta)
        print(time.time()) 
        dxl_io.close()

test_odom()
