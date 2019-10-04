import cv2 as cv
import numpy as np
import debug as dbg
import time

moyenne_gauche = 0
moyenne_droit = 0
pixel_milieu = 0
diff_gauche = 0
diff_droit = 0


resol_h = 240
resol_l = 320
couleur_courante = 2

cap = cv.VideoCapture(0)

def getDirectionLignes ():
    global diff_gauche
    global diff_droit
    global pixel_milieu
    
    return diff_gauche, diff_droit, pixel_milieu

def initCamera(resH,resL):
    
    global cap
    
    # largeur
    cap.set(3,resL)

    # hauteur
    cap.set(4,resH)



#fonction qui traite l'image pour enlever le bruit et ne garder que le contour
def traiteImg (img_capturee):


    #on transforme en gris
    gray = cv.cvtColor(img_capturee,cv.COLOR_BGR2GRAY)
    #cv.imshow ('gray',gray)

    # Gaussian blur pour aider les étapes suivantes
    blur = cv.GaussianBlur(gray,(5,5),0)
    #cv.imshow('lur', blur)

    #on applique un filtre binaire pour nettoyer le bruit
    ret,binair = cv.threshold(blur,50,255,cv.THRESH_BINARY_INV)
    #cv.imshow('binary', binair)
 
    #edges = cv.Canny(binair,140,150,apertureSize = 3)
    #cv.imshow('edges',edges)


    return binair

######################################



############################
#fonction qui permet de renvoyer une image de controle en mergant plusieurs images
def liveCam ( img_live , img_traitee, lignes_directions):

    for i_line in img_live:
            i_line[int(lignes_directions[0])] = 255
            i_line[int(lignes_directions[1])] = 255
            i_line[int(lignes_directions[2])] = 255
 
    x_live = 0
    y_live = 0
    #for l_line in img_traitee:
    #    y_live = y_live + 1
    #    for p_pix in l_line:
    #        x_live = x_live + 1
    #        if p_pix == 255:
    #            img_live[x_live][y_live] = 255

    return img_live

############################



#fonction qui permet de renvoyer l'image contenant une seule couleur
def switchCouleur ( img_live):

    global couleur_courante


    _, img_live = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(img_live, cv.COLOR_BGR2HSV)


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


    #test couleur verte
    #si oui changer la couleur



    if (couleur_courante == 0 ):
        mask = cv.inRange(hsv, lower_yellow, upper_yellow)
    if (couleur_courante == 1 ):
        mask = cv.inRange(hsv, lower_blue, upper_blue)
    if (couleur_courante == 2 ):
        mask = cv.inRange(hsv, lower_red, upper_red)

    res = cv.bitwise_and(img_live,img_live, mask= mask)


    return res

###############################



def captureImage(crop_milieu1, crop_bas,crop_milieu2 ,crop_haut):
    
    # Take each frame
    ret , frame = cap.read()

    if ret != True:
        time.sleep(0.200)
        dbg.aff("failed to capture a first image")

    
    #crop_img = frame[crop_bas:crop_haut, crop_milieu1:crop_milieu2]
    crop_img = frame[200:240, 0:320]
    frame = crop_img
    
    return frame

def directionGauche(image_traitee):
    global pixel_milieu
    global diff_gauche
    global diff_droit
    global moyenne_gauche
    global moyenne_droit
    
    summ_pixel_gauche = 0
    summ_pixel_droit = 0
    
    milieu_image = int (resol_l / 2)
    identimage = 0

    print ("mmmmm",milieu_image)

    for lines in image_traitee:
        #pour chaque pixel
        identimage = 0
        #identimage = identimage + 1
        for pixel in lines:
            identimage = identimage + 1
            if pixel == 0:
                if identimage < milieu_image:
                    summ_pixel_gauche = summ_pixel_gauche + 1
                else:
                    summ_pixel_droit = summ_pixel_droit + 1

    # on boucle sur les lignes
    #for lines in image_traitee:
        #on pour chaque pixel
        #pixel_position = 0
        #gauche = True
        #for pixel in lines:
        #    pixel_position = pixel_position +1
        #    if pixel == 255:
        #        if gauche:
        #            summ_pixel_gauche = summ_pixel_gauche + pixel_position
        #            gauche = False
        #        else:
        #            summ_pixel_droit = summ_pixel_droit + pixel_position
        #            gauche = True
                    
    moyenne_gauche = summ_pixel_gauche /resol_l
    moyenne_droit = summ_pixel_droit / resol_l
    
    #pixel_milieu = resol_l / 2
    
    #diff_gauche = moyenne_gauche - pixel_milieu
    diff_gauche = moyenne_gauche
    #diff_droit = moyenne_droit - pixel_milieu
    diff_droit = moyenne_droit
    print ( "***",diff_gauche,"***",diff_droit)

    return diff_gauche > diff_droit
