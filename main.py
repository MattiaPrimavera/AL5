"""
Usage:
python3 RuzzleGraph.py -m1 PORT --> execution time study
"""

from subprocess import *
import sys

from threading import *
from ClientDictionnaire import *
from RuzzleMatrix import *
from ServerGame import *
from ClientGame import *
from Vertex import *
from ArbreLex import *
from ListeMots import *
from RuzzleGraph import *

def main():
    #initialisation variables
    langue = ""
    parcourDictionnaire = ""
    for par in sys.argv:
        if par == "en":
            langue = "en"
            parcourDictionnaire = "./ressources/dictEn"
        if par == "fr":
            langue = "fr"
            parcourDictionnaire = "./ressources/dictFr"

    #creation de la grille de jeu
    ruzzle = RuzzleMatrix(langue)
    grafoRuzzle = RuzzleGraph(ruzzle.vertexMatrixToGraph(), None)

    # methode 1 (ArbreLexServeur C)
    if sys.argv[1] == "-m1":  
        grafoRuzzle.affichageTableRuzzle()
        print("\n\n")

        grafoRuzzle.dictionnaire = ClientDictionnaire(int(sys.argv[2]))
        grafoRuzzle.generationM1(True)
    
    # methode 1b (ArbreLex en Python)
    elif sys.argv[1] == "-m1b":  
        grafoRuzzle.affichageTableRuzzle()
        print("\n\n")
        grafoRuzzle.generationM1b(parcourDictionnaire, True)
    
    # methode 2 (ArbreLex en Python)
    elif sys.argv[1] == "-m2":  
        grafoRuzzle.affichageTableRuzzle()
        print("\n\n")
        grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, True)

    # Statistiques - Comparation de performances m1 - m1b - m2    
    elif sys.argv[1] == "-s":
        grafoRuzzle.dictionnaire = ClientDictionnaire(int(sys.argv[2]))
        grafoRuzzle.affichageTableRuzzle()
        
        print("Methode 1 (ArbreLexServeur C) --> ")
        grafoRuzzle.generationM1(False)
        grafoRuzzle.listeMotsDansGrille = ListeMots()

        print("Methode 1b (ArbreLex Python) --> ")
        grafoRuzzle.generationM1b(parcourDictionnaire, False)
        grafoRuzzle.listeMotsDansGrille = ListeMots()
    
        print("\nMethode 2 (Py - Parcours Diction) --> ")
        grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, False)
    
    #Multiplayer Mode - Server Side
    elif sys.argv[1] == "-server": 
        print("Generation Liste Mots A Trouver...")
        grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, False)
        print("\nEn attente de connexion pour une defi!")
        serverGame = ServerGame('localhost', int(sys.argv[2]), grafoRuzzle)
        serverGame.waitForOpponent()
    
    #Multiplayer Mode - Client Side
    elif sys.argv[1] == "-client": 
        print("Generation Liste Mots A Trouver...")
        grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, False)
        clientGame = ClientGame(sys.argv[2], int(sys.argv[3]), grafoRuzzle)
        temps = int(input("saisir temps du defi : "))
        clientGame.sendChallenge(temps)

    #mode Single Player
    else: 
        dictionnaire = ArbreLex('-')
        dictionnaire.chargeDictionnaire(parcourDictionnaire)
        dictionnaire.generePossiblesMots(grafoRuzzle)
        grafoRuzzle.playOneMatch()

if __name__ == "__main__":
    main()
