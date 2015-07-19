#!/usr/bin/python3

from ListeMots import *


class ArbreLex:

    def __init__(self, parcoursDict):
        self.noeudRoot = Noeud("", None, None)
        self.chargeDictionnaire(parcoursDict)
        self.listeMotsDansGrille = ListeMots()

    def generePossiblesMots(self, graph):
        self.parcourReturnArbre("", self.noeudRoot, graph)
        return self.listeMotsDansGrille

    """Methodes Construction de l'arbre"""

    def ajouteFils(self, lettre, noeud):
        n = Noeud(lettre, None, None)
        if noeud.fils is None:
            noeud.fils = n
            return noeud.fils
        else:
            ptr = noeud.fils
            while(ptr.frere is not None):
                ptr = ptr.frere
            ptr.frere = n
            return ptr.frere

    def estDans(self, mot):
        ptr = self.noeudRoot
        for i in range(0, len(mot)):
            #print(mot[i])
            #if mot[i] == 's':
            #    print(self.printFils(ptr))
            ptr = self.estFilsDe(mot[i], ptr)
            if ptr is None:
                return 0
        ptr = self.estFilsDe('-', ptr)
        if ptr is None:
            return 1
        else:
            ptr = ptr.frere
            if ptr is None:
                return 3
            else:
                return 2

    def estFilsDe(self, lettre, noeud):
        if noeud.fils is None:
            return None
        if noeud.fils.car == lettre:
            return noeud.fils
        else:
            ptr = noeud.fils
            while ptr.frere is not None:
                if ptr.frere.car == lettre:
                    return ptr.frere
                ptr = ptr.frere
            return None

    def ajouteMot(self, mot):
        ptr = self.noeudRoot
        ptr2 = ptr
        for i in range(0, len(mot)):
            ptr = self.estFilsDe(mot[i], ptr)
            if ptr is not None:
                ptr2 = ptr
                continue
            else:
                for j in range(i, len(mot)):
                    ptr2 = self.ajouteFils(mot[j], ptr2)
                ptr2 = self.ajouteFils('-', ptr2)
                return True

    def chargeDictionnaire(self, parcour):

        fichier = open(parcour, 'r')
        for ligne in fichier.readlines():
            self.ajouteMot(ligne[0:len(ligne) - 1])

    """Fonctions de recherche"""

    def rechercheMot(self, mot):
        ptr = self.noeudRoot
        for car in mot:
            ptr = self.estFilsDe(car, ptr)
            if ptr is not None:
                continue
            else:
                return False
        if self.estFilsDe('-', ptr):
            return True
        else:
            return False

    """Imprime tous les mots contenus dans l'arbre lexicographique a l'ecran"""

    def parcourPrintArbre(self, mot, n):
        ptr = n.fils
        while ptr is not None:
            if ptr.car == '-':
                print(mot)
                ptr = ptr.frere
                continue
            self.parcourPrintArbre(mot + ptr.car, ptr)
            ptr = ptr.frere

    def parcourReturnArbre(self, mot, n, graph):
        ptr = n.fils
        while ptr is not None:
            if ptr.car == '-':
                if graph.motEstDansGraphe(mot) is True:
                    self.listeMotsDansGrille.insert(mot)
                ptr = ptr.frere
                continue
            self.parcourReturnArbre(mot + ptr.car, ptr, graph)
            ptr = ptr.frere


class Noeud:

    def __init__(self, car, fils, frere):
        self.car = car
        self.fils = fils
        self.frere = frere
