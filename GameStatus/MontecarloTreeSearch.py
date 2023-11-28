from GameStatus.Node import Node as Node
from GameStatus.Game import Game

from typing import Type
from random import random
from math import sqrt, log
from time import time
from multiprocessing import Pool

class MontecarloTreeSearch(Node):
    __minSeconsPerSimulation= 3
    __verbose = False

    def __init__(self,obj: Type['Game'], levelsOfMemory: int, numPlayers: int, height: int, turn: int, probability: float):
        assert levelsOfMemory>=0, "error in MontecarloTreeSearch construction"
        assert height>=0, "error in MontecarloTreeSearch construction"
        assert numPlayers>=1
        super().__init__(obj)
        self.__n= levelsOfMemory
        self.__numPlayers= numPlayers
        self.__height= height
        self.__turn= turn
        self.__wons= 0
        self.__losses= 0
        self.__stalemate= 0
        self.__probability= 0
        self.__setProbability(probability)
        if height==0:
            self.__populateNLevelsTree(self.__n)

    def __populateTreeLevel(self) -> None:
        assert len(self.getChildren()) == 0, "method to populate tree already called on this instance of the board"
        moves= self.getValue().moves(self.__turn)
        if len(moves)!=0:
            prob= 1/len(moves)
            for possibleMove in moves:
                self.newChild(MontecarloTreeSearch(possibleMove,self.__n-1,self.__numPlayers, self.__height+1, (self.__turn+1)%self.__numPlayers, prob))
            
    def __populateNLevelsTree(self, n: int) -> None:
        if n > 0:
            self.__populateTreeLevel()
            for child in self.getChildren():
                child.__populateNLevelsTree(n-1)

    @classmethod
    def setVerbosity(cls, value: bool):
        assert type(value) is bool
        cls.__verbose = value

    @classmethod
    def setSecPerMove(cls,t: float) -> None:
        assert t>=0
        cls.__minSeconsPerSimulation= t
    
    def getNumSimulation(self) -> int:
        return self.__wons + self.__losses + self.__stalemate
    
    def getWons(self) -> int:
        return self.__wons

    def getLosses(self) -> int:
        return self.__losses

    def getStalemate(self):
        return self.__stalemate

    def getProbability(self) -> float:
        return self.__probability

    def getMinSimulations(self) -> int:
        return 11*self.getValue().getBranchingFactor()**self.__n
    
    def __setProbability(self, p: float):
        assert p>=0 and p<=1, "probability out of bound, cant have a negative or grater than one probability"
        self.__probability= p
    
    def __explorationExploitationF(self, li: int, ni: int, Ni: int, c: float =sqrt(2)) -> float:
        assert Ni>=ni and ni>=0 and ni>=li and c>=0, f"impossible parameters, no meaning wi={li} ni={ni} Ni={Ni} c={c}"
        return (li/(ni+1)+c*sqrt(log(Ni+1)/(ni+1)))

    def __refreshProbabilityes(self):
        if len(self.getChildren())==0:
            print(f"h={self.__height} No refresh because no childe from where to take date")
        if self.getNumSimulation()>0:
            sum=0
            newValues= []
            for child in self.getChildren():
                v= self.__explorationExploitationF(child.getLosses(), child.getNumSimulation(), self.getNumSimulation())
                assert v!=0, "exploration exploitation formula, returned 0, error"
                sum+= v
                newValues.append(v)
            #normalize to get a probability
            for child, v in zip(self.getChildren(),newValues):
                child.__setProbability(v/sum)
        else:
            raise Exception("can not refresh probabilityes before running a simulation")
    
    def __updateStatus(self,myActualTurn: int, whoEndedGame: int, didWin: int):
        if didWin==0:
            self.__stalemate+= 1
        elif (didWin==1 and myActualTurn%self.__numPlayers==whoEndedGame) or (didWin==-1 and myActualTurn%self.__numPlayers!=whoEndedGame):#i won or i wosn't the one who lost
            self.__wons+= 1
        elif (didWin==-1 and myActualTurn%self.__numPlayers==whoEndedGame) or (didWin==1 and myActualTurn%self.__numPlayers!=whoEndedGame):#i lost ore someone else won
            self.__losses+= 1
        else:
            raise Exception(f"unmanaged case in winnings and losses. myActualTurn={myActualTurn}, whoEndedGame={whoEndedGame}, didWin={didWin}")

    def __randomVisitAndSave(self, n: int, myTurn: int) -> int: #return the end game player number and 1 if winner, -1 if looser and 0 if stalemate
        assert n>=0, f"you must have at least one layer of memory (n=1) to chose the next move, now n={n}"
        assert self.__height>=0, "Negative node height, problem in node creation"
        assert myTurn>=0 and myTurn<self.__numPlayers
        
        if self.__height>=0 and self.__height<n+1:
            #choose a child at random based on probability
            r= random()
            probIntervalBottom= 0
            probIntervalTop= 0
            chosenChild= None
            for child in self.getChildren():
                probIntervalTop+= child.getProbability()
                if probIntervalBottom<=r and r<probIntervalTop:
                    chosenChild= child
                    break
                probIntervalBottom= probIntervalTop
                
            if chosenChild is None: #"No child found for this node. Lost."
                if self.__verbose==True:
                    print("deb:------------ there MIGHT be an error, chosenChild is None.")
                return myTurn%self.__numPlayers, -1
            whoEndedGame, didWin= chosenChild.__randomVisitAndSave(n,(myTurn+1)%self.__numPlayers)
            self.__updateStatus(myTurn, whoEndedGame, didWin)
            self.__refreshProbabilityes()
            return whoEndedGame, didWin
        elif self.__height==n+1:#itertive simulation without memory saves in the tree
            count= self.__height
            turn= myTurn
            nextBoard= self.getValue().randomMove(myTurn)
            while count<80 and nextBoard is not None:
                count+= 1
                turn= (turn+1)%self.__numPlayers
                nextBoard= nextBoard.randomMove(turn) #random farm board to randomly evolve the game
            whoEndedGame= turn%self.__numPlayers
            if count==80:#Stalemate case
                didWin= 0
            elif nextBoard is None:#the turn player lost
                didWin= -1
            else:
                raise Exception("unmanaged case in while cicle no-memory simulations")
            self.__updateStatus(myTurn, whoEndedGame, didWin)
            return whoEndedGame, didWin
        else:
            raise Exception(f"unmanaged case in winnings tree visit, heigth={self.__height}")

    def __chooseChild(self, children) -> Type["MontecarloTreeSearch"]:
        worstChild = None
        for child in children:
            if worstChild is not None:
                if child.getLosses() > worstChild.getLosses():
                    worstChild = child
                else:
                    if child.getLosses() == worstChild.getLosses() and child.getStalemate() > worstChild.getStalemate():
                        worstChild = child
            else:
                worstChild = child
        if self.__verbose == True:
            print(f"mts-deb: chosen child: played={worstChild.getNumSimulation()} W={worstChild.getWons()} s={worstChild.__stalemate} L={worstChild.__losses} Prob={round(worstChild.getProbability(),2)}")
        return worstChild

    def simulate(self, turn: int) -> Type['MontecarloTreeSearch']:
        startTime= time()
        # run simulation for a minimum amount of moves
        for i in range(self.getMinSimulations()):
            self.__randomVisitAndSave(self.__n, turn%self.__numPlayers)
        # keep simulating until seconds per moves are expired
        while(time()-startTime<self.__minSeconsPerSimulation):
            self.__randomVisitAndSave(self.__n, turn%self.__numPlayers)
        
        if self.__verbose==True:
            print(f"Time used: {time()-startTime}sec")
            print("mts-deb-simulation results:---------------------------------------")
            print(f"mts-deb:  h={self.__height}  played={self.getNumSimulation()} W={self.getWons()} s={self.__stalemate} L={self.__losses} Prob={round(self.getProbability(),2)}")
            for child in self.getChildren():
                print(f" mts-deb:  h={child.__height} played={child.getNumSimulation()} W={child.getWons()} s={child.__stalemate} L={child.__losses} Prob={round(child.getProbability(),2)}")
                for child2 in child.getChildren():
                    print(f"    mts-deb:  h={child2.__height} played={child2.getNumSimulation()} W={child2.getWons()} s={child2.__stalemate} L={child2.__losses} Prob={round(child2.getProbability(),2)}")
        return self

    def move(self, turn: int) -> Type['Game']:
        children = self.getChildren()
        if len(children)==1:
            return children[0].getValue().copy()
        elif len(children)==0:
            return None
        else:
            with Pool(len(children)) as p:
                level1 = p.starmap(simulate_wrapper, [(child, turn+1) for child in children])
            return self.__chooseChild(level1).getValue().copy()


def simulate_wrapper(node, turn):
    return node.simulate(turn)