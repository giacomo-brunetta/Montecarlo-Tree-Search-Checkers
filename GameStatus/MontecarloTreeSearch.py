from GameStatus.Node import Node as Node
from GameStatus.Game import Game

from typing import Type
from random import random
from math import sqrt, log
from time import time
from multiprocessing import Pool

class MontecarloTreeSearch(Node):
    __maxSeconsPerMove= 3
    __verbose = False

    def __init__(self, father: Type['MontecarloTreeSearch'],obj: Type['Game'], levelsOfMemory: int, numPlayers: int, height: int, turn: int, probability: float):
        assert levelsOfMemory>=0, "error in MontecarloTreeSearch construction"
        assert height>=0, "error in MontecarloTreeSearch construction"
        assert numPlayers>0
        assert obj is not None, "error in MontecarloTreeSearch construction"
        super().__init__(obj,father)
        
        self.__n= levelsOfMemory #keep in memory about 10^4 Board
        self.__numPlayers= numPlayers
        self.__height= height
        self.__turn= turn
        self.__wons= 0
        self.__losses= 0
        self.__stalemate= 0
        self.__probability= 0
        self.setProbability(probability)
        if height==0:
            self.populateNLevelsTree(self.__n)

    @classmethod
    def verbosity(cls, value: bool):
        assert type(value) is bool
        cls.__verbose = value

    def populateTreeLevel(self) -> None:
        #if self.__verbose==True:
        #    print(f"deb: popolo i figli del livello h={self.__height} turno={self.__turn}")
        assert len(self.getChildren()) == 0, "method to populate tree already called on this instance of the board"
        moves= self.getValue().moves(self.__turn)
        if len(moves)!=0:
            prob= 1/len(moves)
            for possibleMove in moves:
                self.newChild(MontecarloTreeSearch(self,possibleMove,self.__n-1,self.__numPlayers, self.__height+1, (self.__turn+1)%self.__numPlayers, prob))
            
    def populateNLevelsTree(self, n: int) -> None:
        #if self.__verbose==True:
        #    print(f"deb: popolo n={n} livelli sotto di figli")
        if n > 0:
            self.populateTreeLevel()
            for child in self.getChildren():
                child.populateNLevelsTree(n-1)

    @classmethod
    def setSecPerMove(cls,t: float) -> None:
        assert t>=0.1
        cls.__maxSeconsPerMove= t
    
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
        return 30*self.getValue().getBranchingFactor()**self.__n
    
    def setProbability(self, p: float):
        assert p>=0 and p<=1, "probability out of bound, cant have a negative or grater than one probability"
        self.__probability= p
    
    def explorationExploitationF(self, li: int, ni: int, Ni: int, c: float =sqrt(2)) -> float:
        assert Ni>=ni and ni>=0 and ni>=li and c>=0, f"impossible parameters, no meaning wi={li} ni={ni} Ni={Ni} c={c}"
        return (li/(ni+1)+c*sqrt(log(Ni+1)/(ni+1)))

    def __refreshProbabilityes(self):
        if len(self.getChildren())==0:
            print(f"h={self.__height} No refresh because no chile from where to take date")
        if self.getNumSimulation()>0:
            sum=0
            newValues= []
            for child in self.getChildren():
                v= self.explorationExploitationF(child.getLosses(), child.getNumSimulation(), self.getNumSimulation())
                assert v!=0, "exploration exploitation formula, returned 0, error"
                sum+= v
                newValues.append(v)
            #normalize to get a probability
            for child, v in zip(self.getChildren(),newValues):
                child.setProbability(v/sum)
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

    def randomVisitAndSave(self, n: int, myTurn: int) -> int: #return the end game player number and 1 if winner, -1 if looser and 0 if stalemate
        assert n>0, "you must have at least one layer of memory (n=1) to chose the next move"
        assert self.__height>=0, "Negative node height, problem in node creation"
        assert myTurn>=0 and myTurn<self.__numPlayers
        
        if self.__height>=0 and self.__height<n:
            #scegli uno a caso U in base alle probabilità
            r= random()
            probIntervalBottom= 0
            probIntervalTop= 0
            chosenChild= None
            #print(f"deb:-----------------------------------have {len(self.getChildren())} child")
            for child in self.getChildren():
                probIntervalTop+= child.getProbability()
                if probIntervalBottom<=r and r<probIntervalTop:
                    chosenChild= child
                    break
                probIntervalBottom= probIntervalTop
            #randomvisit U
            #print(f"deb-------------chosen child:\n{chosenChild}")
            if chosenChild is None: #"No child found for this node. Lost."
                if self.verbosity==True:
                    print("deb:------------ there MIGHT be an error, chosenChild is None.")
                return myTurn%self.__numPlayers, -1
            whoEndedGame, didWin= chosenChild.randomVisitAndSave(n,(myTurn+1)%self.__numPlayers)
            self.__updateStatus(myTurn, whoEndedGame, didWin)
            self.__refreshProbabilityes()
            return whoEndedGame, didWin
        elif self.__height==n:#itertive simulation without memory saves in the tree
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

    def chooseChild(self, children) -> Type["MontecarloTreeSearch"]:
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
        return worstChild


    def simulate(self, turn: int) -> Type['MontecarloTreeSearch']:
        # run simulation until seconds per moves are expired
        startTime= time()
        for i in range(self.getMinSimulations()):
            self.randomVisitAndSave(self.__n, turn%self.__numPlayers)
        # con i tempi: te giochi e mi fai il numero minimo di mosse per essere accourato con quel
        # numero n di livelli di memoria poi, controlli se hai passato il limite di tempo, se non lo hai
        # passato, continua a simulare finché non passi il tempo
        while(time()-startTime<self.__maxSeconsPerMove):
            self.randomVisitAndSave(self.__n, turn%self.__numPlayers)
        print(f"Time used: {time()-startTime}sec")

        if self.__verbose==True:
            print("mts-deb-simulation results:---------------------------------------")
            print(f"mts-deb:  h={self.__height}  played={self.getNumSimulation()} W={self.getWons()} s={self.__stalemate} L={self.__losses} Prob={round(self.getProbability(),2)}")
            for child in self.getChildren():
                print(f" mts-deb:  h={child.__height} played={child.getNumSimulation()} W={child.getWons()} s={child.__stalemate} L={child.__losses} Prob={round(child.getProbability(),2)}"+(" <-- <-- chosen!" if child is worstChild else " "))
                for child2 in child.getChildren():
                    print(f"    mts-deb:  h={child2.__height} played={child2.getNumSimulation()} W={child2.getWons()} s={child2.__stalemate} L={child2.__losses} Prob={round(child2.getProbability(),2)}")
                    #for child3 in child2.getChildren():
                    #    print(f"    mts-deb:  h={child3.__height}  played={child3.getNumSimulation()} W={child3.getWons()} s={child3.__stalemate} L={child3.__losses} Prob={round(child3.getProbability(),2)}")
            #print(f"mts-deb: chosen child: played={worstChild.getNumSimulation()} W={worstChild.getWons()} s={worstChild.__stalemate} L={worstChild.__losses} Prob={round(worstChild.getProbability(),2)}")
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
            return self.chooseChild(level1).getValue().copy()

def simulate_wrapper(node, turn):
    return node.simulate(turn)