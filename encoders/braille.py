from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class Braille:

    TABLE = {
        '100000': 'a', '110000': 'b', '100100': 'c', '100110': 'd', '100010': 'e',
        '110100': 'f', '110110': 'g', '110010': 'h', '010100': 'i', '010110': 'j',
        '101000': 'k', '111000': 'l', '101100': 'm', '101110': 'n', '101010': 'o',
        '111100': 'p', '111110': 'q', '111010': 'r', '011100': 's', '011110': 't',
        '101001': 'u', '111001': 'v', '010111': 'w', '101101': 'x', '101111': 'y',
        '101011': 'z', '000000': ' ', '000001': ',', '000101': '.', '100111': '?',
        '011101': '!', '001111': '#', '100101': '%', '111101': '&', '111011': '(',
        '011111': ')', '100001': '*', '001101': '+', '001001': '-', '001100': '/',
        '001011': '0', '010000': '1', '011000': '2', '010010': '3', '010011': '4',
        '010001': '5', '011010': '6', '011011': '7', '011001': '8', '001010': '9',
        '100011': ':', '000011': ';', '110001': '<', '111111': '=', '001110': '>',
        '000100': '@', '010101': '[', '110111': ']', '000110': '^', '000111': '_'}

    def text_to_braille(self, input):
        result = []

        for char in input:
            for bin, chr in self.TABLE.items():
                if char.lower() == chr:
                    result.append(bin)
    
        return result
    
    def braille_to_unicode(self, binary):
        """Convert a 6-bit binary string to a Unicode Braille character."""
        # Each dot in a Braille character corresponds to a specific bit position.
        # Unicode Braille starts from U+2800 (⠁), and dots map to bits in this range.
        braille_offset = 0x2800
        # Convert the 6-bit binary string to an integer and add to the base Braille offset
        braille_char = chr(braille_offset + int(binary, 2))
        return braille_char

    pass

class BrailleWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Braille"
        msgbox_txt = (
        "Braille is a tactile writing system used by individuals who are "
        "visually impaired or blind. It was invented by Louis Braille, "
        "a French educator who lost his sight due to a childhood accident. "
        "He developed this system in the early 19th century to make reading "
        "and writing more accessible for people who cannot use traditional print. "
        "The fundamental component of Braille is the 'Braille cell', which "
        "is made up of six raised dots arranged in two parallel columns of "
        "three dots each. These dots are numbered from 1 to 6, with dot 1 "
        "at the top left and dot 6 at the bottom right. Different combinations "
        "of these dots represent different letters, numbers, punctuation marks, "
        "and even entire words or phrases. There are 64 possible combinations "
        "of the six dots, including a configuration with no dots raised. These "
        "combinations are used to encode letters, numbers, and other symbols. "
        "For example, the letter 'A' is represented by a single raised dot "
        "in position 1, while 'B' has raised dots in positions 1 and 2. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Braille>Wikipedia</a><br>"
        "<a href=https://www.britannica.com/topic/Braille-writing-system>Britannica</a>")

        self.setWindowTitle("Braille Tactile Writing System")
        self.setFixedSize(700, 400)

        # Text
        text_input_label = QLabel("Give text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        to_braille_button = DefaultButtonStyle("To Braille", parent=self, command=self.to_braille)
        to_braille_button.setGeometry(300, 120, 100, 50)

        self.to_braille_result_label = QTextEdit(parent=self)
        self.to_braille_result_label.setGeometry(10, 200, 680, 100)
        self.to_braille_result_label.setReadOnly(True)
        self.to_braille_result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_braille(self):
        try:
            if self.text_input.text():
                message = self.text_input.text()
                object = Braille()
                binary = object.text_to_braille(message)
                unicode = ''.join(object.braille_to_unicode(binary) for binary in binary)

                self.to_braille_result_label.clear()
                self.to_braille_result_label.setHtml(f"<b>Braille:</b><br>{str(unicode)}")
                self.to_braille_result_label.show()
            else:
                raise ValueError('Please enter a message/text.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
