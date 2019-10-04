import Goto as go

print("Entrez les coordonnées du point cible")
xC = input("xC :")
yC = input("yC :")
thetaC = input("thetaC :")
            
goto = go.GoTo(xC,yC,thetaC)
goto.run()