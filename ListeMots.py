#!/usr/bin/python3

"""Une ListeMots sous forme de dictionnaire qui regroupe les mots par leur longeur et s'assure de leur unicite'"""
class ListeMots:

    def __init__(self):
        self.listeMots = dict()
        self.longeur = 0

    #methodes de construction et recherche
    def len(self):
        return self.longeur

    def insert(self, mot):
        try:
            for stringa in self.listeMots[len(mot)]:
                if stringa == mot:  # si le mot est deja present dans la liste
                    return
            self.listeMots[len(mot)].append(mot)
            self.longeur += 1
        except:
            self.listeMots[len(mot)] = [mot]
            self.longeur += 1

    def estDans(self, mot):
        try:
            for string in self.listeMots[len(mot)]:
                if string == mot:
                    return True
            return False
        except KeyError:
            return False

    #methodes d'affichage
    def printCroissant(self):
        #print("Mots Trouvees:")
        for string in self.listeMots[3]:
            print(string + ", ", end='')
        print("")
        for string in self.listeMots[4]:
            print(string + ", ", end='')


    def printDecroissant(self):
        if self.longeur == 0:
            print("LISTE_VIDE")
            return
        liste_indices = list()
        for cle in self.listeMots.keys():
            liste_indices.append(cle)
        liste_indices.sort()
        liste_indices.reverse()

        #print("Mots Trouvees:")
        for indice in liste_indices:
            for string in self.listeMots[indice]:
                print(string + ", ", end='')
        print("")


    #methodes de gestion du Jeu en mode Multiplayer
    def compressToSend(self):
        liste_indices = [cle for cle in self.listeMots.keys()]
        liste_indices.sort()
        liste_indices.reverse()
        toSend = ""
        for indice in liste_indices:
            for string in self.listeMots[indice]:
                toSend += string + ";"
        return toSend[0:len(toSend) - 1]

    def decompress(self, toDecompress):
        stringa = toDecompress
        liste = stringa.split(';')
        for mot in liste:
            self.insert(mot)
