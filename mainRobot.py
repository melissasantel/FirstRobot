import cv2 as cv
import numpy as np
import time
import detectionLigne as dl


##########################################################################
##      Main Robot
#########################################################################

resol_h = 240
resol_l = 320

dl.initCamera(resol_l,resol_h)

#######################
while (1):

    #capturer une image ( en entrée on donne les deux points du carré à capturer)
    capture = dl.captureImage( 0,240 , 320,240)

    #switcher sur la bonne couleur ( decide seul quelle couleur suivre et renvoi l'image contenant uniquement cette couleur)
    capture_ligne = dl.switchCouleur(capture)
    cv.imshow("color",capture_ligne)

    #traiter l'image (applique un traitement à l'image et renvoi une image propre avec juste les cotes de la forme à suivre)
    capture_ligne = dl.traiteImg(capture_ligne)
    cv.imshow("binary",capture_ligne)

    #tourner dans la bonne direction
    if dl.directionGauche(capture_ligne):
    #    dm.tournerGauche()
        print ("gauche")
    else:
        print ("droite")
    #    dm.tournerDroite()

    #Mesurer deplacement
    #deplacement = dm.odometrie()

    #Creer carte deplacement
    #carte = dl.creerCarte(carte ,deplacement)


################## 

    #Affichage du liveCam
    print (dl.getDirectionLignes())
    live_image = dl.liveCam(capture, capture_ligne, dl.getDirectionLignes())
    cv.imshow("live_feed", live_image)

    #pause pour pas surcharger le proc
    time.sleep(0.200)


    # pour sortir on detecte la touche échape
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

#
#fin du while
#######################
cv.destroyAllWindows()


