#!/usr/bin/python3

import socket
from ListeMots import *


class ServerGame:

    def __init__(self, ipServerAddress, tcpServerPort, ruzzleGraph):
        self.ipServerAddress = ipServerAddress
        self.tcpServerPort = tcpServerPort
        self.BUFFER_SIZE = 2024
        self.listeTrouvees = ListeMots()
        self.ruzzleGraph = ruzzleGraph
        # starting server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ipServerAddress, self.tcpServerPort))
        self.s.listen(1)

    def waitForOpponent(self):
        print("En attente d' adversaire ... ")
        self.conn, self.addr = self.s.accept()
        print("Adversaire Trouve'! ---> ", self.addr, "\n")
        listeMotsAdversaire = ListeMots()
        listeTrouvees = ListeMots()
        received = str(self.receiveFromClient())
        # reponse au defi
        self.answerClient("CHALLENGE_ACCEPTED")
        # debut match en locale
        if received.startswith("TIME_"):
            self.ruzzleGraph.playChallenge(int(received[5:len(received)]))  # extraction du temps(%) de la str TIME_%
            # envoie resultats au client
            self.answerClient("RESULTS_" + self.ruzzleGraph.listeTrouvees.compressToSend())
            resultsClient = self.receiveFromClient()
            if resultsClient.startswith("RESULTS_"):
                resultsClient = resultsClient[8:len(resultsClient)]
                listeMotsAdversaire = ListeMots()
                listeMotsAdversaire.decompress(resultsClient)
                self.resultatMatch(self.ruzzleGraph.listeTrouvees, listeMotsAdversaire)

    def receiveFromClient(self):
        data = self.conn.recv(self.BUFFER_SIZE)
        stringa = str(data, 'utf-8')
        return stringa

    def answerClient(self, stringa):
        data = stringa
        b = data.encode('utf-8')
        self.conn.send(b)

    def resultatMatch(self, listeTrouvees, listeMotsAdversaire):
        print("")
        print("********************************")
        print("           FIN MATCH           *")
        print("********************************")
        print("L'Adversaire a trouve ", listeMotsAdversaire.len(), " mots...")
        print("********************************")
        listeMotsAdversaire.printDecroissant()
        print("")
        if listeTrouvees.len() == listeMotsAdversaire.len():
            print("Situation de EGALITE' ...")
        else:
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
