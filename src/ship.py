import pyxel

class Ship :

    SHIP_NAMES = ["Sous-marin", "Torpilleur", "Croiseur", "Cuirassé", "Porte-avions"]
    DIRECTION_NORTH = 0
    DIRECTION_EAST  = 1
    DIRECTION_SOUTH = 2
    DIRECTION_WEST  = 3

    def __init__(self, size : int, number : int, x : int, y : int) :
        self.__size = size
        self.__number = number
        self.__cells = [ 1 for i in range(self.__size) ]
        self.__placed = False
        self.__dragged = False
        self.__menuX = x
        self.__menuY = y
        self.__x = x
        self.__y = y
        self.__w = self.__size * 17 + 1
        self.__h = 18
        self.__direction = Ship.DIRECTION_EAST

    def getNumber(self) :
        return self.__number

    def getSize(self) :
        return self.__size
    
    def getDirection(self) :
        return self.__direction
    
    def move(self, x : int, y : int) :
        self.__x = x
        self.__y = y

    def manageDragNDrop(self, onDrag : callable, onDrop : callable) :
        dropped = False

        # Bouton pressé
        if self.__x < pyxel.mouse_x < self.__x + self.__w and self.__y < pyxel.mouse_y < self.__y + self.__h and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) :
            self.__placed = False
            self.__dragged = True
            onDrag(self)

        # Bouton relâché
        elif self.__dragged and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            self.__dragged = False
            dropped = True
            self.__placed = onDrop(self)

        # Changement de direction
        if self.__dragged and pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) :
            self.__direction = (self.__direction + 1) % 4
            self.__w, self.__h = self.__h, self.__w

        # Mise à jour des coordonnées si glissement en cours
        if self.__dragged == True :
            if self.__direction == Ship.DIRECTION_EAST :
                self.__x = pyxel.mouse_x - 9
                self.__y = pyxel.mouse_y - 9
            elif self.__direction == Ship.DIRECTION_WEST :
                self.__x = pyxel.mouse_x - self.__w + 9
                self.__y = pyxel.mouse_y - 9
            elif self.__direction == Ship.DIRECTION_SOUTH :
                self.__x = pyxel.mouse_x - 9
                self.__y = pyxel.mouse_y - 9
            elif self.__direction == Ship.DIRECTION_NORTH :
                self.__x = pyxel.mouse_x - 9
                self.__y = pyxel.mouse_y - self.__h + 9

        # Mise à jour des coordonnées si dépôt
        if dropped :
            if not self.__placed :
                # Si hors-grille
                self.__x = self.__menuX
                self.__y = self.__menuY
                if self.__direction == Ship.DIRECTION_NORTH or self.__direction == Ship.DIRECTION_SOUTH :
                    self.__w, self.__h = self.__h, self.__w
                self.__direction = Ship.DIRECTION_EAST
        
        return self.__dragged

    def isDragged(self) :
        return self.__dragged
    
    def isPlaced(self) :
        return self.__placed
    
    def draw(self) :
        if self.__placed :
            pyxel.rect(self.__x, self.__y, self.__w, self.__h, 14)
        
        pyxel.rectb(self.__x, self.__y, self.__w, self.__h, 7)

        if not self.__dragged :
            if self.__direction == Ship.DIRECTION_NORTH or self.__direction == Ship.DIRECTION_SOUTH :
                for i in range(1, self.__size) :
                    pyxel.line(self.__x, self.__y + i * 17, self.__x + 17, self.__y + i * 17, 7)
            else :
                for i in range(1, self.__size) :
                    pyxel.line(self.__x + i * 17, self.__y, self.__x + i * 17, self.__y + 17, 7)
