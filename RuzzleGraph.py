#!/usr/bin/python3
from subprocess import *
import _thread
import sys
import socket
import time
from threading import *
from ClientDictionnaire import *
from RuzzleMatrix import *
from ServerGame import *
from ClientGame import *
from Vertex import *
from ArbreLex import *
from ListeMots import *

class RuzzleGraph:
	def __init__(self, vertexList, dictionnaire):
		self.matchEnded = False
		self.vertexList = vertexList
		self.dictionnaire = dictionnaire
		self.listeMotsDansGrille = ListeMots()
		self.listeTrouvees = ListeMots()

	def ajouteVertex(self, vertex):
		self.vertexList.append(vertsex)

	def printSimpleGraph(self):
		for v in self.vertexList:
			print(v.value," --> ",end='')
			for adj in v.listeAdjacences:
				print(adj.value, end='')
			print("")
	def affichageTableRuzzle(self):
		#print ligne 0
		print("  ",end='')
		for i in range(0,5):
			if i%2==0:
				print("/"+self.vertexList[i].value+"\\",end='')
			else:
				print(self.vertexList[i].value,end='')
		print("")
		#print ligne 1
		for i in range(5,12):
			if i % 2 != 0:
				print("/"+self.vertexList[i].value+"\\",end='')
			else:
				print(self.vertexList[i].value,end='')
		print("")
		#print ligne 2
		for i in range(12,19):
			if i % 2 == 0:
				print("\\"+self.vertexList[i].value+"/",end='')
			else:
				print(self.vertexList[i].value,end='')
		print("")
		#print ligne 3
		print("  ",end='')
		for i in range(19,24):
			if i % 2 != 0:
				print("\\"+self.vertexList[i].value+"/",end='')
			else:
				print(self.vertexList[i].value,end='')
		print("")

	def motEstDansGraphe(self, mot):
		for vertex in self.vertexList:
			if vertex.value == mot[0]:
				if self.motEstDansGrapheN(mot, vertex, 0, None) == True:
					return True
			elif vertex.value == '*':
				if self.motEstDansGrapheN(mot, vertex, 0, None) == True:
					return True
		return False

	def motEstDansGrapheN(self, mot, n, i, listeDejaVisite):
		#on a trouve un mot, on l'insere dans la grille
		if i == len(mot):
			self.listeMotsDansGrille.insert(mot)
			return True
		#initialisation listeDejaVisite
		if i == 0:
			if mot[0] == n.value:
				listeDejaVisite = [n]
				self.motEstDansGrapheN(mot, n, 1, listeDejaVisite)
			elif n.value == '*':
				listeDejaVisite = [n]
				self.motEstDansGrapheN(mot, n, 1, listeDejaVisite)
			else:
				return False
		else: #cas i != 0, on a deja trouve le premier caractere du mot
			estDansListe = False
			for vertex in n.listeAdjacences:
				if vertex.value == mot[i] and vertex not in listeDejaVisite:
					nouvelleDejaVisite = listeDejaVisite
					nouvelleDejaVisite.append(vertex)
					estDansListe = True
					self.motEstDansGrapheN(mot, vertex, i+1, nouvelleDejaVisite	) #on verifie la presence du carac suivant dans le graphe
				elif vertex.value == '*':
					nouvelleDejaVisite = listeDejaVisite
					nouvelleDejaVisite.append(vertex)
					estDansListe = True
					self.motEstDansGrapheN(mot, vertex, i+1, nouvelleDejaVisite)

			if estDansListe == False:
				return False

	def DFSPy(self, parcourDictionnaire):
		self.dictionnairePy = ArbreLex('-')
		self.dictionnairePy.chargeDictionnaire(parcourDictionnaire)		
		for v in self.vertexList:
			if v.value == '*':
				for i in range(97, 123):
					self.DFSVisitPy(v, str(chr(i)), None)
			elif self.dictionnairePy.estDans(v.value) == 1:
				self.DFSVisitPy(v, str(v.value), None)

	def DFSVisitPy(self, vertex, chainePartielle, listeDejaVisite):
		#cas 0, on ajoute la premiere lettre du mot a la liste dejaVisite
		if listeDejaVisite == None:
			listeDejaVisite = [vertex]
			#print("in DFSVisit -> ", [vertex.value for vertex in vertex.listeAdjacences])
		#on passe au prefix successif en ajoutant un voisin si le prefix chainePartielle+voisin existe dans le dictio
		for v in vertex.listeAdjacences:
			#print(vertex.compteur, " --> ", v.compteur," -> ",v.value," -> ", [v.value for v in v.listeAdjacences])
			if v not in listeDejaVisite: #on s'assure de ne pas passer deux fois sur la meme lettre
				resultatRecherche = 0
				if v.value == '*':
					for i in range(97, 123):
						resultatRecherche = self.dictionnairePy.estDans(chainePartielle+str(chr(i)))
						if resultatRecherche == 0:
							continue
						elif resultatRecherche == 1:
							nouvelleDejaVisite = list()
							nouvelleDejaVisite = [i for i in listeDejaVisite]
							nouvelleDejaVisite.append(v)
							self.DFSVisitPy(v, chainePartielle+str(chr(i)), nouvelleDejaVisite)
						elif resultatRecherche == 2:
							nouvelleDejaVisite = [i for i in listeDejaVisite]
							nouvelleDejaVisite.append(v)
							#on a trouve un mot
							self.listeMotsDansGrille.insert(chainePartielle+str(chr(i)))
							self.DFSVisitPy(v, chainePartielle+str(chr(i)), nouvelleDejaVisite)
						elif resultatRecherche == 3:
							#on a trouve un mot
							self.listeMotsDansGrille.insert(chainePartielle+str(chr(i)))
				else:
					resultatRecherche = self.dictionnairePy.estDans(chainePartielle+str(v.value))
					if resultatRecherche == 0:
						continue
					elif resultatRecherche == 1:
						nouvelleDejaVisite = list()
						nouvelleDejaVisite = [i for i in listeDejaVisite]
						nouvelleDejaVisite.append(v)
						self.DFSVisitPy(v, chainePartielle+str(v.value), nouvelleDejaVisite)
					elif resultatRecherche == 2:
						nouvelleDejaVisite = [i for i in listeDejaVisite]
						nouvelleDejaVisite.append(v)
						#on a trouve un mot
						self.listeMotsDansGrille.insert(chainePartielle+str(v.value))
						self.DFSVisitPy(v, chainePartielle+str(v.value), nouvelleDejaVisite)
					elif resultatRecherche == 3:
						#on a trouve un mot
						self.listeMotsDansGrille.insert(chainePartielle+str(v.value))

	#remplissage liste de mots possibles via ServeurC
	def DFS(self):
		for v in self.vertexList:
			if v.value == '*':
				for i in range(97, 123):
					self.DFSVisit(v, str(chr(i)), None)
			elif self.dictionnaire.estDans(v.value) == 1:
				self.DFSVisit(v, str(v.value), None)	

	#0 -> pas dans l'arbre
	#1 -> mot est prefixe
	#2 -> mot est prefixe et mot 
	#3 -> est mot mais pas prefixe
	def DFSVisit(self, vertex, chainePartielle, listeDejaVisite):
		#cas 0, on ajoute la premiere lettre du mot a la liste dejaVisite
		if listeDejaVisite == None:
			listeDejaVisite = [vertex]
			#print("in DFSVisit -> ", [vertex.value for vertex in vertex.listeAdjacences])
		#on passe au prefix successif en ajoutant un voisin si le prefix chainePartielle+voisin existe dans le dictio
		for v in vertex.listeAdjacences:
			#print(vertex.compteur, " --> ", v.compteur," -> ",v.value," -> ", [v.value for v in v.listeAdjacences])
			if v not in listeDejaVisite: #on s'assure de ne pas passer deux fois sur la meme lettre
				resultatRecherche = 0
				if v.value == '*':
					for i in range(97, 123):
						resultatRecherche = self.dictionnaire.estDans(chainePartielle+str(chr(i)))
						if resultatRecherche == 0:
							continue
						elif resultatRecherche == 1:
							nouvelleDejaVisite = list()
							nouvelleDejaVisite = [i for i in listeDejaVisite]
							nouvelleDejaVisite.append(v)
							self.DFSVisit(v, chainePartielle+str(chr(i)), nouvelleDejaVisite)
						elif resultatRecherche == 2:
							nouvelleDejaVisite = [i for i in listeDejaVisite]
							nouvelleDejaVisite.append(v)
							#on a trouve un mot
							self.listeMotsDansGrille.insert(chainePartielle+str(chr(i)))
							self.DFSVisit(v, chainePartielle+str(chr(i)), nouvelleDejaVisite)
						elif resultatRecherche == 3:
							#on a trouve un mot
							self.listeMotsDansGrille.insert(chainePartielle+str(chr(i)))			
				else:
					resultatRecherche = self.dictionnaire.estDans(chainePartielle+v.value)
					if resultatRecherche == 0:
						continue
					elif resultatRecherche == 1:
						nouvelleDejaVisite = list()
						nouvelleDejaVisite = [i for i in listeDejaVisite]
						nouvelleDejaVisite.append(v)
						self.DFSVisit(v, chainePartielle+str(v.value), nouvelleDejaVisite)
					elif resultatRecherche == 2:
						nouvelleDejaVisite = [i for i in listeDejaVisite]
						nouvelleDejaVisite.append(v)
						#on a trouve un mot
						self.listeMotsDansGrille.insert(chainePartielle+str(v.value))
						self.DFSVisit(v, chainePartielle+str(v.value), nouvelleDejaVisite)
					elif resultatRecherche == 3:
						#on a trouve un mot
						self.listeMotsDansGrille.insert(chainePartielle+str(v.value))

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
		temps = float(input("\nSaisir le temps de duree de votre defi (en secondes)!\ntemps = "))
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

	#resolution ruzzle via C-ServerTree
	def generationM1(self, bool_print):
		if bool_print == True:
			self.affichageTableRuzzle()	
		start_time = time.time()
		self.DFS()
		end_time = time.time()
		if bool_print == True:
			self.listeMotsDansGrille.printDecroissant()
		print("Execution Time -> ", end_time - start_time)	

	#resolution ruzzle via Py-ServerTree
	def generationM1b(self, parcourDictionnaire, bool_print):
		if bool_print == True:
			self.affichageTableRuzzle()
		start_time = time.time()
		self.DFSPy(parcourDictionnaire)
		end_time = time.time()
		if bool_print == True:
			self.listeMotsDansGrille.printDecroissant()
		print("Execution Time -> ", end_time - start_time)

	def generationM2(self, ruzzleGraph, parcourDictionnaire, bool_print):
		if bool_print == True:
			self.affichageTableRuzzle()
		dictionnaire = ArbreLex('-')
		dictionnaire.chargeDictionnaire(parcourDictionnaire)
		start_time = time.time()
		dictionnaire.generePossiblesMots(ruzzleGraph)
		end_time = time.time()
		if bool_print == True:
			self.listeMotsDansGrille.printDecroissant()
		print("Execution Time -> ", end_time - start_time)	




"""
Usage:
python3 RuzzleGraph.py -m1 PORT   --> execution time study

"""
def main():

	langue = ""
	parcourDictionnaire = ""
	for par in sys.argv:
		if par == "en":
			langue = "en"
			parcourDictionnaire = "./dictEn"
		if par == "fr":
			langue = "fr"
			parcourDictionnaire = "./dictFr"

	ruzzle = RuzzleMatrix(langue)
	grafoRuzzle = RuzzleGraph(ruzzle.vertexMatrixToGraph(), None)
	#appel de la juste option
	if sys.argv[1] == "-m1": #methode 1 (ArbreLexServeur C)
		grafoRuzzle.dictionnaire = ClientDictionnaire(int(sys.argv[2]))
		grafoRuzzle.generationM1(True)
	elif sys.argv[1] == "-m1b": #methode 1b (ArbreLex en Python)
		#grafoRuzzle.dictionnaire = ClientDictionnaire(int(sys.argv[3]))
		#grafoRuzzle.generationM1(True)		
		grafoRuzzle.generationM1b(parcourDictionnaire, True)
		#grafoRuzzle.generationM2(grafoRuzzle, sys.argv[2], True)
	elif sys.argv[1] == "-m2": #methode 2 (ArbreLex en Python)
		grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, True)
	elif sys.argv[1] == "-s":
		grafoRuzzle.dictionnaire = ClientDictionnaire(int(sys.argv[2]))
		grafoRuzzle.affichageTableRuzzle()
		#execution M1
		print("Methode 1 (ArbreLexServeur C) --> ")
		grafoRuzzle.generationM1(False)
		#execution M1b
		print("Methode 1b (ArbreLex Python) --> ")
		grafoRuzzle.generationM1b(parcourDictionnaire, False)
		#execution M2
		print("Methode 2 (Py - Parcours Diction) --> ")
		grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, False)
	elif sys.argv[1] == "-server":
		print("Generation Liste Mots A Trouver...")
		grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, False)
		print("\nEn attente de connexion pour une defi!")
		serverGame = ServerGame('localhost', int(sys.argv[2]), grafoRuzzle)
		serverGame.waitForOpponent()
	elif sys.argv[1] == "-client":
		print("Generation Liste Mots A Trouver...")
		grafoRuzzle.generationM2(grafoRuzzle, parcourDictionnaire, False)
		clientGame = ClientGame(sys.argv[2], int(sys.argv[3]), grafoRuzzle)
		temps = int(input("saisir temps du defi : "))
		clientGame.sendChallenge(temps)
	else:
		dictionnaire = ArbreLex('-')
		dictionnaire.chargeDictionnaire(parcourDictionnaire)
		dictionnaire.generePossiblesMots(grafoRuzzle)
		grafoRuzzle.playOneMatch()

if __name__ == "__main__":
	main()
