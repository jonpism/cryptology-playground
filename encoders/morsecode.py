from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class MORSE_CODE:

    TABLE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
        'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
        'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', '?': '..--..', '!': '-.-.--',
        '.': '.-.-.-', ',': '--..--', ';': '-.-.-.', ':': '---...', '+': '.-.-.', '-': '-....-', '/': '-..-.',
        '=': '-...-'}

    def morse_to_text(self, input):
        input_list = input.split(' ')
        input_list = [mc for mc in input_list]

        text = ""
        for i in range(len(input_list)):
            for char, mc in self.TABLE.items():
                if input_list[i] == mc:
                    text += char + " "
        return text
    
    def text_to_morse(self, input):
        # input_list = input.split(' ')
        input_list = [txt for txt in input]

        morse = ""
        for i in range(len(input_list)):
            for char, mc in self.TABLE.items():
                if input_list[i].upper() == char:
                    morse += mc + " "
        return morse

class MorseCodeWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Morse Code"
        msgbox_txt = (
        "Morse code is a method of transmitting text information using "
        "a series of on-off signals, which can be in the form of sound, "
        "light, or visual signals. It encodes the characters of the alphabet, "
        "numerals, and punctuation marks as sequences of dots (.) and  "
        "dashes (−). Morse code was developed in the early 1830s and "
        "1840s by Samuel Morse and Alfred Vail, primarily for use in telegraphy.<br> "
        "Each letter or number is represented by a unique sequence of dots and dashes. "
        "A dot is a short signal, while a dash is a longer one, typically three times "
        "the duration of a dot. <br> "
        "e.g: S= ..., O= ---, so the word SOS becomes: ...---... <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Morse_code>Wikipedia</a><br>")

        self.setWindowTitle("Morse Code")
        self.setFixedSize(700, 700)

        # Text
        text_input_label = QLabel("Give text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        to_morse_button = DefaultButtonStyle("To Morse", parent=self, command=self.to_morse)
        to_morse_button.setGeometry(300, 120, 100, 50)

        self.to_morse_result_label = QTextEdit(parent=self)
        self.to_morse_result_label.setGeometry(10, 200, 680, 100)
        self.to_morse_result_label.setReadOnly(True)
        self.to_morse_result_label.hide()

        # Morse Code encoded
        morse_input_label = QLabel("Give Morse Code encoded text:", parent=self)
        morse_input_label.setGeometry(300, 300, 250, 50)
        self.morse_input = DefaultQLineEditStyle(parent=self, placeholder_text="Separate letters with space")
        self.morse_input.setGeometry(10, 360, 680, 50)

        to_text_button = DefaultButtonStyle("To Text", parent=self, command=self.to_text)
        to_text_button.setGeometry(300, 420, 100, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 520, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.object = MORSE_CODE()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_text(self):
        try:
            morse = self.morse_input.text()
            if not morse:
                raise ValueError("Please give Morse Code Encoded text")
            result = self.object.morse_to_text(morse)
            self.to_text_result_label.clear()
            self.to_text_result_label.setHtml(f"<b>Text:</b><br>{str(result)}")
            self.to_text_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def to_morse(self):
        try:
            txt = self.text_input.text()
            if not txt:
                raise ValueError("Please give text")
            result = self.object.text_to_morse(txt)
            self.to_morse_result_label.clear()
            self.to_morse_result_label.setHtml(f"<b>Morse:</b><br>{str(result)}")
            self.to_morse_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
