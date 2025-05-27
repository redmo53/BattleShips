import pyxel

class Grid :

    DIRECTION_NORTH = 0
    DIRECTION_EAST = 1
    DIRECTION_SOUTH = 2
    DIRECTION_WEST = 3
    HOVER_FILLED = 0
    HOVER_BORDERED = 1

    def __init__(self, size : int, legend : bool = True, hoverDisplay : int = HOVER_FILLED) :
        self.__size = size
        self.__data = [[None for j in range(self.__size)] for i in range(self.__size)]
        self.__w = 17 * self.__size + 1
        self.__h = 17 * self.__size + 1
        self.__x = 128 - int(self.__size / 2 * 17)
        self.__y = 128 - int(self.__size / 2 * 17)
        self.__legend = legend
        self.__hoverDisplay = hoverDisplay
        self.__hoveredDirection = Grid.DIRECTION_SOUTH
        self.__resetHover()
        self.__resetSelect()
        
    def display(self) :
        '''
        Affiche la grille
        '''
        # Grille
        for i in range(self.__size + 1) :
            pyxel.line(self.__x + i * 17, self.__y, self.__x + i * 17, self.__y + self.__h - 1, 13)
        for i in range(self.__size + 1) :
            pyxel.line(self.__x, self.__y + i * 17, self.__x + self.__w - 1, self.__y + i * 17, 13)
        
        # Légende
        if (self.__legend) :
            for i in range(self.__size) :
                pyxel.text(self.__x + 8 + i * 17, self.__y - 12, chr(ord('A') + i), 13)
            for i in range(self.__size) :
                pyxel.text(self.__x - (9 if i < 9 else 13), self.__y + 7 + i * 17, str(i + 1), 13)
        
        # Survol
        if self.__isHovered :
            for cell in self.__hovered :
                if self.__hoverDisplay == Grid.HOVER_FILLED :
                    pyxel.rect(self.__x + cell[0] * 17 + 1, self.__y + cell[1] * 17 + 1, 16, 16, 5)
                else :
                    pyxel.rectb(self.__x + cell[0] * 17, self.__y + cell[1] * 17, 18, 18, 8)
        
        # Sélection
        if self.__isSelected :
            for cell in self.__selected :
                pyxel.rect(self.__x + cell[0] * 17 + 1, self.__y + cell[1] * 17 + 1, 16, 16, 6)

        # Contenu
        for i in range(self.__size) :
            for j in range(self.__size) :
                if self.__data[i][j] != None :
                    (x, y) = self.__getCellCoordinates(i, j)
                    pyxel.text(x, y, str(self.__data[i][j]), 8)

    def setCellData(self, x : int, y : int, value) :
        if 1 <= x <= self.__size and 1 <= y <= self.__size :
            self.__data[x - 1][y - 1] = value

    def __getCellCoordinates(self, i : int, j : int) :
        '''
        Renvoie les coordonnées en pixel d'une case
        ''' 
        return (self.__x + i * 17 + 1, self.__y + j * 17 + 1)
    
    def hover(self) :
        '''
        Gère si une case est survolée par la souris
        '''
        self.__resetHover()
        if self.__x < pyxel.mouse_x < self.__x + self.__w and self.__y < pyxel.mouse_y < self.__y + self.__h :
            self.__hovered.append(((pyxel.mouse_x - self.__x - 1) // 17, (pyxel.mouse_y - self.__y - 1) // 17))
            self.__isHovered = True
    
    def hoverLine(self, length : int = 0) :
        '''
        Affiche une ligne au survol de la souris
        '''
        self.__resetHover()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) :
            self.__hoveredDirection = (self.__hoveredDirection + 1) % 4

        if self.__x < pyxel.mouse_x < self.__x + self.__w and self.__y < pyxel.mouse_y < self.__y + self.__h :
            
            x = (pyxel.mouse_x - self.__x - 1) // 17
            y = (pyxel.mouse_y - self.__y - 1) // 17

            if length == 0 :
                if self.__hoveredDirection == Grid.DIRECTION_NORTH or self.__hoveredDirection == Grid.DIRECTION_SOUTH :
                    for i in range(self.__size) :
                        self.__hovered.append((x, i))
                else :
                    for i in range(self.__size) :
                        self.__hovered.append((i, y))

            else :
                if self.__hoveredDirection == Grid.DIRECTION_NORTH :
                    minY = y - length + 1 if y - length + 1 > 0 else 0
                    for i in range(minY, y + 1) :
                        self.__hovered.append((x, i))
                elif self.__hoveredDirection == Grid.DIRECTION_SOUTH :
                    maxY = y + length if y + length < self.__size else self.__size
                    for i in range(y, maxY) :
                        self.__hovered.append((x, i))
                elif self.__hoveredDirection == Grid.DIRECTION_WEST :
                    minX = x - length + 1 if x - length + 1 > 0 else 0
                    for i in range(minX, x + 1) :
                        self.__hovered.append((i, y))
                elif self.__hoveredDirection == Grid.DIRECTION_EAST :
                    maxX = x + length if x + length < self.__size else self.__size
                    for i in range(x, maxX) :
                        self.__hovered.append((i, y))

            self.__hovered = list(set(self.__hovered))
            self.__isHovered = True

    def hoverCross(self, length : int = 0) :
        '''
        Affiche une croix au survol de la souris
        '''
        self.__resetHover()

        if self.__x < pyxel.mouse_x < self.__x + self.__w and self.__y < pyxel.mouse_y < self.__y + self.__h :
            
            x = (pyxel.mouse_x - self.__x - 1) // 17
            y = (pyxel.mouse_y - self.__y - 1) // 17

            if length == 0 :
                for i in range(self.__size) :
                    self.__hovered.append((x, i))
                for i in range(self.__size) :
                    self.__hovered.append((i, y))
            else :
                minX = x - length + 1 if x - length + 1 > 0 else 0
                maxX = x + length if x + length < self.__size else self.__size
                for i in range(minX, maxX) :
                    self.__hovered.append((i, y))

                minY = y - length + 1 if y - length + 1 > 0 else 0
                maxY = y + length if y + length < self.__size else self.__size
                for i in range(minY, maxY) :
                    self.__hovered.append((x, i))

            self.__hovered = list(set(self.__hovered))
            self.__isHovered = True

    def hoverSquare(self, length : int) :
        '''
        Affiche un carré au survol de la souris (taille minimum : 2)
        '''
        self.__resetHover()

        if self.__x < pyxel.mouse_x < self.__x + self.__w and self.__y < pyxel.mouse_y < self.__y + self.__h :
            
            x = (pyxel.mouse_x - self.__x - 1) // 17
            y = (pyxel.mouse_y - self.__y - 1) // 17

            if length > 1 :
                for i in range(length) :
                    curY = y - (length - i) + 1 if y - (length - i) + 1 > 0 else 0
                    minX = x - i if x - i > 0 else 0
                    maxX = x + i + 1 if x + i + 1 < self.__size else self.__size
                    for j in range(minX, maxX) :
                        self.__hovered.append((j, curY))
                for i in range(1, length) :
                    curY = y + i if y + i < self.__size - 1 else self.__size - 1
                    minX = x - (length - i - 1) if x - (length - i - 1) > 0 else 0
                    maxX = x + (length - i - 1) + 1 if x + (length - i - 1) + 1 < self.__size else self.__size
                    for j in range(minX, maxX) :
                        self.__hovered.append((j, curY))

            self.__hovered = list(set(self.__hovered))
            self.__isHovered = True

    def __resetHover(self) :
        '''
        Annule le survol
        '''
        self.__hovered = []
        self.__isHovered = False

    def select(self, multiSelect : bool = False) :
        '''
        Gère la sélection des cases survolées
        '''
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) :
            if self.__isHovered :
                if multiSelect == False :
                    self.__resetSelect()
                for cell in self.__hovered :
                    self.__toggleSelected(cell[0], cell[1])
            else :
                self.__resetSelect()

    def selectCrossOnly(self, x : int, y : int) :
        if len(self.__selected) == 0 :
            return True
        else :
            if (self.__selected[0][0] == x or self.__selected[0][1] == y) :
                return True
            else :
                return False    

    def __toggleSelected(self, x : int, y : int) :
        '''
        Ajoute ou enlève de la liste des sélections
        '''
        cell = [x, y]
        selected = False
        if (cell in self.__selected) :
            self.__selected.remove(cell)
        else :
            self.__selected.append(cell)
            selected = True
        
        self.__isSelected = len(self.__selected) > 0

        return selected
             

    def __resetSelect(self) :
        '''
        Annule la selection
        '''
        self.__selected = []
        self.__isSelected = False