#!/usr/bin/python3
class ListeMots:
	def __init__(self):
		self.listeMots = dict()
		self.longeur = 0

	def len(self):
		return self.longeur

	def insert(self, mot):
		try:
			for stringa in self.listeMots[len(mot)]:
				if stringa == mot: #si le mot est deja present dans la liste
					return
			self.listeMots[len(mot)].append(mot)
			self.longeur += 1
		except:
			self.listeMots[len(mot)] = [mot]
			self.longeur += 1

	def printDecroissant(self):
		if self.longeur == 0:
			print("LISTE_VIDE")
			return
		liste_indices = list()
		for cle in self.listeMots.keys():
			liste_indices.append(cle)
		liste_indices.sort()
		liste_indices.reverse()
		for indice in liste_indices:
			for string in self.listeMots[indice]:
				print(string)

	def estDans(self, mot):
		try:
			for string in self.listeMots[len(mot)]:
				if string == mot:
					return True
			return False
		except KeyError:
			return False

	def compressToSend(self):
		liste_indices = [cle for cle in self.listeMots.keys()]
		liste_indices.sort()
		liste_indices.reverse()
		toSend = ""
		for indice in liste_indices:
			for string in self.listeMots[indice]:
				toSend += string+";"
		return toSend[0:len(toSend)-1]

	def decompress(self, toDecompress):
		stringa = toDecompress
		liste = stringa.split(';')
		for mot in liste:
			self.insert(mot)
