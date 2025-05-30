import pyxel
from src.grid import Grid
from src.params import Params
from src.ships import Ships

class App:

    PARTS_1_GAME_PARAMS     = 1
    PARTS_2_SHIPS_PLACEMENT = 2
    PARTS_3_PLAYER_TURN     = 3
    PARTS_4_COMPUTER_TURN   = 4

    def __init__(self) :
        pyxel.init(512, 256, "Battle Ships")
        pyxel.load("assets/resources.pyxres")
        pyxel.mouse(True)
        self.playerGrid = None      # Grid(10, [128, 128], hoverDisplay = Grid.HOVER_BORDERED)
        self.computerGrid = None    # Grid(10, [384, 128])
        self.ships = None
        self.params = Params()
        self.currentPart = App.PARTS_1_GAME_PARAMS
        pyxel.run(self.update, self.draw)

    def update(self) :
        if self.currentPart == App.PARTS_1_GAME_PARAMS :
            if self.params.update() :
                self.playerGrid = Grid(self.params.getSize(), [192, 128])
                self.ships = Ships(self.params.getSize())
                self.currentPart = App.PARTS_2_SHIPS_PLACEMENT

        if self.currentPart == App.PARTS_2_SHIPS_PLACEMENT :
            if self.ships.update(self.playerGrid) :

                self.currentPart = App.PARTS_3_PLAYER_TURN

    def draw(self) :
        pyxel.cls(0)
        
        if self.currentPart == App.PARTS_1_GAME_PARAMS :
            self.params.draw()

        if self.currentPart == App.PARTS_2_SHIPS_PLACEMENT :
            self.playerGrid.draw()
            self.ships.draw()
        
        #self.computerGrid.draw()

App()