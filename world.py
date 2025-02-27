# world.py
#
# A file that represents the Wumpus World, keeping track of the
# position of all the objects: pits, Wumpus, gold, and the agent, and
# moving them when necessary.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

import random
import config
import utils
from utils import Pose
from utils import Directions
from utils import State

class World():

    def __init__(self):

        # Import boundaries of the world. because we index from 0,
        # these are one less than the number of rows and columns.
        self.maxX = config.worldLength - 1
        self.maxY = config.worldBreadth - 1

        # Keep a list of locations that have been used.
        self.locationList = []

        # Wumpus locations within the world
        self.wLoc = []
        for i in range(config.numberOfWumpus):
            newLoc = utils.pickUniquePose(self.maxX, self.maxY, self.locationList)
            self.wLoc.append(newLoc)
            self.locationList.append(newLoc)

        # Link location
        newLoc = utils.pickUniquePose(self.maxX, self.maxY, self.locationList)
        self.lLoc = newLoc
        self.locationList.append(newLoc)

        # Gold location
        self.gLoc = []
        for i in range(config.numberOfGold):
            newLoc = utils.pickUniquePose(self.maxX, self.maxY, self.locationList)
            self.gLoc.append(newLoc)
            self.locationList.append(newLoc)

        # Pit locations
        self.pLoc = []
        for i in range(config.numberOfPits):
            newLoc = utils.pickUniquePose(self.maxX, self.maxY, self.locationList)
            self.pLoc.append(newLoc)
            self.locationList.append(newLoc)

        # Game state
        self.status = State.PLAY

        # Did Link just successfully loot some gold?
        self.looted = False
        
    #
    # Access Methods
    #
    # These are the functions that can be used by Link to access
    # information about the world though since Link has direct access
    # to the work they can just directly read and change attributes.

    # Where is/are the Wumpus?
    def getWumpusLocation(self):
        return self.wLoc

    # Where is Link?
    def getLinkLocation(self):
        return self.lLoc

    # Where is the Gold?
    def getGoldLocation(self):
        return self.gLoc

    # Where are the Pits?
    def getPitsLocation(self):
        return self.pLoc

    # Did we just loot some gold?
    def justLooted(self):
        return self.looted

    # What is the current game state?
    def getGameState(self):
        return self.status

    # Does Link feel the wind?
    def linkWindy(self):
        return self.isWindy(self.lLoc)

    # Does Link smell the Wumpus?
    def linkSmelly(self):
        return self.isSmelly(self.lLoc)

    # Does Link see the glitter?
    def linkGlitter(self):
        return self.isGlitter(self.lLoc)
 
    #
    # Methods
    #
    # These are the functions that are used to update and report on
    # world information to game.py and puzzle.py

    # Has the game come to an end?
    def isEnded(self):
        dead = False
        won = False
        # Has Link met the Wumpus?
        for i in range(len(self.wLoc)):
            if utils.sameLocation(self.lLoc, self.wLoc[i]):
                print("Oops! Met the Wumpus at [", self.lLoc.x, ',', self.lLoc.y, "]")
                dead = True
                self.status = State.LOST
                
        # Did Link fall in a Pit?
        for i in range(len(self.pLoc)):
            if utils.sameLocation(self.lLoc, self.pLoc[i]):
                print("Arghhhhh! Fell in a pit at [", self.lLoc.x, ',', self.lLoc.y, "]")
                dead = True
                self.status = State.LOST

        # Did Link loot all the gold?
        if len(self.gLoc) == 0:
            won = True
            self.status = State.WON
            
        if dead == True or won == True:
            print("Game Over!")
            return True
            
    # Implements the move chosen by Link
    def updateLink(self, direction):
        # Set the looted flag to False
        self.looted = False
        # Implement non-determinism if appropriate
        direction = self.probabilisticMotion(direction)
        if direction == Directions.NORTH:
            if self.lLoc.y < self.maxY:
                self.lLoc.y = self.lLoc.y + 1
            
        if direction == Directions.SOUTH:
            if self.lLoc.y > 0:
                self.lLoc.y = self.lLoc.y - 1
                
        if direction == Directions.EAST:
            if self.lLoc.x < self.maxX:
                self.lLoc.x = self.lLoc.x + 1
                
        if direction == Directions.WEST:
            if self.lLoc.x > 0:
                self.lLoc.x = self.lLoc.x - 1

        # Did Link just loot some gold?
        match = False
        index = 0
        for i in range(len(self.gLoc)):
            if utils.sameLocation(self.lLoc, self.gLoc[i]):
                match = True
                index = i
                self.looted = True
                print("Gold, yeah!")

        # Assumes that golds have different locations. Or, that only
        # one gold can be picked up in a given turn.
        if match:
            self.gLoc.pop(index)

    # Implement nondeterministic motion, if appropriate. This is not
    # really used at the moment.
    def probabilisticMotion(self, direction):
        if config.nonDeterministic:
            dice = random.random()
            if dice < config.directionProbability:
                return direction
            else:
                return self.sideMove(direction)
        else:
            return direction
        
    # Move at 90 degrees to the original direction.
    def sideMove(self, direction):
        # Do we head left or right of the intended direction?
        dice =  random.random()
        if dice > 0.5:
            left = True
        else:
            left = False
        if direction == Directions.NORTH:
            if left:
                return Directions.WEST
            else:
                return Directions.EAST

        if direction == Directions.SOUTH:
            if left:
                return Directions.EAST
            else:
                return Directions.WEST

        if direction == Directions.WEST:
            if left:
                return Directions.SOUTH
            else:
                return Directions.NORTH

        if direction == Directions.EAST:
            if left:
                return Directions.NORTH
            else:
                return Directions.SOUTH
            
    # Move the Wumpus if that is appropriate
    #
    # Need a decrementDifference function to tidy things up
    #
    def updateWumpus(self):
        if config.dynamic:
            for i in range(len(self.wLoc)):
                if utils.separation(self.wLoc[i], self.lLoc) < config.senseDistance:
                    self.moveToLink(i)
                else:
                    self.makeRandomMove(i)

    # Head towards Link 
    def moveToLink(self, i):
        target = self.lLoc
        # If same x-coordinate, move in the y direction
        if self.wLoc[i].x == target.x:
            self.wLoc[i].y = self.reduceDifference(self.wLoc[i].y, target.y)        
        # If same y-coordinate, move in the x direction
        elif self.wLoc[i].y == target.y:
            self.wLoc[i].x = self.reduceDifference(self.wLoc[i].x, target.x)        
        # If x and y both differ, approximate a diagonal
        # approach by randomising between moving in the x and
        # y direction.
        else:
            dice = random.random()
            if dice > 0.5:
                self.wLoc[i].y = self.reduceDifference(self.wLoc[i].y, target.y)        
            else:
                self.wLoc[i].x = self.reduceDifference(self.wLoc[i].x, target.x)        

    # Move value towards target.
    def reduceDifference(self, value, target):
        if value < target:
            return value+1
        elif value > target:
            return value-1
        else:
            return value

    # Randomly pick to change either x or y coordinate, and then
    # randomly make a change in that coordinate.
    def makeRandomMove(self, i):
        dice = random.random()
        if dice > 0.5:
            xChange = random.randint(0, 2) - 1
            self.wLoc[i].x = utils.checkBounds(self.maxX, self.wLoc[i].x - xChange)
        else:
            yChange = random.randint(0, 2) - 1
            self.wLoc[i].y = utils.checkBounds(self.maxY, self.wLoc[i].y - yChange)


    # Some additional information about the world which may be useful
    # for planning how to move Link.
    
    # Is the given location smelly?
    #
    # A location is smelly if it is next to the Wumpus
    def isSmelly(self, location):
        if self.isAjacent(self.wLoc, location):
            return True
        else:
            return False

    # Is the given location windy? 
    def isWindy(self, location):
        if self.isAjacent(self.pLoc, location):
            return True
        else:
            return False

     # Does the given location glitter? 
    def isGlitter(self, location):
        if self.isAjacent(self.gLoc, location):
            return True
        else:
            return False
                
    # Is the location loc next to any of the locations in locList.
    #
    # To be adjacent in this sense, you either have to be at the same
    # x coordinate and have a y coordinate that differs by 1, or in
    # the same y coordinate and have an x coordinate that differs by
    # one.
    def isAjacent(self,locList, loc):
        for aloc in locList:
            # Ajacency holds if it holds for any location in locList.
            if aloc.x == loc.x:
                if aloc.y == loc.y + 1 or aloc.y == loc.y - 1:
                    return True
                else:
                    return False
            elif aloc.y == loc.y:
                if aloc.x == loc.x + 1 or aloc.x == loc.x - 1:
                    return True
                else:
                    return False
            else:
                return False
            
