import cv2 as cv
import numpy as np
import time
import pypot.dynamixel

#open CV example
#https://docs.opencv.org/master/df/d9d/tutorial_py_colorspaces.html

#http://colorizer.org/


cap = cv.VideoCapture(0)

# largeur
resol_l = 320
cap.set(3,resol_l)
# hauteur
resol_h = 240
cap.set(4,resol_h)



ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit("no port")

dxl_io = pypot.dynamixel.DxlIO(ports[0])


while(1):
    
    time.sleep(.200)
    
    # Take each frame
    _, frame = cap.read()

    crop_bas = 120
    crop_milieu1 = 0
    crop_milieu2 = resol_l
    crop_img = frame[crop_bas:resol_h, crop_milieu1:crop_milieu2]
    frame = crop_img

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    
    #define range of red color in HSV
    lower_red = np.array([0,50,50])
    upper_red = np.array([20,255,255])

    #define range of green color in HSV
    lower_green = np.array([80,50,50])
    upper_green = np.array([100,255,255])

    #define range of red color in HSV
    lower_yellow = np.array([20,50,50])
    upper_yellow = np.array([30,255,255])


    # Threshold the HSV image to get only blue colors
    #mask = cv.inRange(hsv, lower_blue, upper_blue)
    mask = cv.inRange(hsv, lower_red, upper_red)
    #mask = cv.inRange(hsv, lower_green, upper_green)
    #mask = cv.inRange(hsv, lower_yellow, upper_yellow)
    
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    #cv.imshow('frame',frame)
    #cv.imshow('mask',mask)
    #cv.imshow('res',res)

    #on transforme en gris
    gray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
    #cv.imshow ('gray',gray)
    
    # Gaussian blur pour aider les étapes suivantes
    blur = cv.GaussianBlur(gray,(5,5),0)
    #cv.imshow('lur', blur)    
    #on applique un filtre binaire pour nettoyer le bruit
    ret,binair = cv.threshold(blur,50,255,cv.THRESH_BINARY_INV)
    #cv.imshow('binary', binair)
    
    edges = cv.Canny(binair,140,150,apertureSize = 3)
    #cv.imshow('edges',edges)


    summ_pixel_gauche = 0
    summ_pixel_droit = 0
    # on boucle sur les lignes
    for lines in edges:
        #on pour chaque pixel
        pixel_position = 0
        gauche = True
        for pixel in lines:
            pixel_position = pixel_position +1
            if pixel == 255:
                if gauche:
                    summ_pixel_gauche = summ_pixel_gauche + pixel_position
                    gauche = False
                else:
                    summ_pixel_droit = summ_pixel_droit + pixel_position
                    gauche = True
        
    moyenne_gauche = summ_pixel_gauche /resol_l
    moyenne_droit = summ_pixel_droit / resol_l
    pixel_milieu = resol_l / 2
    diff_gauche = moyenne_gauche - pixel_milieu
    diff_droit = moyenne_droit - pixel_milieu
    
    if abs(diff_gauche) > abs(diff_droit):
        print ("gauche")
        dxl_io.set_moving_speed({1:-25,2:20})
    else:
        print ("droite")
        dxl_io.set_moving_speed({1:-20,2:25})
        
    for i_line in frame:
        i_line[int(diff_gauche)] = 255
        i_line[int(diff_droit)] = 255
        i_line[int(pixel_milieu)] = 255
 
    for i_line in binair:
        i_line[int(diff_gauche)] = 255
        i_line[int(diff_droit)] = 255
        i_line[int(pixel_milieu)] = 255


    cv.imshow('Suivi',binair)
    cv.imshow('liveCam',frame)

     # pour sortir on detecte la touche échape
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
dxl_io.set_moving_speed({1:0,2:0})

