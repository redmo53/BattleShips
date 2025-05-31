class Params :
    
    RULES_NORMAL        = 0
    RULES_ENHANCED      = 1
    DIFFICULTY_EASY     = 8
    DIFFICULTY_MEDIUM   = 10
    DIFFICULTY_HARD     = 12
    TIME_SHORT          = 20
    TIME_MEDIUM         = 30
    TIME_LONG           = 45

    def __init__(self) :
        
        self.__rules = Params.RULES_NORMAL
        self.__size = Params.DIFFICULTY_MEDIUM
        self.__timeByTurn = Params.TIME_MEDIUM

    def setRules(self, rules : int) :
        self.__rules = rules

    def getRules(self) :
        return self.__rules

    def setSize(self, size : int) :
        self.__size = size

    def getSize(self) :
        return self.__size

    def setTimeByTurn(self, timeByTurn : int) :
        self.__timeByTurn = timeByTurn

    def getTimeByTurn(self) :
        return self.__timeByTurn
