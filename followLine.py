import control as Rc
import pypot.dynamixel
import time
import cv2 as cv
import detectionLigne as dl
import debug as dbg
import Robot as R
import Goto



def initialisation():
    
    dbg.aff("initialisation")
    
    global dxl_io
    global orderToMove
    global robot1
    
    orderToMove = False
    
    #Check access to pypot.dynamixel
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        exit('no port')
        
    dxl_io = pypot.dynamixel.DxlIO(ports[0])
    dxl_io.set_moving_speed({1:0,2:0})
    
    #Access to camera and image from vision
    resol_h = 240
    resol_l = 320

    dl.initCamera(resol_l,resol_h)
    
    #Initialise robotState
    robot1 = R.RobotState()
    
def mainLine(): 

    #input(res)


    global orderToMove

    dbg.aff("debut main")
 
    initialisation()
    
    #successiv_robot_state = list()
    #successiv_robot_state.append([robot1.xR,robot1.yR,robot1.thetaR,time.time()])
    while True: 
        t0=time.time()
        
        #print ("avance ? (enter)")
        #input()
        orderToMove = True

        #Get the different 
        linear_speed = 0.02
        coeff_angular_speed = 0.5 #rad/s can't be above 3.14
        
            #capturer une image ( en entrée on donne les deux points du carré à capturer)
        capture = dl.captureImage( 0,0 , 320,240)

        #switcher sur la bonne couleur ( decide seul quelle couleur suivre et renvoi l'image contenant uniquement cette couleur)
        capture_ligne = dl.switchCouleur(capture)
        #cv.imshow("color",capture_ligne)

        #traiter l'image (applique un traitement à l'image et renvoi une image propre avec juste les cotes de la forme à suivre)
        capture_ligne = dl.traiteImg(capture_ligne)
        #cv.imshow("binary",capture_ligne)

        #tourner dans la bonne direction
        direction = 0
        if dl.directionGauche(capture_ligne):
        #    dm.tournerGauche()
            print ("**** ALLER A GAUCHE ****")
            direction = -1
            avanceG = 5
            avanceD = -8
        else:
            print ("****ALLER A DROITE ****")
            direction = 1
            avanceG = 8
            avanceD = -5
        #    dm.tournerDroite()
        
        angular_speed = direction*coeff_angular_speed
        
        
        #Cacul the speed of wheels
        [speed_wheelR, speed_wheelL]=Rc.forward_kinematics(linear_speed, angular_speed)
        [rpm_wheelR, rpm_wheelL]= Rc.convert_rads_to_rpm(speed_wheelR, speed_wheelL)
        
        #Give instruction to move forward
        if orderToMove:
            print ("Vitesse roue droite= %.2f" % rpm_wheelR)
            print ("Vitesse roue gauche= %.2f" % rpm_wheelL)
            #dxl_io.set_moving_speed({1:-rpm_wheelR,2:rpm_wheelL})
            dxl_io.set_moving_speed({1:avanceD,2:avanceG})
        
        #Get the position of the robot in the world and update the robot state
        [linear_speed, angular_speed]=Rc.direct_kinematics(speed_wheelR, speed_wheelL)
        
        
        delta_time = 0.05
        
        [dx,dy,dTheta] = Rc.odom(linear_speed, angular_speed,delta_time,speed_wheelR, speed_wheelL)
        robot1.old_xR = robot1.xR
        robot1.old_YR = robot1.yR
        robot1.old_thetaR =robot1.thetaR
        [robot1.xR, robot1.yR, robot1.thetaR] = Rc.tick_odom(robot1.xR, robot1.yR, robot1.thetaR,dx,dy,dTheta)
        
        t1=time.time()
        
        #Append the state of the robot in a list
        #successiv_robot_state.append(.. )
        
        #Calcul frequency of program executions
        if t1-t0 != 0:
            freqExec=1/((t1-t0))
            print ("Execution time: %.2f" % freqExec)


        #Affichage du liveCam
        print (dl.getDirectionLignes())
        live_image = dl.liveCam(capture_ligne, capture_ligne, dl.getDirectionLignes())
        cv.imshow("live_feed", live_image)

        #pause pour pas surcharger le proc
        time.sleep(0.2)


        # pour demarrer le robot on detecte la touche entree
        k = cv.waitKey(5) & 0xFF
        if k == 10:
            if orderToMove:
                orderToMove = False
                dxl_io.set_moving_speed({1:0,2:0})
            else:
                orderToMove = True

        # pour sortir on detecte la touche échape
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            dxl_io.set_moving_speed({1:0,2:0})
            break


#
#fin du while
#######################
cv.destroyAllWindows()

        
dbg.start()
#if __name__ == "main":
mainLine() 
