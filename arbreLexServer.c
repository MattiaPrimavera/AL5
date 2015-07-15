#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#include <resolv.h>
#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <strings.h>

#define true 1
#define false 0
#define MAXBUF 1024

typedef struct Noeud Noeud;
struct Noeud {
	Noeud* frereSuivant;
	Noeud* fils; //il y a que un fils et une liste de frères
	char car;
};

int rechercheMot(const char* mot, Noeud* n);
void parcourPrint(const char* mot, Noeud* n);
void printListeFreres(Noeud* n);
void printVerticalFils(Noeud* n);
Noeud* ajouteFrere(char c, Noeud* n);
Noeud* ajouteFils(char c, Noeud* n);
Noeud* estInListeFreres(char c, Noeud* n);
Noeud* estFilsDe(char c, Noeud* n);
int ajouteMot(const char* mot, Noeud* n);
Noeud* ajouteFilsN(char c, Noeud* n);
Noeud* chargeDictionnaire(char* parcour, Noeud* n);

//USAGE: ./arbreLexServer PORT dict_path
int main(int argc, char** argv)
{
	int i;
	int MY_PORT = atoi(argv[1]);
	Noeud* arbre = malloc(sizeof(Noeud));

	arbre->car = '-';
	arbre->frereSuivant = NULL;

	chargeDictionnaire(argv[2], arbre);
	//printf("recherche zoo = %d\n", rechercheMot("zoo", arbre));
	//parcourPrint("", arbre);

	//PARTIE SERVEUR DU DICTIONNAIRE
	int sockfd;
	struct sockaddr_in self;
	char buffer[MAXBUF];

	/*---Create streaming socket---*/
	if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		perror("Socket");
		exit(errno);
	}

	/*---Initialize address/port structure---*/
	bzero(&self, sizeof(self));
	self.sin_family = AF_INET;
	self.sin_port = htons(MY_PORT);
	self.sin_addr.s_addr = INADDR_ANY;

	/*---Assign a port number to the socket---*/
	if (bind(sockfd, (struct sockaddr*)&self, sizeof(self)) != 0) {
		perror("socket--bind");
		exit(errno);
	}

	/*---Make it a "listening socket"---*/
	if (listen(sockfd, 20) != 0) {
		perror("socket--listen");
		exit(errno);
	}

	/*---Forever... ---*/
	int clientfd;
	struct sockaddr_in client_addr;
	int addrlen = sizeof(client_addr);

	/*---accept a connection (creating a data pipe)---*/
	clientfd = accept(sockfd, (struct sockaddr*)&client_addr, &addrlen);
	//printf("%s:%d connected\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
	while (1) {
		recv(clientfd, buffer, MAXBUF, 0);
		/*---Echo back 0 if not present, 1 if present, 2 if prefix and mot---*/
		char* reponse = malloc(2 * sizeof(char));
		//printf("recu -> %s\n", buffer);
		int resultatRecherche = rechercheMot(buffer, arbre);
		//printf("resultatRecherche = %d\n", resultatRecherche);
		sprintf(reponse, "%d", resultatRecherche);
		send(clientfd, reponse, 1, 0);
		/*---Close data connection---*/
	}

	/*---Clean up (should never get here!)---*/
	close(clientfd);
	close(sockfd);
}

/*
Recherche mot dans l'arbre, la fonction renvoie:
0 -> pas dans l'arbre
1 -> mot est prefixe
2 -> mot est prefixe et mot
3 -> est mot mais pas prefixe
*/
int rechercheMot(const char* mot, Noeud* n)
{
	Noeud* ptr = n;
	int i = 0;

	for (i = 0; i < strlen(mot); i++) {
		if ((ptr = estFilsDe(mot[i], ptr)) == NULL) return 0;
	}
	if ((ptr = estFilsDe('-', ptr)) == NULL) {
		return 1;
	} else {
		if ((ptr = ptr->frereSuivant) == NULL)
			return 3;
		else
			return 2;
	}
}

void parcourPrint(const char* mot, Noeud* n)
{
	Noeud* ptr = n->fils;
	char* destination = malloc(25 * sizeof(char));

	strcpy(destination, mot);
	while (ptr != NULL) {
		if (ptr->car == '-') {
			printf("%s\n", mot);
			ptr = ptr->frereSuivant;
			continue;
		}
		strncat(destination, &(ptr->car), 1);
		parcourPrint(destination, ptr);
		ptr = ptr->frereSuivant;
		strcpy(destination, mot);
	}
}

//ajoute un mot à l'arbre, le mot se termine par '-'
int ajouteMot(const char* mot, Noeud* n)
{
	Noeud* ptr = n;
	Noeud* ptr2;

	if (strlen(mot) == 1) {
		ptr = ajouteFilsN(mot[0], n);
		ptr = ajouteFilsN('-', ptr);
		return true;
	}
	if (n == NULL) return false;
	int i, j;

	for (i = 0; i < strlen(mot); i++) {
		if ((ptr2 = estFilsDe(mot[i], ptr)) != NULL)
			ptr = ptr2;
		else {
			for (j = i; j < strlen(mot); j++)
				ptr = ajouteFilsN(mot[j], ptr);
			break;
		}
	}
	ptr = ajouteFilsN('-', ptr);
	return true;
}

Noeud* ajouteFilsN(char c, Noeud* n)
{
	//creation noeud
	Noeud* result = malloc(sizeof(Noeud));

	result->frereSuivant = NULL;
	result->fils = NULL;
	result->car = c;

	//ajout fils
	Noeud* ptr = n;
	if (n->fils == NULL) {
		n->fils = result;
		return result;
	} else {
		ptr = n->fils;
		return ajouteFrere(c, ptr);
	}
}

Noeud* estFilsDe(char c, Noeud* n)
{
	if (n->fils == NULL) return NULL;
	Noeud* result = estInListeFreres(c, n->fils);
	if (result == NULL) return NULL;
	else return result;
}

Noeud* estInListeFreres(char c, Noeud* n)
{
	Noeud* ptr = n;

	while (ptr != NULL) {
		if (ptr->car == c) return ptr;
		ptr = ptr->frereSuivant;
	}
	return NULL;
}

Noeud* ajouteFils(char c, Noeud* n)
{
	//création fils
	Noeud* result = malloc(sizeof(Noeud));

	result->frereSuivant = NULL;
	result->car = c;
	result->fils = NULL;
	//ajoute fils
	n->fils = result;
	return result;
}

Noeud* ajouteFrere(char c, Noeud* n)
{
	//création frère
	Noeud* result = malloc(sizeof(Noeud));

	result->car = c;
	result->fils = NULL;
	result->frereSuivant = NULL;
	//ajoute frère
	Noeud* ptr = n;
	while (ptr->frereSuivant != NULL) {
		ptr = ptr->frereSuivant;
	}
	ptr->frereSuivant = result;
	return result;
}

//Construction de l'arbre lexicographique à partir d'un fichier
Noeud* chargeDictionnaire(char* parcour, Noeud* n)
{
	//ouverture fichier
	FILE* fichier;

	if ((fichier = fopen(parcour, "r")) == NULL)
		perror("");

	//on ajoute chaque mot du fichier à l'arbre lexicographique
	char *tampon = malloc(25 * sizeof(char));
	while (!feof(fichier)) {
		fscanf(fichier, "%s\n", tampon);
		ajouteMot(tampon, n);
	}
}

void printVerticalFils(Noeud* n)
{
	Noeud* ptr = n;

	while (ptr->fils != NULL) {
		printf("%c", ptr->car);
		ptr = ptr->fils;
	}
	printf("%c\n", ptr->car);
}

void printListeFreres(Noeud* n)
{
	Noeud* ptr = n;

	while (ptr != NULL) {
		printf("%c", ptr->car);
		ptr = ptr->frereSuivant;
	}
	putchar('\n');
}
