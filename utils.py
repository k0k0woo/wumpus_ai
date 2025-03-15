# utils.py
#
# Some bits and pieces that are used in different places in the Wumpus
# world code.
#
# 
# Written by: Simon Parsons
# Last Modified: 18/12/24

import random
import math
import copy
from enum import Enum

# Representation of directions.
#
# Note that NORTH is interpreted as the
# direction of increasing y, and graphics.py interprets increasing y
# as downwards in the grid.
class Directions(Enum):
    NORTH = 1
    SOUTH = 2
    EAST  = 3
    WEST  = 4

# representation of game state
class State(Enum):
    PLAY = 0
    WON  = 1
    LOST = 2

# Class to represent the position of elements within the game
class Pose():
    x = 0
    y = 0
    cost = 0
    def __lt__(self, other):
        return self.cost < other.cost
    def __gt__(self, other):
        return self.cost > other.cost
    def print(self):
        print('Cost:',self.cost,'[', self.x, ',', self.y, ']')

# Check if two game elements are in the same location
def sameLocation(pose1, pose2):
    if pose1.x == pose2.x:
        if pose1.y == pose2.y:
            return True
        else:
            return False
    else:
        return False

# Define the order over two locations/poses by distance from
# origin. Helpful if we need to sort them and only care about having a
# unique order.
def ltPose(pose):
    origin = Pose()
    return separation(pose, origin)
    
# Return distance between two game elements.
def separation(pose1, pose2):
    return math.sqrt((pose1.x - pose2.x) ** 2 + (pose1.y - pose2.y) ** 2)

# Make sure that a location doesn't step outside the bounds on the world.
def checkBounds(max, dimension):
    if (dimension > max):
        dimension = max
    if (dimension < 0):
        dimension = 0

    return dimension

# Pick a location in the range [0, x] and [0, y]
#
# Used to randomize the initial conditions.
def pickRandomPose(x, y):
    p = Pose()
    p.x = random.randint(0, x)
    p.y = random.randint(0, y)

    return p

# Pick a unique location, in the range [0, x] and [0, y], given a list
# of locations that have already been chosen.
def pickUniquePose(x, y, taken):
    uniqueChoice = False
    while(not uniqueChoice):
        candidatePose = pickRandomPose(x, y)
        # Don't seem to be able to use 'in' here. I suspect it is
        # because of the way __contains__ checks for equality.
        if not containedIn(candidatePose, taken):
            uniqueChoice = True
    return candidatePose

# Check if a pose with the same x and y is already in poseList.
#
# There should be a way to do this with in/__contains__ by overloading
# the relevant equality operator for pose, but that is for another
# time.
def containedIn(pose, poseList):
    contained = False
    for poses in poseList:
        if sameLocation(pose, poses):
            contained = True
            #print(pose, "and", poses, "are (both) at (", pose.x, ",
            #", pose.y, ") and (", pose.x, ", ", pose.y, ")")
    return contained

# Print out game state information. Not so useful given
# the graphical display, but might come in handy.
def printGameState(world):
    print("Wumpus:")
    for i in range(len(world.getWumpusLocation())):
        world.getWumpusLocation()[i].print()
        
    print("Link:")
    world.getLinkLocation().print()

    print("Gold:")
    for i in range(len(world.getGoldLocation())):
        world.getGoldLocation()[i].print()

    print("Pits:")
    for i in range(len(world.getPitsLocation())):
        world.getPitsLocation()[i].print()

# Pick a random direction
def pickRandomDirection():
    direction = random.randint(0, 3)
    if direction == 0:
        return Directions.NORTH
    elif direction == 1:
        return Directions.SOUTH
    elif direction == 2:
        return Directions.EAST
    elif direction == 3:
        return Directions.WEST

# Check if two world objects are the same (helpful for the puzzle)
#
# We consider them to be the same if the locations of Link and the Wumpus
# (plural) are the same.
#
# Clearly this could be true for two worlds of different sizes, but we
# will ignore that possibility for now (we should only ever be
# comparing worlds of the same size).
def sameAs(state1, state2):
    if sameLink(state1, state2) and sameWumpus(state1, state2):
        return True
    else:
        return False
    
def sameLink(state1, state2):
    if sameLocation(state1.lLoc, state2.lLoc):
        return True
    else:
        return False
    
# The wumpus in two states are the same if for every wumpus in state1
# there is a wumpus with the same location in state 2. We need to sort
# by location to check this, and we need to create copies because sort
# has side-effects.
def sameWumpus(state1, state2):
    state3 = copy.deepcopy(state1)
    state4 = copy.deepcopy(state2)
    state3.wLoc.sort(key=ltPose)
    state4.wLoc.sort(key=ltPose)
    for i in range(len(state3.wLoc)):
        if not sameLocation(state3.wLoc[i], state4.wLoc[i]):
            return False
    return True
