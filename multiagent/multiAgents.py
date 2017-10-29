# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from fileinput import close
from audioop import minmax

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        #print successorGameState.getScore()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        thresholdDistance = 3                                       #A threshold distance for Ghost.
        
        minGhost =100000
        for ghost in newGhostStates:
            ghostDist = manhattanDistance(newPos, ghost.configuration.getPosition())
            if(ghostDist<thresholdDistance):                        #If Manhattan distance is less than threshold distance than this state is bad
                return -100                                         #return a high negative value
            if ghostDist<minGhost:
                minGhost = ghostDist
        
        closestFood =1000
        for food in newFood.asList():
            foodDist = manhattanDistance(newPos, food)              #Calculate the Manhattan distance and get the closest food
            if(foodDist ==0):                                           
                foodDist = 1
            if(foodDist<closestFood):
                closestFood = foodDist

        return successorGameState.getScore()+(1.0/closestFood)-(1.0/minGhost)      #Final score is sum of score, reciprocal of closest food and deducting the closest ghost distance 

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def minMax(self, gameState,index):
        l = []
        #Terminal state when it is a win state, lose state or index is max depth of trees
        if index == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return ('',self.evaluationFunction(gameState))
        
        else:
            # We generate the newGameStates for all legal actions and calculate the respective MinMax value
            for action in gameState.getLegalActions(index%gameState.getNumAgents()):
                newGameState = gameState.generateSuccessor(index%gameState.getNumAgents(), action)
                direction,val = self.minMax(newGameState, index+1)          #Sending in the next index as we are going one level down
                l.append((action,val))                                      #We append the legal moves and the value calculated 
            if(index%gameState.getNumAgents() ==0):                         #Max state will be when the modulo of index to numAgents is 0
                maxValue = -1000                
                maxAction = 0
                for action,value in l:                                      #Calculating the MAX value and action and returning it to the next stage
                    if value>maxValue:
                        maxValue = value
                        maxAction = action
                return (maxAction,maxValue)
            else:
                minValue = 10000                                            #Min states will be the remaining states when Ghost moves 
                minAction = 0
                for action,value in l:                                      #Calculating the MIN value and action and returning it to the next stage
                    if value<minValue:
                        minValue = value
                        minAction = action
                return (minAction,minValue)
    
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        direction,value = self.minMax(gameState, self.index)
        return direction
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def maxValue(self, gameState, alpha, beta, index):
        val = -1000000
        maxAction = 0
        for action in gameState.getLegalActions(index%gameState.getNumAgents()):
            newGameState = gameState.generateSuccessor(index%gameState.getNumAgents(), action)
            direction,value = self.getVal(newGameState, alpha, beta, index+1)
            if(value>=val):
                val = value
                maxAction = action
            if val > beta:                                  #If current value is greater than beta then we prune the remaining branches and return the value 
                return (action,val)
            alpha = max(val,alpha)                          #We keep updating alpha at each step to max of alpha and the current value
        return (maxAction,val)
    
    def minValue(self, gameState, alpha, beta, index):
        val = 1000000
        minAction = 0
        for action in gameState.getLegalActions(index%gameState.getNumAgents()):
            newGameState = gameState.generateSuccessor(index%gameState.getNumAgents(), action)
            direction,value = self.getVal(newGameState, alpha, beta, index+1)
            if(value<=val):
                val = value
                minAction = action
            if val < alpha:                                 # if current value is less than alpha we prune the remaining branches and return the value
                return (action,val) 
            beta = min(val,beta)                            # We keep updating beta at each step to the min of beta and current value                        
        return (minAction,val)
    
    
    def getVal(self, gameState, alpha, beta, index):
        #Depending if it is a terminal state or MAX or min state we make the respective function calls
        if index == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return ('',self.evaluationFunction(gameState))
        if(index%gameState.getNumAgents()==0):
            return self.maxValue(gameState, alpha, beta, index)
        else:
            return self.minValue(gameState, alpha, beta, index)
            
    
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        direction,value = self.getVal(gameState, -100000, 1000000, self.index)
        return direction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectiMax(self, gameState,index):
        l = []
        #Terminal state when it is a win state, lose state or index is max depth of trees
        if index == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return ('',self.evaluationFunction(gameState))
        
        else:
            # We generate the newGameStates for all legal actions and calculate the respective MinMax value
            for action in gameState.getLegalActions(index%gameState.getNumAgents()):
                newGameState = gameState.generateSuccessor(index%gameState.getNumAgents(), action)
                direction,val = self.expectiMax(newGameState, index+1)          #Sending in the next index as we are going one level down
                l.append((action,val))                                          #We append the legal moves and the value calculated 
            if(index%gameState.getNumAgents() ==0):                             #Max state will be when the modulo of index to numAgents is 0
                maxValue = -1000.0                
                maxAction = 0
                for action,value in l:  
                    if value>maxValue:                                           #Calculating the MAX value and action and returning it to the next stage          
                        maxValue = value
                        maxAction = action
                return (maxAction,maxValue)
            else:
                minAction = ''
                sumValue = float(len(l))
                valueSum =0.0
                for action,value in l:
                    valueSum = valueSum + value                                 #Calculating the sum over all values and then dividing by all branches to get the expectimax value 
                minValue = valueSum/sumValue            
                return (minAction,minValue)
            
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        direction,value = self.expectiMax(gameState, self.index)
        return direction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

