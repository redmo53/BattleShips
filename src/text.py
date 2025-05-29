from PIL import Image, ImageFont, ImageDraw
import pyxel

class Text(object):
    '''
    a unicode pixel font builder for pyxel
    '''

    def __init__(self, font_path: str, original_size: int, multipler: int = 8, mode: str = '1'):
        """initialize the class
        takes 4 parameter to initialize
        Args:
            font_path:  
                path to TrueTypeFont file (*.ttf)
            original_size:  
                Since we are using a pixel font, there must be a most suitable original size(e.g. 12px, 16px)
            multipler: (default=8)
                Sampling multipler, bigger number means better quality (and slower speed).
                For some other using you can use 1 for a blurry output (not recommanded)
            mode: (default='1')
                '1' means bilevel
                'L' means grayscale (not recommanded)
        """
        self.font_path = font_path
        self.original_size = original_size
        if multipler < 1:
            print('multipler can not be less than 1, using default(10) setting')
            multipler = 10
        self.multipler = multipler
        if mode not in ('1', 'L'):
            print(
                'mode support "1"(bilevel) and "L"(grayscale) only, using defualt("1") setting')
            mode = '1'
        self.mode = mode
        self.font_height = len(self.__extract_pixel('|'))
        self.__char_info = {}

    def __get_text_dimensions(self, text_string, font):
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = font.getmetrics()

        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent

        return (text_width, text_height)

    def __extract_pixel(self, char: str) -> list:
        """Extract pixel information of the unicode charactor
        Args:
            char: 
                charactor you want to extract, length shoud be 1
        Returns:
            2 dim list of grayscale value
        """
        # get fontsize
        font = ImageFont.truetype(
            self.font_path, self.original_size * self.multipler)
        # dummy image for get text_size
        tmp = Image.new('RGB', (1, 1), (0, 0, 0))
        tmp_d = ImageDraw.Draw(tmp)
        new_box = tmp_d.textbbox((0, 0), char, font)
        width = new_box[2]
        height = new_box[3]

        # background: transparent
        img = Image.new('RGB', (width, height), (0, 0, 0))
        img_d = ImageDraw.Draw(img)
        img_d.text((0, 0), char, font=font)
        # convert it to bilevel or grayscale image
        img = img.convert(self.mode)
        data = list(img.getdata())
        output_width = width // self.multipler
        output_height = height // self.multipler
        result = [[0]*(output_width) for _ in range(output_height)]
        p_offset = self.multipler >> 1  # color picker offset
        for i in range(output_height):
            for j in range(output_width):
                y = i * self.multipler
                x = j * self.multipler
                # calculate one dimension index in image data
                one_dim_idx = (y + p_offset) * width + x + p_offset
                result[i][j] = data[one_dim_idx]
        return result
    
    def __getCharInfo(self, s: str) :
        char = s[0]
        if char not in self.__char_info:
            # update the character table
            self.__char_info[char] = self.__extract_pixel(char)
            # update the font_height
            self.font_height = max(
                len(self.__char_info[char]), self.font_height)
        return self.__char_info[char]

    def getLength(self, s: str) :
        length = 0
        for char in s:
            c = self.__getCharInfo(char)
            length += len(c[0])
        return length
        

    def draw(self, x: int, y: int, s, color: int = 7):
        """unicode text painter (just like pyxel.text())
        Args:
            x, y:
                x,y-coordinate
            s:
                string or a list of unicode-(combining-)character
                "ABCDEFG" or ['ā', 'ć', 'ģ']
            color: (default=7)
                Foreground color of the string
        """
        cur_x, cur_y = x, y - 5  # current coordination
        origin_x = x
        for char in s:
            if char == '\n':
                cur_y += self.font_height - 4
                cur_x = origin_x
                continue
            c = self.__getCharInfo(char)
            for row in range(len(c)):
                for col in range(len(c[0])):
                    if c[row][col]:
                        pyxel.pset(cur_x + col, cur_y + row, color)
            cur_x += len(c[0])

text = Text("assets/Pixel-UniCode.ttf", 16, 2)