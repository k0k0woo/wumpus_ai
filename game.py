# game.py
#
# Code that runs the Wumpus World as a game.
#
# run this on its own using:
# python game.py
#
# but better is to invoke this through wumpus.py
#
# Written by: Simon Parsons
# Last Modified: 17/12/24

from world import World
from link  import Link
from dungeon import Dungeon
import random
import config
import utils
import time
import statistics

# We explicitly define the main function to allow this to both be run
# from the command line on its own, or invoked (from wumpus.py)
def main():
    # How we set the game up. Create a world, then connect player and
    # display to it.
    gameWorld = World()
    player = Link(gameWorld)
    display = Dungeon(gameWorld)

    # Uncomment this for a printout of world state at the start
    #utils.printGameState(gameWorld)

    # Show initial state
    display.update()
    time.sleep(1)
    # Now run...
    calc_time = []
    while not(gameWorld.isEnded()):
        start_time = time.time()
        gameWorld.updateLink(player.makeMove())
        end_time = time.time()-start_time
        calc_time.append(end_time)
        gameWorld.updateWumpus()
        # Uncomment this for a printout of world state every step
        # utils.printGameState(gameWorld)
        display.update()
        time.sleep(0.1)

    # Display message at end
    #if gameWorld.status == utils.State.WON:
        #print("You won!")
    #else:
        #print("You lost!")

    calc_time.sort(reverse=True)
    longest = round(calc_time[0]*1000,2)
    calc_time.sort()
    shortest = round(calc_time[0]*1000,2)
    average = round(statistics.mean(calc_time)*1000,2)
    print(f"longest time: {longest}ms shortest time: {shortest}ms average time: {average}ms")

    # Close the display --- neded if we are going to have multiple runs.
    display.close()

# Since we explicitly named the main function
if __name__ == "__main__":
    main()
