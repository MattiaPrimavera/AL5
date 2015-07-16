# AL5

Ruzzle Implementation with Algorithm performance study

## Requirements

* gcc 
* python3

## Usage

    chmod +x start.sh

To execute the single player mode use the following command:

    ./start.sh
    
The exagonal grid will appear and you'll be prompted to choose how many seconds you want the challenge to last: find all the words you can by writing them one by one on your keyboard and validating through the **Enter** Key.

For the multiplayer (local) mode, run the server:

    ./start.sh -server tcpServerPort

then the client in another terminal window:

    ./start.sh -client serverAddress tcpPort 

You can also run the automatic solver for each approach studied, so that:
    
    ./start.sh -m1

will generate a new grid and solve it by using the first approach (check the **Approaches** section of this document) through the Tree-Server Dictionnary written in C language.
By executing

    ./start.sh -m1b

the grid will still be solved by using the first approach but this time through the Lexicographic-Tree written in Python language.

And finally you can execute the second approach to find all the words hidden by executing (this time the entire solution has been written in Python):

    ./start.sh -m2

If you wanna make check 

    ./start.sh -s 

## Synopsis

This project is a modified version of the Ruzzle videogame where you have to find the most of the words hidden inside the grid you can, and in a limited lapse of time.

In this implementation the grid has exagonal shape and cases can contain walls ('#' character), which cannot be used in the sequence of letters to form a "discovered word", and jolly characters ('*'), which can be used as no matter the letter we need.   

## Algorithms

The interest behind the project was a performance study on different approaches to solve following problem: how many words are hidden in a given exagonal grid of characters? How many would they be if the grid contained walls and jolly characters?

### Approaches

Two approaches have been studied here: one is to compare each possible combination of consecutive characters from the grid with the dictionary, the other is to check how many words from the dictionnary are hidden in the grid by trying to verify if each of the word is somewhere in the grid.

### Data Structures and Algorithms:

A Graph has been used to modelize the characters grid while the dictionary as been implemented as a Lexicographic-Tree (A tree where each node is a letter). A particular List Objects handles the list of words found in the current grid, in order to fasten up the process of checking the presence of a word into the list.

A Depth-First-Search algorithm has been used on the graph and on the tree to read the dictionnary and walk through all the possible combinations of neighboor characaters in the graph.

Since the first approach is the most performant one (verify the informations executing with **-s option**), an implementation of the dictionary as a local Server written in C language has been written to replace the one written in Python and check if we could gain in performances by dividing the tasks in a distributed system with could exploit C language power with a through a Client-Server model.
This last approached revealed to be the most performing one.
