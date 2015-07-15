#!/usr/bin/python3

class Vertex:
    compteur = 0

    def __init__(self, value):
        if value != '#':
            Vertex.compteur += 1
        self.compteur = Vertex.compteur
        self.value = value
        self.listeAdjacences = list()

    def ajouteAdjacence(self, vertex):
        self.listeAdjacences.append(vertex)
