import pyxel
from text import text
from forms import *

class Params :
    
    DIFFICULTY_EASY     = 8
    DIFFICULTY_MEDIUM   = 10
    DIFFICULTY_HARD     = 12
    TIME_SHORT          = 20
    TIME_MEDIUM         = 30
    TIME_LONG           = 45

    def __init__(self) :
        
        self.__size = Params.DIFFICULTY_MEDIUM
        self.__sizeRadiosGroup = RadiosGroup([
            Radio(153, 100, str(Params.DIFFICULTY_EASY) + " x " + str(Params.DIFFICULTY_EASY), Params.DIFFICULTY_EASY),
            Radio(234, 100, str(Params.DIFFICULTY_MEDIUM) + " x " + str(Params.DIFFICULTY_MEDIUM), Params.DIFFICULTY_MEDIUM, True),
            Radio(314, 100, str(Params.DIFFICULTY_HARD) + " x " + str(Params.DIFFICULTY_HARD), Params.DIFFICULTY_HARD),
        ], self.setSize)

        self.__timeByTurn = Params.TIME_MEDIUM
        self.__timeByTurnRadiosGroup = RadiosGroup([
            Radio(153, 140, str(Params.TIME_LONG) + '"', Params.TIME_LONG),
            Radio(234, 140, str(Params.TIME_MEDIUM) + '"', Params.TIME_MEDIUM, True),
            Radio(314, 140, str(Params.TIME_SHORT) + '"', Params.TIME_SHORT),
        ], self.setTimeByTurn)

        self.__validateButton = Button(256 - text.getLength("Commencer") // 2 - 12, 180, "Commencer", self.__close)

        self.__ready = False

    def setSize(self, size : int) :
        self.__size = size

    def getSize(self) :
        return self.__size

    def setTimeByTurn(self, timeByTurn : int) :
        self.__timeByTurn = timeByTurn

    def getTimeByTurn(self) :
        return self.__timeByTurn
    
    def isReady(self) :
        return self.__ready
    
    def open(self) :
        self.__ready = False

    def __close(self) :
        self.__ready = True

    def update(self) :
        self.__sizeRadiosGroup.update()
        self.__timeByTurnRadiosGroup.update()
        self.__validateButton.update()
        return self.__ready

    def draw(self) :
        pyxel.rectb(128, 30, 256, 196, 7)
        pyxel.rect(129, 31, 254, 194, 0)
        pyxel.bltm(178, 40, 0, 0, 0, 155, 18)
        text.draw(140, 80, "Taille de la grille :", 7)
        self.__sizeRadiosGroup.draw()
        text.draw(140, 120, "Temps par tour :", 7)
        self.__timeByTurnRadiosGroup.draw()
        self.__validateButton.draw()