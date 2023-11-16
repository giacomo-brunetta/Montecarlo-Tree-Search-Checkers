from GameStatus.Node import Node as Node
from GameStatus.Game import Game
from GameStatus.Checkers import Checkers

from typing import Type
from random import random
from math import sqrt, log
from time import time


class MontecarloTreeSearch(Node):
    __seconsPerMove= 3
    __verbose = False

    def __init__(self, father: Type['MontecarloTreeSearch'],obj: Type['Game'], levelsOfMemory: int, isWhiteTurn: bool, height: int, probability: float):
        assert levelsOfMemory>=0, "error in MontecarloTreeSearch construction"
        assert height>=0, "error in MontecarloTreeSearch construction"
        assert obj is not None, "error in MontecarloTreeSearch construction"
        super().__init__(obj,father)
        
        self.__n= levelsOfMemory #keep in memory about 10^4 Board
        self.__isWhiteTurn= isWhiteTurn
        self.__height= height
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
        assert len(self.getChildren()) == 0, "method to populate tree already called on this instance of the board"
        moves= self.getValue().moves(self.__height)
        if len(moves)!=0:
            prob= 1/len(moves)
            for possibleMove in moves:
                self.newChild(MontecarloTreeSearch(self,possibleMove,self.__n-1,not self.__isWhiteTurn, self.__height+1, prob))
            
    def populateNLevelsTree(self, n: int) -> None:
        if n > 0:
            self.populateTreeLevel()
            for child in self.getChildren():
                child.populateNLevelsTree(n-1)

    @classmethod
    def setSecPerMove(cls,t: float) -> None:
        assert t>=0.1
        cls.__seconsPerMove= t
    
    def getNumSimulation(self) -> int:
        return self.__wons + self.__losses + self.__stalemate
    
    def getWons(self) -> int:
        return self.__wons

    def getLosses(self) -> int:
        return self.__losses

    def getProbability(self) -> float:
        return self.__probability
    
    def setProbability(self, p: float):
        assert p>=0 and p<=1, "probability out of bound, cant have a negative or grater than one probability"
        self.__probability= p
    
    def explorationExploitationF(self, li: int, ni: int, Ni: int, c: float =sqrt(2)) -> float:
        assert Ni>=ni and ni>=0 and ni>=li and c>=0, f"impossible parameters, no meaning wi={li} ni={ni} Ni={Ni} c={c}"
        return (li/(ni+1)+c*sqrt(log(Ni+1)/(ni+1)))

    def __refreshProbabilityes(self):
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
        
    def randomVisitAndSave(self, n: int) -> int: #won? +1won white -1lost white 0 patta
        assert n>0, "you must have at least one layer of memory (n=1) to chose the next move"
        assert self.__height>=0, "Negative node height, problem in node creation"
        if len(self.getChildren())==0: #"No child found for this node. Lost."
            if self.__isWhiteTurn==True:
                return -1
            else:
                return 1
        elif self.__height>=0 and self.__height<n:
            #scegli uno a caso U in base alle probabilità
            r= random()
            probIntervalBottom= 0
            probIntervalTop= 0
            chosenMove= None
            #print(f"deb:-----------------------------------have {len(self.getChildren())} child")
            for child in self.getChildren():
                probIntervalTop+= child.getProbability()
                if probIntervalBottom<=r and r<probIntervalTop:
                    chosenChild= child
                    break
                probIntervalBottom= probIntervalTop
            #randomvisit U
            #print(f"deb-------------chosen child:\n{chosenChild}")
            result= chosenChild.randomVisitAndSave(n)
            #print(f"deb-------------res={result}")
            #se true incrementa le tue vincite, se false le tue perdite
            if result==0:
                self.__stalemate +=1
            elif (result==1 and self.__isWhiteTurn==True) or (result==-1 and self.__isWhiteTurn==False):
                self.__wons+= 1
            elif (result==-1 and self.__isWhiteTurn==True) or (result==1 and self.__isWhiteTurn==False):
                self.__losses+= 1
            else:
                raise Exception(f"unmanaged case in winnings and losses. Res={result} isWhite={self.__isWhiteTurn}")
            self.__refreshProbabilityes()
            return result
        elif self.__height>=80:#sarebbe 40 da quando non varia più il numero dei pezzi ma pace
            return 0
        elif self.__height>=n and self.__height<80:#altezza menouno significa che non è da salvare il risultato
            #farma un unico nodo a caso con la funzione di farming singola e crea un nodo di altezza ++
            nextBoard= self.getValue().randomMove(self.__height)
            #se il nodo farmato è None allora hai finito e ha perso isWhiteTurn quindi ritorni -1 se era bianco o +1 se nero
            if nextBoard is None:
                if self.__isWhiteTurn==True:
                    return -1
                else:
                    return 1
            else:
                #altrimenti chiami sul nodo che hai ottenuto randomVisitAndSave
                return MontecarloTreeSearch(self,nextBoard, 0, not self.__isWhiteTurn, self.__height+1, 0).randomVisitAndSave(n)
        else:
            raise Exception(f"unmanaged case in winnings tree visit, heigth={self.__height}")

    def findNextBestMove(self) -> Type['Game']:
        children= self.getChildren()
        if len(children)==1:
            return children[0].getValue().copy()
        elif len(children)==0:
            return None
        else:
            # run simulation untill seconds per moves are expired
            startTime= time()
            while True:
                for i in range(50): #for50 because I don't want to wast CPU resources cecking the time after every simulation
                    self.randomVisitAndSave(self.__n)
                if time() > startTime+self.__seconsPerMove:
                    break
            #I choose the more winning move above all the childs
            worstChild= None
            for child in children:
                if worstChild is not None:
                    if child.getLosses() > worstChild.getLosses():
                        worstChild= child
                else:
                    worstChild= child
            if self.__verbose==True:
                print("mts-deb-simulation results:---------------------------------------")
                print(f"mts-deb:  h={self.__height} W={self.getWons()} s={self.__stalemate} L={self.__losses}")
                for child in children:
                    print(f" mts-deb:  h={child.__height} W={child.getWons()} s={child.__stalemate} L={child.__losses} Prob={round(child.getProbability(),2)}")
                    for child2 in children:
                        print(f"    mts-deb:  h={child2.__height} W={child2.getWons()} s={child2.__stalemate} L={child2.__losses} Prob={round(child2.getProbability(),2)}")
                
            return worstChild.getValue().copy()
    
    def move(self) -> Type['Game']:
        playerTurn= self.__isWhiteTurn
        mov= self.findNextBestMove()
        self.__isWhiteTurn= playerTurn
        return mov
    
    '''# for debug purpose to check if the deallocation is working. It is.
    def __del__(self):
        if self.__verbose==True:
            print(f"deb: Level {self.__height} ",end="")
            if self.__isWhiteTurn==True:
                print("white",end="")
            else:
                print("black",end="")
            print(" node destroyed")
    '''