import pyxel
from src.text import text
from src.grid import Grid
from src.ship import Ship   

class Ships :

    SHIPS_COUNT_BY_DIFFICULTY = {
        8  : [0, 3, 2, 0, 0],
        10 : [0, 1, 2, 1, 1],
        12 : [4, 3, 2, 1, 0]
    }

    def __init__(self, size : int) :
        self.__ships = []
        shipsGroupsCount = 0
        for i in range(5) :
            if Ships.SHIPS_COUNT_BY_DIFFICULTY[size][i] > 0 :
                shipsGroupsCount += 1
                for j in range(Ships.SHIPS_COUNT_BY_DIFFICULTY[size][i]) :
                    self.__ships.append(Ship(i + 1, 330 + j * ((i + 1) * 17 + 10), shipsGroupsCount * 40 + 14))

    def update(self, grid : Grid) :
        isDragging = False
        draggingSize = 0
        draggingDirection = 0
        for i in range(len(self.__ships)) :
            if self.__ships[i].manageDragNDrop(grid.onShipDrop) :
                isDragging = True
                draggingSize = self.__ships[i].getSize()
                draggingDirection = self.__ships[i].getDirection()
        
        if isDragging :
            grid.hoverLine(draggingSize, draggingDirection)
        else :
            grid.resetHover()

    def draw(self) :
        currentShipsSize = 0
        currentShipsCount = 0
        shipsGroupCount = 0
        for i in range(len(self.__ships)) :
            if self.__ships[i].getSize() != currentShipsSize :
                currentShipsSize = self.__ships[i].getSize()
                shipsGroupCount += 1
                text.draw(330, shipsGroupCount * 40, Ship.SHIP_NAMES[currentShipsSize - 1])
                currentShipsCount = 0
            
            self.__ships[i].draw()

            currentShipsCount += 1
