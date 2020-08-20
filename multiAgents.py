# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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

  def evaluationFunction(self, currGameState, pacManAction):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    nextGameState = currGameState.generatePacmanSuccessor(pacManAction)
    newPos = nextGameState.getPacmanPosition()
    oldFood = currGameState.getFood()
    newGhostStates = nextGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    return nextGameState.getScore()

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
  def recurrentMiniMaxCalc(self, ghosts, currGameState):
      """

      :return:
      """
      min_scores = []
      index = ghosts[0]
      next_g_moves = currGameState.getLegalActions(index)
      # Movement when ghost doesn't move (empty list)
      if len(next_g_moves) == 0:
          if len(ghosts) == 1:
            return self.evaluationFunction(currGameState)
          else:
            return self.recurrentMiniMaxCalc(ghosts[1:], currGameState)
      else:
        for last_g_move in next_g_moves:
          last_state = currGameState.generateSuccessor(index, last_g_move)
          if len(ghosts) == 1:
              min_scores.append(self.evaluationFunction(last_state))
          else:
              min_scores.append(self.recurrentMiniMaxCalc(ghosts[1:], last_state))
        min_score = min(min_scores)
        return min_score
  def getAction(self, currGameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      currGameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      currGameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      currGameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"

    max_scores = []
    # Vinden van moves van PacMan
    pacman_moves = currGameState.getLegalActions(0)
    next_move = Directions.STOP
    # Alle ghosts indexen hebben (PacMan is steeds 0, de ghosts in increasing order vanaf 1
    ghosts = [iter + 1 for iter in range(3)]
    # Recurrent function
    for pacman_move in pacman_moves:
        # voor alle mogelijke moves van PacMan het maximum ondergaan, door eerst min staat van de ghosts te gaan berekenen
        next_state = currGameState.generateSuccessor(0, pacman_move)
        random.shuffle(ghosts)
        # met behulp van recurrent functie de minimax tree ondergaan
        max_scores.append(self.recurrentMiniMaxCalc(ghosts, next_state))
    max_move = max(max_scores)
    move_index = max_scores.index(max_move)
    return pacman_moves[move_index]



class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, currGameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def recurrentExpectimaxCalc(self, ghosts, currGameState):
      """

      :return:
      """
      min_scores = []
      index = ghosts[0]
      next_g_moves = currGameState.getLegalActions(index)
      if len(next_g_moves) == 0:
          # checken of dit niet de laatste staat mogelijk is
          if len(ghosts) == 1:
              return self.evaluationFunction(currGameState)
          else:
              # Returnt naar de volgende staten
              return self.recurrentExpectimaxCalc(ghosts[1:], currGameState)
      else:
          # Alle staten nagaan van alle mogelijke moves van de ghosts
          for last_g_move in next_g_moves:
              last_state = currGameState.generateSuccessor(index, last_g_move)
              if len(ghosts) == 1:
                  min_scores.append(self.evaluationFunction(last_state))
              else:
                  min_scores.append(self.recurrentExpectimaxCalc(ghosts[1:], last_state))   
          min_score = sum(min_scores)/len(min_scores)
          return min_score
  def getAction(self, currGameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    max_scores = []
    # Vinden van moves van PacMan
    pacman_moves = currGameState.getLegalActions(0)
    next_move = Directions.STOP
    # Alle ghosts indexen hebben (PacMan is steeds 0, de ghosts in increasing order vanaf 1
    ghosts = [iter + 1 for iter in range(currGameState.getNumAgents() - 1)]
    # voor alle mogelijke moves van PacMan  het minimum ondergaan
    for pacman_move in pacman_moves:
        # volgende staat volgens pacmans beweging
        next_state = currGameState.generateSuccessor(0, pacman_move)
        # positie van de ghosts moet random zijn
        random.shuffle(ghosts)
        # met behulp van recurrent functie de expectimax tree ondergaan, max waarde hiervan terugkrijgen
        # deze is de minimax waarde van de mogelijke PacMan moves.
        max_scores.append(self.recurrentExpectimaxCalc(ghosts, next_state))
    # Max PacMan movement terugkrijgen van de gevonden minimum waarden
    max_move = max(max_scores)
    move_index = max_scores.index(max_move)
    return pacman_moves[move_index]

def betterEvaluationFunction(currGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class GeneticAgent(MultiAgentSearchAgent):
    def __init__(self):
        util.raiseNotDefined()
    def getAction(self, state):
        util.raiseNotDefined()

