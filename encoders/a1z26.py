from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class A1Z26_encode:
    TABLE = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 
        'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 
        'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
        'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 
        'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26}

    # letter to number
    def encode(self, input):
        input_list = list(input)
        encoded = []
        for char in input_list:
            if char in self.TABLE:
                encoded.append(str(self.TABLE[char]))
            else:
                encoded.append(char)
        return ' '.join(encoded)

class A1Z26EncodeWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About A1Z26 Encode"
        msgbox_txt = (
        "Converts characters to their corresponding order number: "
        "A=1, B=2, C=3, ..., Z=26 <br> "
        "e.g: Hello Anne, becomes: 8, 5, 12, 12, 15, 1, 14, 14, 5")

        self.setWindowTitle("A1Z26 Encode")
        self.setFixedSize(700, 400)

        # Text
        message_input_label = QLabel("Give message:", parent=self)
        message_input_label.setGeometry(300, 10, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.command)
        submit_button.setGeometry(300, 160, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 220, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        
    def command(self):
        message = self.message_input.text()

        obj = A1Z26_encode()
        encoded = obj.encode(message)

        self.result_label.clear()
        self.result_label.setHtml(f"<b>Encoded text:</b><br>{str(encoded)}")
        self.result_label.show()

# ========================================================================================================================

class A1Z26_decode:
    TABLE = A1Z26_encode.TABLE

    # number to letter
    def decode(self, input):
        input_list = input.split(' ')
        input_list = [int(num) for num in input_list]

        decoded = ""
        for i in range(len(input_list)):
            for letter, number in self.TABLE.items():
                if input_list[i] == number:
                    decoded += letter
        return decoded

class A1Z26DecodeWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About A1Z26 Decode"
        msgbox_txt = (
        "Converts characters to their corresponding order number: "
        "A=1, B=2, C=3, ..., Z=26 <br> "
        "e.g: Hello Anne, becomes: 8, 5, 12, 12, 15, 1, 14, 14, 5")

        self.setWindowTitle("A1Z26 Decode")
        self.setFixedSize(700, 400)

        # Text
        numbers_input_label = QLabel("Give numbers separated with space (1-26):", parent=self)
        numbers_input_label.setGeometry(250, 10, 300, 50)
        self.numbers_input = DefaultQLineEditStyle(parent=self)
        self.numbers_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.command)
        submit_button.setGeometry(300, 160, 100, 50)

        self.decoded_label = QTextEdit(parent=self)
        self.decoded_label.setGeometry(10, 220, 680, 100)
        self.decoded_label.setReadOnly(True)
        self.decoded_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def command(self):
        numbers = self.numbers_input.text()

        obj = A1Z26_decode()
        decoded = obj.decode(numbers)

        self.decoded_label.clear()
        self.decoded_label.setHtml(f"<b>Decoded text:</b><br>{str(decoded)}")
        self.decoded_label.show()
