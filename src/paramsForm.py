import pyxel
from src.text       import text
from src.forms      import *
from src.params     import Params

class ParamsForm :

    def __init__(self) :
        
        self.__params = Params()

        self.__rulesRadiosGroup = RadiosGroup([
            Radio(153, 90, "Normales", Params.RULES_NORMAL, True),
            Radio(234, 90, "Améliorées", Params.RULES_ENHANCED),
        ], self.__params.setRules)
        
        self.__sizeRadiosGroup = RadiosGroup([
            Radio(153, 130, str(Params.DIFFICULTY_EASY) + " x " + str(Params.DIFFICULTY_EASY), Params.DIFFICULTY_EASY),
            Radio(234, 130, str(Params.DIFFICULTY_MEDIUM) + " x " + str(Params.DIFFICULTY_MEDIUM), Params.DIFFICULTY_MEDIUM, True),
            Radio(314, 130, str(Params.DIFFICULTY_HARD) + " x " + str(Params.DIFFICULTY_HARD), Params.DIFFICULTY_HARD),
        ], self.__params.setSize)

        self.__timeByTurnRadiosGroup = RadiosGroup([
            Radio(153, 170, str(Params.TIME_LONG) + '"', Params.TIME_LONG),
            Radio(234, 170, str(Params.TIME_MEDIUM) + '"', Params.TIME_MEDIUM, True),
            Radio(314, 170, str(Params.TIME_SHORT) + '"', Params.TIME_SHORT),
        ], self.__params.setTimeByTurn)

        self.__validateButton = Button(256 - text.getLength("Commencer") // 2 - 12, 200, "Commencer", self.__close)

        self.__ready = False

    def getParams(self) :
        return self.__params

    def __close(self) :
        self.__ready = True

    def update(self) :
        self.__rulesRadiosGroup.update()
        self.__sizeRadiosGroup.update()
        self.__timeByTurnRadiosGroup.update()
        self.__validateButton.update()
        return self.__ready

    def draw(self) :
        pyxel.rect(125, 27, 266, 210, 13)
        pyxel.rectb(123, 25, 266, 210, 7)
        pyxel.rect(124, 26, 264, 208, 0)
        pyxel.bltm(178, 40, 0, 0, 0, 155, 18)
        text.draw(140, 70, "Règles :", 7)
        self.__rulesRadiosGroup.draw()
        text.draw(140, 110, "Taille de la grille :", 7)
        self.__sizeRadiosGroup.draw()
        text.draw(140, 150, "Temps par tour :", 7)
        self.__timeByTurnRadiosGroup.draw()
        self.__validateButton.draw()