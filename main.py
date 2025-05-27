import pyxel
from grid import Grid

class App:
    def __init__(self) :
        pyxel.init(512, 256, "Battle Ships 2025")
        pyxel.mouse(True)
        self.grid = Grid(10, hoverDisplay = Grid.HOVER_BORDERED)
        self.grid.setCellData(1, 1, 1)
        self.grid.setCellData(5, 3, 1)
        self.grid.setCellData(2, 8, 1)
        pyxel.run(self.update, self.draw)

    def update(self) :
        self.grid.hover()          # Une case
        #self.grid.hoverLine()      # Ligne complète
        #self.grid.hoverLine(3)     # Ligne limitée
        #self.grid.hoverCross()     # Une croix complète
        #self.grid.hoverCross(2)    # Une croix limitée
        #self.grid.hoverSquare(3)    # Un losange
        self.grid.select()

    def draw(self) :
        pyxel.cls(0)
        self.grid.display()

App()