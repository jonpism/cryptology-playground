from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 

class ROT13Window(QWidget):

    TABLE1 = {'A' : 1, 'B' : 2, 'C' : 3, 'D' : 4, 'E' : 5,
        'F' : 6, 'G' : 7, 'H' : 8, 'I' : 9, 'J' : 10,
        'K' : 11, 'L' : 12, 'M' : 13, 'N' : 14, 'O' : 15,
        'P' : 16, 'Q' : 17, 'R' : 18, 'S' : 19, 'T' : 20,
        'U' : 21, 'V' : 22, 'W' : 23, 'X' : 24, 'Y' : 25, 'Z' : 26}
    
    TABLE2 = {0 : 'Z', 1 : 'A', 2 : 'B', 3 : 'C', 4 : 'D', 5 : 'E',
        6 : 'F', 7 : 'G', 8 : 'H', 9 : 'I', 10 : 'J',
        11 : 'K', 12 : 'L', 13 : 'M', 14 : 'N', 15 : 'O',
        16 : 'P', 17 : 'Q', 18 : 'R', 19 : 'S', 20 : 'T',
        21 : 'U', 22 : 'V', 23 : 'W', 24 : 'X', 25 : 'Y'}

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About ROT13"
        msgbox_txt = (
        "ROT13 is a simple letter substitution cipher that replaces "
        "each letter in the alphabet with the letter 13 positions after it. "
        "If you go past 'Z'm you wrap around to the beginning of the alphabet. "
        "This means: A becomes N, B becomes O, C becomes P ... and so on until "   
        "N becomes A, and so forth. ROT13 is a symmetric cipher, meaning "
        "applying it twice brings you back to the original text. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/ROT13>Wikipedia</a><br>"
        "<a href=https://www.geeksforgeeks.org/rot13-cipher>Geeks for Geeks</a>")

        self.setWindowTitle("ROT13")
        self.setFixedSize(700, 400)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_rot13)
        encrypt_button.setGeometry(300, 160, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 230, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_rot13(self):
        try:
            if not self.plaintext_input.text():
                raise ValueError('Please enter plaintext.')
            input = self.plaintext_input.text()
            encrypted_input = self.rot13_encryption(input)

            self.encrypted_text_label.clear()
            self.encrypted_text_label.setHtml(f"<b>Ciphertext:</b><br>{str(encrypted_input)}")
            self.encrypted_text_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def rot13_encryption(self, message):
        cipher = ''
        shift = 13
        for letter in message:
            if(letter != ' '):
                num = (self.TABLE1[letter.upper()] + shift) % 26
                cipher += self.TABLE2[num]
            else:
                cipher += ' '
        return cipher
