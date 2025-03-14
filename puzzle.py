# puzzle.py
#
# Code that runs the Wumpus World as a puzzle.
#
# Run this on its own using:
# python puzzle.py
#
# but better is to invoke this through wumpus.py
#
# Written by: Simon Parsons
# Last Modified: 17/12/24

from puzzleWorld import PuzzleWorld
from dungeon import Dungeon
import random
import config
import utils
import time

# We explicitly define the main function to allow this to both be run
# from the command line on its own, or invoked (from wumpus.py)
def main():
    # How we set the puzzle up. 
    puzzle = PuzzleWorld()
    endState = PuzzleWorld()
    # Check if we want a display of the game state
    if not config.headless:
        display = Dungeon(puzzle)
        # Creates a visualization of the end state
        show = Dungeon(endState)

    # Uncomment this for a printout of world state and end state at the start
    #utils.printGameState(puzzle)
    #utils.printGameState(endState)

    # If we are showing the world, then update our view. 
    if not config.headless:
        # Show initial and end state
        display.update()
        # Show end state
        show.update()
        time.sleep(1)

    # Now run...
    start_time = time.time()
    while not(puzzle.isSolved(endState)):
        puzzle.makeAMove(endState)
        if not config.headless:
            display.update()
            time.sleep(1)
    end_time = time.time()

    print("complete time: ",end_time-start_time,"s")
    # Display message at end
    if puzzle.status == utils.State.WON:
        print("You succeeded!")
    else:
        print("You failed!")

    # Close the display --- needed if we are going to have multiple runs.
    if not config.headless:
        display.close()

# Since we explicitly named the main function
if __name__ == "__main__":
    main()
