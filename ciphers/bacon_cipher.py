from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 

TABLE = {
    "A": "aaaaa", "B": "aaaab", "C": "aaaba", "D": "aaabb", "E": "aabaa", "F": "aabab", "G": "aabba", 
    "H": "aabbb", "I": "abaaa", "J": "abaab", "K": "ababa", "L": "ababb", "M": "abbaa", "N": "abbab",
    "O": "abbba", "P": "abbbb", "Q": "baaaa", "R": "baaab", "S": "baaba", "T": "baabb", "U": "babaa",
    "V": "babab", "W": "babba", "X": "babbb", "Y": "bbaaa", "Z": "bbaab"}

# Implementation
class Bacon_CipherImp:

    def __init__(self, text) -> None:
        self.text = text

    def bacon_cipher_encode(self, text) -> str:
        result = ""

        for i in text:
            for char, bacon in TABLE.items():
                if i != " " and char == i.upper():
                    result += bacon + " "

        return result
    
    def bacon_cipher_decode(self, text) -> str:
        result = ""
        index = 0
    
        while index < len(text):
            if text[index] == " ":
                index += 1
                continue
        
            chunk = text[index: index + 5]
        
            for char, bacon in TABLE.items():
                if chunk == bacon:
                    result += char + " "
                    break
        
            index += 5
    
        return result


class BaconCipherWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Bacon cipher"
        msgbox_txt = (
        "The Bacon cipher, also known as Bacon's cipher, is a steganographic "
        "method developed by Sir Francis Bacon in the early 17th century. "
        "It encodes messages through binary coding, where text is concealed by "
        "using two distinct typefaces or styles of text (for example, bold and regular). "
        "This cipher falls under the category of steganography because the encoded "
        "message is hidden within the text’s format rather than in the content itself. "
        "Each letter in the English alphabet is represented by a sequence of five "
        "binary characters (A or B). Bacon originally mapped out 24 letters "
        "(I and J, as well as U and V, were each treated as a single letter). <br>"
        "For example: A=AAAAA, B=AAAAB, C=AAABA, D=AAABB etc"
        "<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Bacon's_cipher>Wikipedia</a><br>"
        "<a href=http://www.practicalcryptography.com/ciphers/baconian-cipher>Practical Cryptography</a>")

        self.setWindowTitle("Bacon Cipher")
        self.setFixedSize(700, 700)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_encryption)
        encrypt_button.setGeometry(300, 120, 100, 50)

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 180, 680, 100)
        self.ciphertext_label.setReadOnly(True)
        self.ciphertext_label.hide()

        bacon_label = QLabel("Give text encrypted with bacon cipher:", parent=self)
        bacon_label.setGeometry(250, 300, 300, 50)
        self.bacon_input = DefaultQLineEditStyle(parent=self)
        self.bacon_input.setGeometry(10, 350, 680, 50)

        encrypt_button = DefaultButtonStyle("Decrypt", parent=self, command=self.call_decryption)
        encrypt_button.setGeometry(300, 410, 100, 50)

        self.decrypted_text_label = QTextEdit(parent=self)
        self.decrypted_text_label.setGeometry(10, 470, 680, 100)
        self.decrypted_text_label.setReadOnly(True)
        self.decrypted_text_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def call_encryption(self):
        try:
            if self.plaintext_input.text():
                input = self.plaintext_input.text()

                obj = Bacon_CipherImp(text=input)
                ciphertext = obj.bacon_cipher_encode(input)

                self.ciphertext_label.setHtml(f"<b>Ciphertext:</b><br>{ciphertext}")
                self.ciphertext_label.show()
            else:
                raise ValueError('Please enter a plaintext.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def call_decryption(self):
        try:
            if self.bacon_input.text():
                input = self.bacon_input.text()

                obj = Bacon_CipherImp(text=input)
                decrypted_input = obj.bacon_cipher_decode(input)

                self.decrypted_text_label.setHtml(f"<b>Decrypted text:</b><br>{decrypted_input}")
                self.decrypted_text_label.show()
            else:
                raise ValueError('Please enter bacon ciphertext input.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
