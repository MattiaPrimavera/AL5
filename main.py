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

    if sys.argv[1] == "-m1":  # methode 1 (ArbreLexServeur C)
        grafoRuzzle.dictionnaire = ClientDictionnaire(int(sys.argv[2]))
        grafoRuzzle.generationM1(True)
    elif sys.argv[1] == "-m1b":  # methode 1b (ArbreLex en Python)
        grafoRuzzle.generationM1b(parcourDictionnaire, True)
    elif sys.argv[1] == "-m2":  # methode 2 (ArbreLex en Python)
        grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, True)
    elif sys.argv[1] == "-s":
        grafoRuzzle.dictionnaire = ClientDictionnaire(int(sys.argv[2]))
        grafoRuzzle.affichageTableRuzzle()
        # execution M1
        print("Methode 1 (ArbreLexServeur C) --> ")
        grafoRuzzle.generationM1(False)
        
        # execution M1b
        print("Methode 1b (ArbreLex Python) --> ")
        grafoRuzzle.generationM1b(parcourDictionnaire, False)
    
        # execution M2
        print("\nMethode 2 (Py - Parcours Diction) --> ")
        grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, False)
    
    elif sys.argv[1] == "-server": #Multiplayer Mode - Server Side
        print("Generation Liste Mots A Trouver...")
        grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, False)
        print("\nEn attente de connexion pour une defi!")
        serverGame = ServerGame('localhost', int(sys.argv[2]), grafoRuzzle)
        serverGame.waitForOpponent()
    elif sys.argv[1] == "-client": #Multiplayer Mode - Client Side
        print("Generation Liste Mots A Trouver...")
        grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, False)
        clientGame = ClientGame(sys.argv[2], int(sys.argv[3]), grafoRuzzle)
        temps = int(input("saisir temps du defi : "))
        clientGame.sendChallenge(temps)
    else: #mode Single Player
        dictionnaire = ArbreLex('-')
        dictionnaire.chargeDictionnaire(parcourDictionnaire)
        dictionnaire.generePossiblesMots(grafoRuzzle)
        grafoRuzzle.playOneMatch()

if __name__ == "__main__":
    main()
