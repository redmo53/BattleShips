import pyxel
from src.text import text
from src.grid import Grid
from src.ship import Ship   
from src.forms import Button  

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
                    self.__ships.append(Ship(i + 1, len(self.__ships) + 1, 330 + j * ((i + 1) * 17 + 10), shipsGroupsCount * 40 + 14))
        
        self.__validateButton = Button(392 - text.getLength("Lancer la partie") // 2 - 12, 210, "Lancer la partie", self.__close, False)
        self.__ready = False
        self.__dragging = False

    def update(self, grid : Grid) :
        self.__dragging = False
        draggingSize = 0
        draggingDirection = 0
        for i in range(len(self.__ships)) :
            if self.__ships[i].manageDragNDrop(grid.onShipDrag, grid.onShipDrop) :
                self.__dragging = True
                draggingSize = self.__ships[i].getSize()
                draggingDirection = self.__ships[i].getDirection()
        
        if self.__dragging :
            grid.hoverLine(draggingSize, draggingDirection)
        else :
            grid.resetHover()

        if self.__areAllShipsPlaced() :
            self.__validateButton.setEnabled(True)
        self.__validateButton.update()

        return self.__ready

    def __areAllShipsPlaced(self) :
        for ship in self.__ships :
            if not ship.isPlaced() :
                return False
        return True

    def __areAllShipsPlacedInGroup(self, size : int) :
        for ship in self.__ships :
            if ship.getSize() == size and not ship.isPlaced() :
                return False
        return True
    
    def __close(self) :
        self.__ready = True

    def draw(self) :
        pyxel.rect(316, 11, 153, 236, 7)
        pyxel.rect(316, 11, 151, 234, 0)
        pyxel.rectb(315, 10, 153, 236, 7)

        text.draw(330, 20, "Placez vos navires :")

        currentShipsSize = 0
        currentShipsCount = 0
        shipsGroupsCount = 0
        for i in range(len(self.__ships)) :
            if self.__ships[i].getSize() != currentShipsSize :
                currentShipsSize = self.__ships[i].getSize()
                shipsGroupsCount += 1
                if self.__areAllShipsPlacedInGroup(currentShipsSize) :
                    text.draw(330, shipsGroupsCount * 40, Ship.SHIP_NAMES[currentShipsSize - 1], 13)
                else :
                    text.draw(330, shipsGroupsCount * 40, Ship.SHIP_NAMES[currentShipsSize - 1])
                currentShipsCount = 0
            
            self.__ships[i].draw()

            currentShipsCount += 1

        self.__validateButton.draw()

        if self.__dragging :
            text.draw(192 - text.getLength("(Clic-droit pour pivoter le navire)") // 2, 240, "(Clic-droit pour pivoter le navire)")


    # TODO Rendre les texte traductible