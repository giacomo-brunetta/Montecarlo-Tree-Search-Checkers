from GameStatus.Node import Node as Node
from GameStatus.Checkers import Checkers
from random import random

class MontecarloTreeSearch(Node):
    def __init__(self, obj: Checkers, isWhiteTurn: bool, height: int, probability: float):
        assert isinstance(obj, Checkers)
        super().__init__(obj)
        
        self.__isWhiteTurn= isWhiteTurn
        self.__height= height
        self.__wons= 0
        self.__losses= 0
        self.__stalemate= 0
        self.__probability= probability
    
    def getNumSimulation(self) -> int:
        return self.__wons + self.__losses + self.__stalemate
    
    def getProbability(self):
        return self.__probability
    
    def populateTreeLevel(self, whiteTurn: bool):
        assert len(self.__children) == 0, "metod to populate tree already called on this instance of the board"
        moves= self.__value.moves(whiteTurn)
        prob= 1/len(moves)
        for possibleMove in moves:
            self.newChild(MontecarloTreeSearch(possibleMove,not whiteTurn, self.__height+1, prob))
            
    def populateNLevelsTree(self, n: int):
        if n>0:
            self.populateTreeLevel(self.__isWhiteTurn)
            for child in self.__children:
                child.populateNLevelsTree(n-1)
    
    def randomVisitAndSave(self, n: int) -> int: #won? +1won white -1lost white 0 patta
        if self.__height>=0 and self.__height<n:
            #scegli uno a caso U in base alle probabilità
            r= random()
            probIntervalBottom= 0
            probIntervalTop= 0
            chosenMove= None
            for child in self.__children:
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
        elif self.__height>=40:
            return 0
        else:#altezza menouno significa che non è da salvare il risultato
            #farma un unico nodo a caso con la funzione di farming singola e crea un nodo di altezza ++
            nextBoard= self.__value.randomMove()
            #se il nodo farmato è None allora hai finito e ha perso isWhiteTurn quindi ritorni -1 se era bianco o +1 se nero
            if nextBoard==None:
                if self.__isWhiteTurn()==True:
                    return -1
                else:
                    return 1
            #altrimenti chiami sul nodo che hai ottenuto randomVisitAndSave
            MontecarloTreeSearch(nextBoard, not self.__isWhiteTurn, self.__height+1, None).randomVisitAndSave(n)



    


