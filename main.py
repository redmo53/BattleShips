import pyxel
from grid import Grid
from params import Params

class App:
    def __init__(self) :
        pyxel.init(512, 256, "Battle Ships")
        pyxel.load("resources.pyxres")
        pyxel.mouse(True)
        self.playerGrid = None      # Grid(10, [128, 128], hoverDisplay = Grid.HOVER_BORDERED)
        self.computerGrid = None    # Grid(10, [384, 128])
        self.params = Params()
        pyxel.run(self.update, self.draw)

    def update(self) :
        if not self.params.isReady() :
            if self.params.update() :
                self.playerGrid = Grid(self.params.getSize(), [128, 128], hoverDisplay = Grid.HOVER_BORDERED)
                self.computerGrid = Grid(self.params.getSize(), [384, 128])

        if self.playerGrid != None :
            self.playerGrid.hover()
            self.playerGrid.select()

    def draw(self) :
        pyxel.cls(0)
        if not self.params.isReady() :
            self.params.draw()

        if self.playerGrid != None :
            self.playerGrid.draw()
        
        #self.computerGrid.draw()

App()