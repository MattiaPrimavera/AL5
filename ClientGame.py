#!/usr/bin/python3
import socket
import sys
from ListeMots import *


class ClientGame:

	def __init__(self, tcpServerAddress, tcpServerPort, ruzzleGraph):
		self.tcpServerPort = tcpServerPort
		self.tcpServerAddress = tcpServerAddress
		self.ruzzleGraph = ruzzleGraph

	def sendChallenge(self, challengeTime):
		#on envoie une requete de defi au serveur
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverHostName = socket.gethostbyaddr(self.tcpServerAddress)
		serverHostName = serverHostName[0]
		self.client_socket.connect((serverHostName, self.tcpServerPort))
		#envoie du defi au serveur
		print("Connexion au Serveur en cours ...\n")
		self.sendToServeur("TIME_"+str(challengeTime))
		#elaboration reponse
		reponseDuServeur = self.receiveFromServeur()
		if reponseDuServeur == "CHALLENGE_ACCEPTED":
			self.ruzzleGraph.playChallenge(challengeTime)
			#envoie resultats...
			self.sendToServeur("RESULTS_"+self.ruzzleGraph.listeTrouvees.compressToSend())
			#reception resultats
			reponse = self.receiveFromServeur()
			if reponse.startswith("RESULTS_") == True:
				reponse = reponse[8:len(reponse)]
				listeMotsAdversaire = ListeMots()
				listeMotsAdversaire.decompress(reponse)
				self.resultatMatch(self.ruzzleGraph.listeTrouvees, listeMotsAdversaire)

	def sendToServeur(self, stringa):
		data = stringa
		b = data.encode('utf-8')
		self.client_socket.send(b)

	def receiveFromServeur(self):
		recu = self.client_socket.recv(2048)
		stringa = str(recu, 'utf-8')
		return stringa

	def resultatMatch(self, listeTrouvees, listeMotsAdversaire):
		print("")
		print("********************************")
		print("           FIN MATCH           *")
		print("********************************")
		print("L'Adversaire a trouve ", listeMotsAdversaire.len(), " mots...")
		print("********************************")
		listeMotsAdversaire.printDecroissant()
		print("")
		if listeTrouvees.len() > listeMotsAdversaire.len():
			print("Vous avez Gagne!  ", listeTrouvees.len(), " - ", listeMotsAdversaire.len())
		else:
			print("Vous avez Perdu!  ", listeMotsAdversaire.len(), " - ", listeTrouvees.len())

		print("Mots Trouvees...")
		print("********************************")
		if listeTrouvees.len() == 0:
			print("   LISTE_VIDE")
		else:
			listeTrouvees.printDecroissant()
		print("********************************")

		print("Mots Adversaire...")
		print("********************************")
		if listeMotsAdversaire.len() == 0:
			print("   LISTE_VIDE")
			print("********************************")
		else:
			listeMotsAdversaire.printDecroissant()
			print("********************************")
