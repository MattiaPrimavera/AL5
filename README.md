# AL5

Ruzzle Implementation with Algorithm performance study

## Requirements

* gcc 
* python3

## Usage

    chmod +x start.sh

To execute the single player mode use the following command:

    ./start.sh
    
The exagonal grid will appear and you'll be prompted to choose how many seconds you want the challenge to last: find all the words you can by writing them one by one on your keyboard and validating through the `Enter` Key.

For the multiplayer (local) mode, run the server:

    ./start.sh -server tcpServerPort

then the client in another terminal window:

    ./start.sh -client serverAddress tcpPort 

You can also run the automatic solver for each approach studied, so that:
    
    ./start.sh -m1

will generate a new grid and solve it by using the first approach (check the **Approaches** section of this document) through the Lexicographic-Tree Server Dictionnary written in C language.
By executing

    ./start.sh -m1b

the grid will still be solved by using the first approach but this time through the Lexicographic-Tree written in Python language.

And finally you can execute the second approach to find all the words hidden with (this time the entire solution has been written in Python):

    ./start.sh -m2

If you wanna have a visual comparison of the three strategies with execution times on the same automatically generated grid: 

    ./start.sh -s 

Here's an execution example of last command:



## Synopsis

This project is a modified version of the [Ruzzle](https://fr.wikipedia.org/wiki/Ruzzle) videogame where you have to find the most of the words hidden inside the grid you can, and in a limited lapse of time.

In this implementation the grid has exagonal shape instead of being square-shaped and cases can contain **walls** (`#` character), which cannot be used in the sequence of letters to form a **discovered word**, and **jolly** characters (`*`), which can be used as no matter the letter we need.   

## Algorithms

The interest behind this project was a performance study on different approaches to solve the following problem: **how many words are hidden in a given exagonal grid of characters? How many would they be if the grid contained walls and jolly characters?**

### Approaches

Two approaches have been studied here: one is to compare each possible combination of consecutive characters from the grid with the dictionary, the other is to check how many words from the dictionnary are hidden in the grid by trying to verify if each of the word is somewhere in the grid.

### Data Structures and Algorithms:

A **Graph** has been used to modelize the grid characters while the dictionary as been implemented as a **Lexicographic-Tree** (A tree where each node is a letter, which increases performances when checking if a word is inside the dictionary). A Customized **List** Object handles the list of words found in the current grid, ordering them according to their length, in order to fasten up the process of checking the presence of a word into the list.

A **Depth-First-Search** algorithm has been used on the graph and on the tree to read the dictionnary and walk through all the possible combinations of neighboor characaters in the graph.

As predicted, the first approach results more performant than the second one (you may want to verify the informations executing with `-s option`). As an attempt to increase again performances, an implementation of the dictionary as a local Server written in C language has replaced the one written in Python (`-m1 option`). 

With success, an ulterior gain in performances was so obtained by dividing the tasks in a distributed system and exploiting on the dictionnary side the execution speed of C language (the main program and the dictionnary communicate thanks to Server-Client model).

Eventually the last approach revealed to be the most performing one.
