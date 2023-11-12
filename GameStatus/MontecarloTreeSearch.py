from GameStatus.Node import Node as Node
from GameStatus.Game import Game
from GameStatus.Checkers import Checkers

from typing import Type
from random import random
from math import sqrt, log
from time import time



class MontecarloTreeSearch(Node):
    n= 4 #keei in memory about 10^4 Board
    seconsPerMove= 30

    def explorationExploitationF(wi: int, ni: int, Ni: int, c: float =sqrt(2)):
        assert Ni>=ni and ni>0 and ni>=wi, "impossible parameters, no meaning"
        return wi/ni+c*sqrt(log(Ni)/ni)
    
    def populateTreeLevel(self, whiteTurn: bool):
        assert len(self.getChildren()) == 0, "metod to populate tree already called on this instance of the board"
        moves= self.getValue().moves(whiteTurn)
        prob= 1/len(moves)
        for possibleMove in moves:
            self.newChild(MontecarloTreeSearch(possibleMove,not whiteTurn, self.__height+1, prob))
            
    def populateNLevelsTree(self, n: int):
        if n>0:
            self.populateTreeLevel(self.__isWhiteTurn)
            for child in self.getChildren():
                child.populateNLevelsTree(n-1)

    def __init__(self, obj: Game, isWhiteTurn: bool, height: int, probability: float):
        assert isinstance(obj, Game)
        super().__init__(obj)
        
        self.__isWhiteTurn= isWhiteTurn
        self.__height= height
        self.__wons= 0
        self.__losses= 0
        self.__stalemate= 0
        self.__probability= probability
        self.populateNLevelsTree(self.n)
    
    def getNumSimulation(self) -> int:
        return self.__wons + self.__losses + self.__stalemate
    
    def getWons(self) -> int:
        return self.__wons

    def getProbability(self) -> float:
        return self.__probability
    
    def setProbability(self, p: float):
        assert p>=0 and p<=1, "probability out of bound, cant have a negative or grater than one probability"
        self.__probability= p
  
    def __refreshProbabilityes(self):
        if self.getNumSimulation()>0:
            sum=0
            newValues= []
            for child in self.getChildren():
                if child.getNumSimulation()>0:
                    v= self.explorationExploitationF(child.getWons(), child.getNumSimulation(), self.getNumSimulation())
                else:
                    v= child.getProbability()
                sum+= v
                newValues.append(v)
            #normalize to get a probability
            for v, child in zip(self.getChildren(),newValues):
                child.setProbability(v/sum)
        
    def randomVisitAndSave(self, n: int) -> int: #won? +1won white -1lost white 0 patta
        if self.__height>=0 and self.__height<n:
            #scegli uno a caso U in base alle probabilità
            r= random()
            probIntervalBottom= 0
            probIntervalTop= 0
            chosenMove= None
            self.__refreshProbabilityes()
            for child in self.getChildren():
                probIntervalTop+= child.getProbability()
                if probIntervalBottom<=r and r<probIntervalTop:
                    chosenChild= child
                    break
                probIntervalBottom= probIntervalTop
            #randomvisit U
            result= chosenChild.randomVisitAndSave(n)
            #se true incrementa le tue vincite, se false le tue perdite
            if result==0:
                self.__stalemate +=1
            elif (result==1 and self.__isWhiteTurn()==True) or (result==-1 and self.__isWhiteTurn()==False):
                self.__wons+= 1
            elif (result==-1 and self.__isWhiteTurn()==True) or (result==1 and self.__isWhiteTurn()==False):
                self.__losses+= 1
            else:
                raise Exception("unmanaged case in winnings and losses")
            return result
        elif self.__height>=80:#sarebbe 40 da quando non varia più il numero dei pezzi ma pace
            return 0
        else:#altezza menouno significa che non è da salvare il risultato
            #farma un unico nodo a caso con la funzione di farming singola e crea un nodo di altezza ++
            nextBoard= self.getValue().randomMove()
            #se il nodo farmato è None allora hai finito e ha perso isWhiteTurn quindi ritorni -1 se era bianco o +1 se nero
            if nextBoard==None:
                if self.__isWhiteTurn()==True:
                    return -1
                else:
                    return 1
            #altrimenti chiami sul nodo che hai ottenuto randomVisitAndSave
            MontecarloTreeSearch(nextBoard, not self.__isWhiteTurn, self.__height+1, None).randomVisitAndSave(n)

    def findNextBestMoove(self) -> Type['Game']:
        # run simulation untill seconds per moves are expired
        startTime= time()
        while True:
            self.randomVisitAndSave(self.n)
            if time() > startTime+self.seconsPerMove:
                break
        #I choose the more winning move above all the childs
        bestChild= None
        for child in self.getChildren():
            if bestChild!=None:
                if child.getWons() > bestChild.getWons():
                    bestChild= child
            else:
                bestChild= child
        return bestChild.copy()
    