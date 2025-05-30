import pyxel
from src.text import text

class Button :

    def __init__(self, x : int, y : int, label : str, onClick : callable, enabled : bool = True) :
        self.__label = label
        self.__x = x
        self.__y = y
        labelLength = text.getLength(label)
        self.__w = labelLength + 22
        self.__h = 21
        self.__onClick = onClick
        self.__clicked = False
        self.__enabled = enabled

    def setEnabled(self, enabled : bool) :
        self.__enabled = enabled
        
    def isEnabled(self) :
        return self.__enabled

    def update(self) :
        if self.__enabled :
            # Bouton pressé
            if self.__x < pyxel.mouse_x < self.__x + self.__w and self.__y < pyxel.mouse_y < self.__y + self.__h and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) :
                self.__clicked = True
            # Bouton relâché
            elif self.__x < pyxel.mouse_x < self.__x + self.__w and self.__y < pyxel.mouse_y < self.__y + self.__h and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
                self.__clicked = False
                self.__onClick()
            else :
                self.__clicked = False

    def draw(self) :
        # Couleur
        color = 7 if self.__enabled else 13
        
        # Ombre
        pyxel.rect(self.__x + 2, self.__y + 2, self.__w, self.__h, 13 if self.__clicked else color)

        # Bouton
        if self.__clicked :
            pyxel.rect(self.__x + 2, self.__y + 2, self.__w - 2, self.__h - 2, 0)
            pyxel.rectb(self.__x + 1, self.__y + 1, self.__w, self.__h, color)
            text.draw(self.__x + 13, self.__y + 7, self.__label, color)
        else :
            pyxel.rect(self.__x + 1, self.__y + 1, self.__w - 2, self.__h - 2, 0)
            pyxel.rectb(self.__x, self.__y, self.__w, self.__h, color)
            text.draw(self.__x + 12, self.__y + 6, self.__label, color)
        
        

class Radio :

    def __init__(self, x : int, y : int, label : str, value, checked : bool = False) :
        self.__label = label
        self.__value = value
        self.__x1 = x
        self.__y1 = y
        labelLength = text.getLength(label)
        self.__x2 = x + labelLength + 13
        self.__y2 = y + 8
        self.__checked = checked

    def isChecked(self) :
        return self.__checked
    
    def check(self) :
        self.__checked = True
    
    def uncheck(self) :
        self.__checked = False

    def getValue(self) :
        return self.__value
    
    def update(self) :
        if self.__x1 < pyxel.mouse_x < self.__x2 and self.__y1 < pyxel.mouse_y < self.__y2 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) :
            self.__checked = True
            return True
        return False

    def draw(self) :
        if self.__checked :
            pyxel.circ(self.__x1 + 4, self.__y1 + 4, 4, 7)
        else :
            pyxel.circb(self.__x1 + 4, self.__y1 + 4, 4, 7)
        text.draw(self.__x1 + 13, self.__y1, self.__label, 7)

class RadiosGroup :

    def __init__(self, radios : list, onChange : callable) :
        self.__radios = radios
        self.__radiosCount = len(radios)
        self.__selected = None
        for i in range(self.__radiosCount) :
            if self.__radios[i].isChecked() :
                self.__selected = i
        if self.__selected == None :
            self.__selected = 0
            self.__radios[0].check()
        self.__onChange = onChange

    def uncheckAllExcept(self, thisOne : int) :
        for i in range(self.__radiosCount) :
            if (i != thisOne) :
                self.__radios[i].uncheck()

    def update(self) :
        for i in range(self.__radiosCount) :
            if self.__radios[i].update() :
                self.uncheckAllExcept(i)
                self.__onChange(self.__radios[i].getValue())
                break

    def draw(self) :
        for radio in self.__radios :
            radio.draw()