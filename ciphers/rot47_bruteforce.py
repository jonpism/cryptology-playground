from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class ROT47BFWindow(QWidget):

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

        self.setWindowTitle("ROT47 Brute Force")
        self.setFixedSize(700, 600)

        # Ciphertext
        ciphertext_label = QLabel("Give ciphertext:", parent=self)
        ciphertext_label.setGeometry(300, 10, 120, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(10, 60, 680, 50)

        bf_button = DefaultButtonStyle("Submit", parent=self, command=self.call_bf)
        bf_button.setGeometry(300, 160, 100, 50)

        self.decrypted_text_label = QTextEdit(parent=self)
        self.decrypted_text_label.setGeometry(10, 220, 680, 300)
        self.decrypted_text_label.setReadOnly(True)
        self.decrypted_text_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_bf(self):
        try:
            if not self.ciphertext_input.text():
                raise ValueError('Please enter ciphertext.')
            ciphertext_input = self.ciphertext_input.text()
            decrypted_input = self.brute_force_rot47(ciphertext_input)

            self.decrypted_text_label.clear()
            self.decrypted_text_label.setHtml(f"<b>ROT47 Brute Force:</b><br>{str(decrypted_input)}")
            self.decrypted_text_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
    
    def rot47(self, text, shift):
        result = []
    
        for char in text:
            ascii_val = ord(char)
            # Only rotate characters within the printable ASCII range (33 to 126)
            if 33 <= ascii_val <= 126:
                rotated = 33 + (ascii_val - 33 + shift) % 94
                result.append(chr(rotated))
            else:
                result.append(char)  # Non-rotatable characters are kept the same

        return ''.join(result)

    def brute_force_rot47(self, text):
        decrypted_text = ""
        for shift in range(1, 94):  # Try all possible shifts in the range (1 to 93)
            decrypted_text += self.rot47(text, shift) + "\n"
        return decrypted_text
