#!/usr/bin/python3
from ListeMots import *
import time
from ArbreLex import *
from RuzzleMatrix import *
import pickle

class RuzzleGraph:

    def __init__(self, vertexList, dictionnaire):
        self.matchEnded = False
        self.vertexList = vertexList
        self.dictionnaire = dictionnaire
        self.listeMotsDansGrille = ListeMots()
        self.listeTrouvees = ListeMots()

    #methodes de construction et affichage
    def ajouteVertex(self, vertex):
        self.vertexList.append(vertex)

    def printSimpleGraph(self):
        for v in self.vertexList:
            print(v.value, " --> ", end='')
            for adj in v.listeAdjacences:
                print(adj.value, end='')
            print("")

    def affichageTableRuzzle(self):
        # print ligne 0
        print("  ", end='')
        for i in range(0, 5):
            if i % 2 == 0:
                print("/" + self.vertexList[i].value + "\\", end='')
            else:
                print(self.vertexList[i].value, end='')
        print("")
        # print ligne 1
        for i in range(5, 12):
            if i % 2 != 0:
                print("/" + self.vertexList[i].value + "\\", end='')
            else:
                print(self.vertexList[i].value, end='')
        print("")
        # print ligne 2
        for i in range(12, 19):
            if i % 2 == 0:
                print("\\" + self.vertexList[i].value + "/", end='')
            else:
                print(self.vertexList[i].value, end='')
        print("")
        # print ligne 3
        print("  ", end='')
        for i in range(19, 24):
            if i % 2 != 0:
                print("\\" + self.vertexList[i].value + "/", end='')
            else:
                print(self.vertexList[i].value, end='')
        print("")

    """Verification presence du mot dans la grille Ruzzle (pour methode 2)"""
    def motEstDansGraphe(self, mot):
        for vertex in self.vertexList:
            if vertex.value == mot[0] or vertex.value == '*':
                if self.motEstDansGrapheN(mot, vertex, "", None) is True:
                    return True
                
        return False

    def motEstDansGrapheN(self, mot, n, chainePartielle, listeDejaVisite):
        i = len(chainePartielle)

        if chainePartielle == mot:
            return True

        if i >= len(mot):
            return False

        # initialisation listeDejaVisite
        if i == 0:
            if mot[0] == n.value:
                listeDejaVisite = [n]
                return self.motEstDansGrapheN(mot, n, str(n.value), listeDejaVisite)
            elif n.value == '*':
                listeDejaVisite = [n]
                for car in range(97, 123):
                    result = self.motEstDansGrapheN(mot, n, str(chr(car)), listeDejaVisite)
                    if result is True:
                        return True
                    else:
                        continue
            else:
                return False

        else:  # cas i != 0, on a deja trouve le premier caractere du mot
            bonVoisin = False
            for vertex in n.listeAdjacences:
                if vertex.value == mot[i] and vertex not in listeDejaVisite:
                    bonVoisin = True
                    nouvelleDejaVisite = [el for el in listeDejaVisite]
                    nouvelleDejaVisite.append(vertex)
                
                    # on verifie la presence du caractere suivant dans le graphe
                    result = self.motEstDansGrapheN(mot, vertex, str(chainePartielle) + str(vertex.value), nouvelleDejaVisite)
                    if result is True:
                        return True
                    else:
                        continue
                elif vertex.value == '*' and vertex not in listeDejaVisite:
                    nouvelleDejaVisite = [el for el in listeDejaVisite]
                    nouvelleDejaVisite.append(vertex)
                    for car in range(97, 123):
                        result = self.motEstDansGrapheN(mot, vertex, str(chainePartielle) + str(chr(car)), nouvelleDejaVisite)
                        if result is True:
                            return True
 
            if bonVoisin == False:
                return False
            

    """Solution Ruzzle via Dictionnaire Python (DFS sur le graphe + verification presence mot non distribuee')"""
    def DFSPy(self, parcourDictionnaire):
        self.dictionnairePy = ArbreLex(parcourDictionnaire)
        # self.dictionnairePy.chargeDictionnaire(parcourDictionnaire)
        for v in self.vertexList:
            if v.value == '*':
                for i in range(97, 123):
                    if self.dictionnairePy.estDans(str(chr(i))) == 1:
                        self.DFSVisitPy(v, str(chr(i)), None)
            
            if self.dictionnairePy.estDans(v.value) == 1:
                self.DFSVisitPy(v, str(v.value), None)

    def DFSVisitPy(self, vertex, chainePartielle, listeDejaVisite):
        # cas 0, on ajoute la premiere lettre du mot a la liste dejaVisite
        if listeDejaVisite == None:
            listeDejaVisite = [vertex]
        # on passe au prefix successif en ajoutant un voisin si le prefix
        # chainePartielle+voisin existe dans le dictio
        for v in vertex.listeAdjacences:
            # on s'assure de ne pas passer deux fois sur la meme lettre
            if v not in listeDejaVisite:
                resultatRecherche = 0
                if v.value == '*':
                    for i in range(97, 123):
                        resultatRecherche = self.dictionnairePy.estDans(
                            chainePartielle + str(chr(i)))
                        if resultatRecherche == 0:
                            continue
                        elif resultatRecherche == 1:
                            nouvelleDejaVisite = list()
                            nouvelleDejaVisite = [i for i in listeDejaVisite]
                            nouvelleDejaVisite.append(v)
                            self.DFSVisitPy(
                                v, chainePartielle + str(chr(i)), nouvelleDejaVisite)
                        elif resultatRecherche == 2:
                            nouvelleDejaVisite = [i for i in listeDejaVisite]
                            nouvelleDejaVisite.append(v)
                            # on a trouve un mot
                            self.listeMotsDansGrille.insert(
                                chainePartielle + str(chr(i)))
                            self.DFSVisitPy(
                                v, chainePartielle + str(chr(i)), nouvelleDejaVisite)
                        elif resultatRecherche == 3:
                            # on a trouve un mot
                            self.listeMotsDansGrille.insert(
                                chainePartielle + str(chr(i)))

                else:
                    resultatRecherche = self.dictionnairePy.estDans(chainePartielle + str(v.value))
                    
                    if resultatRecherche == 0:
                        continue
                    elif resultatRecherche == 1:
                        nouvelleDejaVisite = list()
                        nouvelleDejaVisite = [i for i in listeDejaVisite]
                        nouvelleDejaVisite.append(v)
                        self.DFSVisitPy(v, chainePartielle + str(v.value), nouvelleDejaVisite)
                    elif resultatRecherche == 2:
                        nouvelleDejaVisite = [i for i in listeDejaVisite]
                        nouvelleDejaVisite.append(v)
                        # on a trouve un mot
                        self.listeMotsDansGrille.insert(chainePartielle + str(v.value))
                        self.DFSVisitPy(v, chainePartielle + str(v.value), nouvelleDejaVisite)
                    elif resultatRecherche == 3:
                        # on a trouve un mot
                        self.listeMotsDansGrille.insert(chainePartielle + str(v.value))

                

    """Solution Ruzzle via ServeurC (DFS sur le graphe + verification presence mot distribuee')"""
    def DFS(self):
        for v in self.vertexList:
            if v.value == '*':
                for i in range(97, 123):
                    self.DFSVisit(v, str(chr(i)), None)
            elif self.dictionnaire.estDans(v.value) == 1:
                self.DFSVisit(v, str(v.value), None)


    """
    Renvoie:
    0 -> pas dans l'arbre
    1 -> mot est prefixe
    2 -> mot est prefixe et mot
    3 -> est mot mais pas prefixe
    """
    def DFSVisit(self, vertex, chainePartielle, listeDejaVisite):
        # cas 0, on ajoute la premiere lettre du mot a la liste dejaVisite
        if listeDejaVisite == None:
            listeDejaVisite = [vertex]
        # on passe au prefix successif en ajoutant un voisin si le prefix
        # chainePartielle+voisin existe dans le dictio
        for v in vertex.listeAdjacences:
            # print(vertex.compteur, " --> ", v.compteur," -> ",v.value," -> ", [v.value for v in v.listeAdjacences])
            # on s'assure de ne pas passer deux fois sur la meme lettre
            if v not in listeDejaVisite:
                resultatRecherche = 0
                if v.value == '*':
                    for i in range(97, 123):
                        resultatRecherche = self.dictionnaire.estDans(
                            chainePartielle + str(chr(i)))
                        if resultatRecherche == 0:
                            continue
                        elif resultatRecherche == 1:
                            nouvelleDejaVisite = list()
                            nouvelleDejaVisite = [i for i in listeDejaVisite]
                            nouvelleDejaVisite.append(v)
                            self.DFSVisit(
                                v, chainePartielle + str(chr(i)), nouvelleDejaVisite)
                        elif resultatRecherche == 2:
                            nouvelleDejaVisite = [i for i in listeDejaVisite]
                            nouvelleDejaVisite.append(v)
                            # on a trouve un mot
                            self.listeMotsDansGrille.insert(
                                chainePartielle + str(chr(i)))
                            self.DFSVisit(
                                v, chainePartielle + str(chr(i)), nouvelleDejaVisite)
                        elif resultatRecherche == 3:
                            # on a trouve un mot
                            self.listeMotsDansGrille.insert(
                                chainePartielle + str(chr(i)))
                else:
                    resultatRecherche = self.dictionnaire.estDans(
                        chainePartielle + v.value)
                    if resultatRecherche == 0:
                        continue
                    elif resultatRecherche == 1:
                        nouvelleDejaVisite = list()
                        nouvelleDejaVisite = [i for i in listeDejaVisite]
                        nouvelleDejaVisite.append(v)
                        self.DFSVisit(
                            v, chainePartielle + str(v.value), nouvelleDejaVisite)
                    elif resultatRecherche == 2:
                        nouvelleDejaVisite = [i for i in listeDejaVisite]
                        nouvelleDejaVisite.append(v)
                        # on a trouve un mot
                        self.listeMotsDansGrille.insert(
                            chainePartielle + str(v.value))
                        self.DFSVisit(
                            v, chainePartielle + str(v.value), nouvelleDejaVisite)
                    elif resultatRecherche == 3:
                        # on a trouve un mot
                        self.listeMotsDansGrille.insert(
                            chainePartielle + str(v.value))


    #methodes de gestion du Jeu en mode Multiplayer
    def gererFinMatch(self, listeTrouvees):
        print("Time's UP!!!")
        if listeTrouvees.len() > 0:
            print("Score --> ", listeTrouvees.len())
            print("Mots Trouvees...")
            listeTrouvees.printDecroissant()
            print("Fin PARTIE!")
            self.matchEnded = True
        else:
            print("Aucun Mot a ete' trouve'!!!!\nScore --> 0")
            print("Fin PARTIE!")
            self.matchEnded = True

    def playOneMatch(self):
        listeTrouvees = ListeMots()
        self.affichageTableRuzzle()
        temps = float(
            input("\nSaisir le temps de duree de votre defi (en secondes)!\ntemps = "))
        timer = Timer(temps, self.gererFinMatch, [listeTrouvees])
        timer.start()
        print("Saisir les mots que vous trouvez dans la grille!...\n")
        while True:
            if self.matchEnded == True:
                sys.exit()
            mot = input("mot -> ")
            if self.listeMotsDansGrille.estDans(mot):
                listeTrouvees.insert(mot)

    def playChallenge(self, challengeTime):
        self.affichageTableRuzzle()
        start_time = time.time()
        while True:
            current_time = time.time() - start_time
            if current_time > float(challengeTime):
                print("\n***********************")
                print("Mots Trouves --> ", self.listeTrouvees.len())
                print("***********************")
                self.listeTrouvees.printDecroissant()
                print("***********************")
                return
            mot = input("mot -> ")
            if self.listeMotsDansGrille.estDans(mot):
                self.listeTrouvees.insert(mot)


    #methodes de Resolution automatique du Ruzzle
    """resolution ruzzle via C-ServerTree"""
    def generationM1(self, bool_print):
        start_time = time.time()
        self.DFS()
        end_time = time.time()
        
        print("Execution Time -> ", end_time - start_time)
        print("Mots Trouves: " + str(self.listeMotsDansGrille.len()) + "\n")
        if bool_print is True:
            self.listeMotsDansGrille.printDecroissant()
          

    """resolution ruzzle via Py-ServerTree"""
    def generationM1b(self, parcourDictionnaire, bool_print):
        start_time = time.time()
        self.DFSPy(parcourDictionnaire)
        end_time = time.time()

        print("Execution Time -> ", end_time - start_time)
        print("Mots Trouves: " + str(self.listeMotsDansGrille.len()) + "\n")
        if bool_print is True:
            self.listeMotsDansGrille.printDecroissant()

    """resolution ruzzle via methode 2 (on verifie la presence de chaque mot du Dictionnaire dans la grille)"""
    def generationM2(self, ruzzleGraph, parcourDictionnaire, bool_print):
        dictionnaire = ArbreLex(parcourDictionnaire)
        start_time = time.time()
        listeMotsDansGrille = dictionnaire.generePossiblesMots(ruzzleGraph)
        end_time = time.time()
        
        print("Execution Time -> ", end_time - start_time)
        print("Mots Trouves: " + str(listeMotsDansGrille.len()) + "\n")
        if bool_print is True:
            listeMotsDansGrille.printDecroissant()


if __name__ == "__main__":
    ruzzleMatrix = RuzzleMatrix("en")
    ruzzleMatrix.chaine = "sqeeetinihtznarfotierope"
    graph = ruzzleMatrix.vertexMatrixToGraph()
    ruzzleGraph = RuzzleGraph(graph, ArbreLex("ressources/dictEn"))
    ruzzleGraph.affichageTableRuzzle()

    #ruzzleGraph.generationM1b("ressources/dictEn", False)
    #ruzzleGraph.generationM2(ruzzleGraph, "ressources/dictEn", False)
    #ruzzleGraph.rechercheMot("ressources/dictEn", "ninetieth")
    print(ruzzleGraph.motEstDansGraphe("it"))

