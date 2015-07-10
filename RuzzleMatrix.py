#!/usr/bin/python3
from Vertex import *
import random


"""
Classe Outilitaire pour la construction du graphe representant le plateau du jeu
"""
class RuzzleMatrix:
	def __init__(self, langue):
		self.chaine = self.generateChaine(langue)
		self.grille = self.chaineToGrilleMatrix(self.chaine)
		self.vertexMatrix = self.grilleToVertexMatrix()

	"""
	Construction du Graphe a partir d'une matrice d'objets Vertex
	"""
	def vertexMatrixToGraph(self):
		graph = list()
		for i in range(0, 4):
			for j in range(0, 7):
				if (i,j) in [(0,0),(0,6),(3,0),(3,6)]:
					continue
				else:
					graph.append(self.vertexMatrix[i][j])
					listeVoisins = self.listeAdjacences(i, j, self.directionTriangle(i,j))
					for (m,n) in listeVoisins:
						self.vertexMatrix[i][j].ajouteAdjacence(self.vertexMatrix[m][n])
		return graph

	"""Generation de la chaine de caracteres a mettre dans le plateau,
		la chaine est genere' selon une table regroupante la percentage
		d'occurrence dans un texte de chaque lettre de la langue concernee
	"""
	def generateChaine(self, dictionnaireOccurrances):
		if dictionnaireOccurrances == "en":
			tableOccurranceEn = {'A':8,'B':2,'C':3,'D':4,'E':11,'F':2,'G':2,'H':5,'I':7,'J':1,'K':1,'L':4,'M':3,'N':7,'O':7,'P':2,'Q':1,'R':6,'S':6,'T':9,'U':3,'V':1,'W':2, 'X':1, 'Y':1, 'Z':1, '#':4, '*': 4}
			somme = 0
			listeLettres = list()
			for key, value in tableOccurranceEn.items():
				for i in range(0,value):
					listeLettres.append(key)
			mot = list()
			for j in range(0, 24):
				r = random.randint(0,107)
				mot.append(listeLettres[r])
			result = ''.join(mot).lower()
			return result
		elif dictionnaireOccurrances == "fr":
			tableOccurranceFr = {'A':8,'B':1,'C':3,'D':4,'E':14,'F':1,'G':1,'H':1,'I':8,'J':1,'K':1,'L':5,'M':3,'N':7,'O':5,'P':3,'Q':1,'R':6,'S':8,'T':7,'U':6,'V':2,'W':1,  'X':1, 'Y':1, 'Z':1, '#':4, '*': 4}
			somme = 0
			listeLettres = list()
			for key, value in tableOccurranceFr.items():
				for i in range(0,value):
					listeLettres.append(key)
			mot = list()
			for j in range(0, 24):
				r = random.randint(0,107)
				mot.append(listeLettres[r])
			result = ''.join(mot).lower()
			return result

	def grilleToVertexMatrix(self):
		vertexMatrix = list()
		for i in range(0, len(self.grille)):
			vertexMatrix.append([])
			for j in range(0, len(self.grille[0])):
				vertexMatrix[i].append(Vertex(self.grille[i][j]))
		return vertexMatrix

	def printVertexMatrix(self):
		for i in range(0, len(self.vertexMatrix)):
			for j in range(0, len(self.vertexMatrix[0])):
				print(self.vertexMatrix[i][j].value,end='')
			print("")
		print("")

	def chaineToGrilleMatrix(self, chaine):
		grille = [[],[],[],[]]
		for i in range(0,len(chaine)+4):
			if i in [0,6]:
				grille[0].append('#')
			elif i in [21,27]:
				grille[3].append('#')
			elif i < 6:
				grille[0].append(chaine[i-1])
			elif i < 14:
				grille[1].append(chaine[i-2])
			elif i < 21:
				grille[2].append(chaine[i-2])
			else:
				grille[3].append(chaine[i-3])
		return grille

	def listeAdjacences(self, i, j, direction):
		result = list()
		if direction == "haut":
			result = [(i-1, j-1),(i-1,j),(i-1,j+1),(i,j-2),(i,j-1),(i,j+1),(i,j+2),(i+1,j-2),(i+1,j-1),(i+1,j),(i+1,j+1),(i+1,j+2)]
		elif direction == "bas":
			result = [(i-1,j-2),(i-1,j-1),(i-1,j),(i-1,j+1),(i-1,j+2),(i,j-2),(i,j-1),(i,j+1),(i,j+2),(i+1, j-1),(i+1,j),(i+1,j+1)]
		result = [(i,j) for (i,j) in result if (i,j) not in [(0,0),(0,6),(3,0),(3,6)] and (i>-1 and i<4 and j>-1 and j<7)]
		return result

	def printListeAdjacences(self):
		for i in range(0,4):
			print([i.value for i in self.vertexMatrix[i]])
		for i in range(0, 4):
			for j in range(0, 7):
				if (i,j) in [(0,0),(0,6),(3,0),(3,6)]:
					continue
				else:
					stringa = self.vertexMatrix[i][j].value + " --> " + str(self.listeAdjacences(i,j,self.directionTriangle(i,j)))
					print(stringa)

	def directionTriangle(self, i, j):
		hautDirectionTriangles = [(0,1),(0,3),(0,5),(1,0),(1,2),(1,4),(1,6),(2,1),(2,3),(2,5),(3,2),(3,4)]
		if (i,j) in hautDirectionTriangles:
			return "haut"
		else:
			return "bas"
