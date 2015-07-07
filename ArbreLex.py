#!/usr/bin/python3
import time


class ArbreLex:

    def __init__(self, lettre):
        self.noeudRoot = Noeud(lettre, None, None)

    def generePossiblesMots(self, graph):
        self.parcourReturnArbre("", self.noeudRoot, graph)
        return True

    def ajouteFils(self, lettre, noeud):
        n = Noeud(lettre, None, None)
        if noeud.fils == None:
            noeud.fils = n
            return noeud.fils
        else:
            ptr = noeud.fils
            while(ptr.frere != None):
                ptr = ptr.frere
            ptr.frere = n
            return ptr.frere

    def estFilsDe(self, lettre, noeud):
        if noeud.fils == None:
            return None
        if noeud.fils.car == lettre:
            return noeud.fils
        else:
            ptr = noeud.fils
            while ptr.frere != None:
                if ptr.car == lettre:
                    return ptr
                ptr = ptr.frere
            return None

    def rechercheMot(self, mot):
        ptr = self.noeudRoot
        for car in mot:
            ptr = self.estFilsDe(car, ptr)
            if ptr != None:
                continue
            else:
                return False
        if self.estFilsDe('-', ptr):
            return True
        else:
            return False

    def estDans(self, mot):
        ptr = self.noeudRoot
        for i in range(0, len(mot)):
            ptr = self.estFilsDe(mot[i], ptr)
            if ptr == None:
                return 0
        ptr = self.estFilsDe('-', ptr)
        if ptr == None:
            return 1
        else:
            ptr = ptr.frere
            if ptr == None:
                return 3
            else:
                return 2

    def ajouteMot(self, mot):
        ptr = self.noeudRoot
        ptr2 = ptr
        for i in range(0, len(mot)):
            ptr = self.estFilsDe(mot[i], ptr)
            if ptr != None:
                ptr2 = ptr
                continue
            else:
                for j in range(i, len(mot)):
                    ptr2 = self.ajouteFils(mot[j], ptr2)
                ptr2 = self.ajouteFils('-', ptr2)
                return True

    def parcourReturnArbre(self, mot, n, graph):
        ptr = n.fils
        while ptr != None:
            if ptr.car == '-':
                graph.motEstDansGraphe(mot)
                ptr = ptr.frere
                continue
            self.parcourReturnArbre(mot + ptr.car, ptr, graph)
            ptr = ptr.frere

    def parcourPrintArbre(self, mot, n):
        ptr = n.fils
        while ptr != None:
            if ptr.car == '-':
                print(mot)
                ptr = ptr.frere
                continue
            self.parcourPrintArbre(mot + ptr.car, ptr)
            ptr = ptr.frere

    def chargeDictionnaire(self, parcour):

        fichier = open(parcour, 'r')
        for ligne in fichier.readlines():
            self.ajouteMot(ligne[0:len(ligne) - 1])


class Noeud:

    def __init__(self, car, fils, frere):
        self.car = car
        self.fils = fils
        self.frere = frere
