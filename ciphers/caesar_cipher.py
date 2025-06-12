from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 

# Implementation
class Caesar_CipherImp:

    def __init__(self, text, shift) -> None:
        self.text = text
        self.shift = shift

    def caesar_cipher_enc_dec(self, text, shift):
        return ''.join(
            chr((ord(char) - 65 + shift) % 26 + 65) if char.isupper() else 
            chr((ord(char) - 97 + shift) % 26 + 97) if char.islower() else char
            for char in text)
    

class CaesarCipherWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Caesar Cipher"
        msgbox_txt = (
        "The Caesar Cipher is one of the simplest and oldest known encryption techniques, "
        "attributed to Julius Caesar. It's a type of substitution cipher where each "
        "letter in the plaintext is shifted a fixed number of positions down or up the alphabet. "
        "The cipher relies on a 'shift' value, which is the number of positions each letter "
        "will be moved. For example, with a shift of 3: 'A' becomes 'D', 'B' becomes 'E',  "
        "'Z' becomes 'C' (wrapping back to the beginning of the alphabet). <br> "
        "Caesar Cipher is easy to break, especially with brute force, because there "
        "are only 26 possible shifts for the English alphabet. Due to its simplicity "
        "and low security, it's primarily used for educational purposes rather than "
        "for secure communication. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Caesar_cipher>Wikipedia</a><br>"
        "<a href=https://www.geeksforgeeks.org/caesar-cipher-in-cryptography>Geeks for Geeks</a>")

        self.setWindowTitle("Caesar Cipher")
        self.setFixedSize(700, 700)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        shift_label = QLabel("Enter positive shift for encryption:", parent=self)
        shift_label.setGeometry(10, 120, 300, 50)
        self.shift_input = DefaultQLineEditStyle(parent=self, int_validator = True)
        self.shift_input.setGeometry(250, 120, 50, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_encryption)
        encrypt_button.setGeometry(350, 120, 100, 50)

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 180, 680, 100)
        self.ciphertext_label.setReadOnly(True)
        self.ciphertext_label.hide()

        bacon_label = QLabel("Give text encrypted with caesar cipher:", parent=self)
        bacon_label.setGeometry(250, 300, 300, 50)
        self.bacon_input = DefaultQLineEditStyle(parent=self)
        self.bacon_input.setGeometry(10, 350, 680, 50)

        negative_shift_label = QLabel("Enter negative shift for decryption:", parent=self)
        negative_shift_label.setGeometry(10, 410, 300, 50)
        self.negative_shift_input = DefaultQLineEditStyle(parent=self, int_validator = True)
        self.negative_shift_input.setGeometry(250, 410, 50, 50)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, command=self.call_decryption)
        decrypt_button.setGeometry(350, 410, 100, 50)

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
                if self.shift_input.text():
                    input = self.plaintext_input.text()
                    shift = int(self.shift_input.text())

                    obj = Caesar_CipherImp(text=input, shift=shift)
                    ciphertext = obj.caesar_cipher_enc_dec(input, shift)

                    self.ciphertext_label.clear()
                    self.ciphertext_label.setHtml(f"<b>Ciphertext:</b><br>{ciphertext}")
                    self.ciphertext_label.show()
                else:
                    raise ValueError('Please enter encryption shift.')
            else:
                raise ValueError('Please enter plaintext.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def call_decryption(self):
        try:
            if self.bacon_input.text():
                if self.negative_shift_input.text():
                    input = self.bacon_input.text()
                    shift = int(self.negative_shift_input.text())

                    obj = Caesar_CipherImp(text=input, shift=shift)
                    decrypted_input = obj.caesar_cipher_enc_dec(input, shift)

                    self.decrypted_text_label.clear()
                    self.decrypted_text_label.setHtml(f"<b>Decrypted text:</b><br>{decrypted_input}")
                    self.decrypted_text_label.show()
                else:
                    raise ValueError('Please enter decryption shift.')
            else:
                raise ValueError('Please enter ciphertext.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
