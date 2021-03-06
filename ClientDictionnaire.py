#!/usr/bin/python3

import socket


"""
Classe qui recherche la presence d'un mot dans le dictionnaire en s'appuyant
sur le Dictionnaire Serveur (ecrit en langage C qui doit avoir ete' prealablement active')
"""

class ClientDictionnaire:

    def __init__(self, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', port))

    def estDans(self, mot):
        data = mot + "\0"
        b = data.encode('utf-8')
        self.client_socket.send(b)
        recu = self.client_socket.recv(2)
        stringa = str(recu, 'utf-8')
        return int(stringa)
