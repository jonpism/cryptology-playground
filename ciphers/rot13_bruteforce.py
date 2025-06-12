from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 

class ROT13BFWindow(QWidget):

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

        self.setWindowTitle("ROT13 Brute Force")
        self.setFixedSize(700, 400)

        # Ciphertext
        ciphertext_label = QLabel("Give ciphertext:", parent=self)
        ciphertext_label.setGeometry(300, 10, 120, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(10, 60, 680, 50)

        bf_button = DefaultButtonStyle("Submit", parent=self, command=self.call_bf)
        bf_button.setGeometry(300, 160, 100, 50)

        self.decrypted_text_label = QTextEdit(parent=self)
        self.decrypted_text_label.setGeometry(10, 220, 680, 100)
        self.decrypted_text_label.setReadOnly(True)
        self.decrypted_text_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_bf(self):
        try:
            if not self.ciphertext_input.text():
                raise ValueError('Please enter ciphertext.')
            ciphertext = self.ciphertext_input.text()
            decrypted_input = self.brute_force_rot13(ciphertext)

            self.decrypted_text_label.clear()
            self.decrypted_text_label.setHtml(f"<b>ROT13 Brute Force:</b><br>{str(decrypted_input)}")
            self.decrypted_text_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def caesar_cipher(self, text, shift):
        result = ""

        for char in text:
            if char.isupper():
                result += chr((ord(char) - 65 + shift) % 26 + 65)
            elif char.islower():
                result += chr((ord(char) - 97 + shift) % 26 + 97)
            else:
                result += char

        return result

    def brute_force_rot13(self, text):
        for shift in range(1, 14):
            decrypted_text = self.caesar_cipher(text, shift)
        return decrypted_text
