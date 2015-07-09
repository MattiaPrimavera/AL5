#!/bin/bash

# Usage:
# chmod +x start.sh
#
# Execute one of the commands
# ./start.sh -m1 
# ./start.sh -m1b
# ./start.sh -m2
# ./start.sh -s 

case "$1" in
    "-m1" )
		echo "Starting C-Server Dictionary";
		gcc arbreLexServer.c -o arbreLexServer;
		./arbreLexServer 8000 ressources/dictEn &
		python3 main.py -m1 8000 en;
        ;;
    "-m1b")
		python3 main.py -m1b en;
		;;
    "-m2" )
        python3 main.py -m2 en;
        ;;
    "-s")
		gcc arbreLexServer.c -o arbreLexServer;
		./arbreLexServer 8000 ressources/dictEn &
		python3 main.py -s 8000 en
		;;
esac