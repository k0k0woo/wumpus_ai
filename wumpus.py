# wumpus.py
#
# A script to invoke both the game and the puzzle versions of the
# wumpus world.
#
# To find out how to use it, run:
# python wumpus.py -h

# Written by: Simon Parsons
# Last Modified: 06/01/24

# This borrows from:
# https://www.geeksforgeeks.org/command-line-arguments-in-python/

import puzzle
import getopt
import random
import config
import game
import sys

#
# Print help message.
#
def displayHelp():
    print("wumpus.py accepts the following arguments:")
    print("-h : generates this message")
    print("-g : runs the game version of the wumpus world")
    print("-p : runs the puzzle version of the wumpus world")
    print("-d : do not use the graphics (ie run headless)")
    print("-n <number> : runs either the -p or the -g version <number> of times. Note that <number> should be an integer")

def main():
    # Seed the random number generator.
    #
    # Your code will be tested with the random seed fixed to your student
    # ID and some other fixed values. But you probably want to comment
    # this out during development so you test under a variety of
    # conditions
    random.seed(config.myId)
    
    # Set global flags to help parse the command line arguments
    wType = "none"
    count = 1
    
    # Drop the filename from the list of command line arguments
    argList = sys.argv[1:]

    # We support a help option, running either the game version or the
    # puzzle version, running with no display, and possiblly running n
    # iterations.
    options = "hgpdn:"

    # Long options
    long_options = ["Help", "Game", "Puzzle", "Headless", "Number"]

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argList, options, long_options)
    
        # checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--Help"):
                displayHelp()
                wType = "none"
            
            elif currentArgument in ("-g", "--Game"):
                wType = "game"
            
            elif currentArgument in ("-p", "--Puzzle"):
                wType = "puzzle"
                
            elif currentArgument in ("-d", "--Headless"):
                config.headless = True

            elif currentArgument in ("-n", "--Number"):
                count = int(currentValue)
                print(currentValue)
                
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
    
    if wType != "none":
        if wType == "game":
            for i in range(count):
                game.main()
        elif wType == "puzzle":
            for i in range(count):
                puzzle.main()            
        
if __name__ == "__main__":
    main()
