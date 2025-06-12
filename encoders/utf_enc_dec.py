from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
import ast

class TexttoCharcodeWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About UTF"
        msgbox_txt = (
            "Unicode Transformation Formats (UTFs) are a set of methods "
            "used to encode Unicode characters so they can be efficiently "
            "represented in computer systems. Unicode itself is a "
            "standardized encoding system that assigns a unique code point "
            "(an integer) to every character across different languages, scripts, "
            "and symbols worldwide. However, storing or transmitting these "
            "code points directly as integers isn't always practical, "
            "so Unicode Transformation Formats come into play to encode "
            "these code points into sequences of bytes. <br>"
            "<b>UTF-8:</b> UTF-8 is the most widely used Unicode encoding "
            "and is variable-length. It uses 1 to 4 bytes to represent a character.<br>"
            "<b>UTF-16:</b> UTF-16 is also a variable-length encoding, using either 2 or 4 bytes. <br>"
            "<b>UTF-32:</b> UTF-32 is a fixed-length encoding that uses 4 bytes for every "
            "character, regardless of the code point. <br><br>"
            "Useful links: <br>"
            "<a href=###>Wikipedia</a><br>"
            "<a href=>Geeks for Geeks</a>")

        self.setWindowTitle("Unicode Transformation Formats (Text to UTF bytes)")
        self.setFixedSize(700, 700)

        # Plaintext
        plaintext_label = QLabel("Give text:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        utf_label = QLabel("Format:", parent=self)
        utf_label.setGeometry(340, 110, 120, 50)
        self.utf_options = DefaultQComboBoxStyle(parent=self, items=["utf-8", "utf-16", "utf-32"])
        self.utf_options.setGeometry(320, 160, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.to_charcode)
        submit_button.setGeometry(300, 230, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 330, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_charcode(self):
        txt = self.plaintext_input.text()
        encoding = self.utf_options.currentText()
        encoded = self.encode(txt, encoding)
        self.result_label.clear()
        self.result_label.setHtml(f"<b>{encoding}:</b><br>{str(encoded)}")
        self.result_label.show()

    def encode(self, text: str, encoding: str) -> bytes:
        try:
            encoded_bytes = text.encode(encoding)
            return encoded_bytes
        except UnicodeEncodeError as e:
            print(f"Encoding Error: {e}")
            return None

class CharcodetoTextWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About UTF"
        msgbox_txt = (
            "Unicode Transformation Formats (UTFs) are a set of methods "
            "used to encode Unicode characters so they can be efficiently "
            "represented in computer systems. Unicode itself is a "
            "standardized encoding system that assigns a unique code point "
            "(an integer) to every character across different languages, scripts, "
            "and symbols worldwide. However, storing or transmitting these "
            "code points directly as integers isn't always practical, "
            "so Unicode Transformation Formats come into play to encode "
            "these code points into sequences of bytes. <br>"
            "<b>UTF-8:</b> UTF-8 is the most widely used Unicode encoding "
            "and is variable-length. It uses 1 to 4 bytes to represent a character.<br>"
            "<b>UTF-16:</b> UTF-16 is also a variable-length encoding, using either 2 or 4 bytes. <br>"
            "<b>UTF-32:</b> UTF-32 is a fixed-length encoding that uses 4 bytes for every "
            "character, regardless of the code point. <br><br>"
            "Useful links: <br>"
            "<a href=###>Wikipedia</a><br>"
            "<a href=>Geeks for Geeks</a>")

        self.setWindowTitle("Unicode Transformation Formats (UTF bytes to Text)")
        self.setFixedSize(700, 700)

        # Plaintext
        charcode_input_label = QLabel("Give Charcode (bytes only):", parent=self)
        charcode_input_label.setGeometry(300, 10, 200, 50)
        self.charcode_input = DefaultQLineEditStyle(parent=self)
        self.charcode_input.setGeometry(10, 60, 680, 50)

        utf_label = QLabel("Format:", parent=self)
        utf_label.setGeometry(340, 110, 120, 50)
        self.utf_options = DefaultQComboBoxStyle(parent=self, items=["utf-8", "utf-16", "utf-32"])
        self.utf_options.setGeometry(320, 160, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.to_text)
        submit_button.setGeometry(300, 230, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 330, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_text(self):
        chrcode = self.charcode_input.text()
        encoding = self.utf_options.currentText()
        try:
            chrcode_bytes = ast.literal_eval(chrcode)
            if isinstance(chrcode_bytes, bytes):
                decoded = self.decode_charcode(chrcode_bytes, encoding)
            else:
                raise ValueError("Input is not a valid byte string.")
        except (ValueError, SyntaxError) as e:
            print(f"Error converting to bytes: {e}")
            decoded = None

        self.result_label.clear()
        self.result_label.setHtml(f"<b>{encoding}:</b><br>{str(decoded)}")
        self.result_label.show()

    def decode_charcode(self, data: bytes, encoding: str) -> str:
        try:
            decoded_text = data.decode(encoding)
            return decoded_text
        except UnicodeDecodeError as e:
            print(f"Decoding Error: {e}")
            return None
