from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class ROT47Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About ROT47"
        msgbox_txt = (
        "ROT47 is an extension of the ROT13 cipher but works on a wider range of "
        "ASCII characters, specifically characters with ASCII codes from 33 to 126. "
        "This includes not only letters but also numbers and many special characters, "
        "making it more versatile than ROT13. Like ROT13, ROT47 shifts characters "
        "by 47 positions in a circular fashion: <br> "
        "ASCII characters 33 to 126 are shifted by 47 positions. <br>  "
        "If the shifted position exceeds 126, it wraps around back to 33. "
        "Applying ROT47 twice returns the original text, as it's a symmetric transformation. "
        " "
        ""
        "<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/ROT13#Variants>Wikipedia</a><br>")

        self.setWindowTitle("ROT47")
        self.setFixedSize(700, 400)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_rot47)
        encrypt_button.setGeometry(300, 160, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 230, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        
    def call_rot47(self):
        try:
            if not self.plaintext_input.text():
                raise ValueError('Please enter plaintext.')
            input = self.plaintext_input.text()
            encrypted_input = self.rot47_encryption(input)

            self.encrypted_text_label.clear()
            self.encrypted_text_label.setHtml(f"<b>Ciphertext:</b><br>{str(encrypted_input)}")
            self.encrypted_text_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def rot47_encryption(self, s):
        x = []
        for i in range(len(s)):
            j = ord(s[i])
            if j >= 33 and j <= 126:
                x.append(chr(33 + ((j + 14) % 94)))
            else:
                x.append(s[i])
        return ''.join(x)
