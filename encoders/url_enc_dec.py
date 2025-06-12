from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
import urllib.parse

class URLDecodeWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About URL Encode-Decode"
        msgbox_txt = (
        "URL encoding, also known as percent encoding, is a method "
        "used to encode special characters in a Uniform Resource Locator (URL) "
        "so they can be safely transmitted over the Internet. URLs can only be "
        "sent over the Internet using the ASCII character set. Since URLs often "
        "contain characters outside the ASCII set, URL encoding is used to "
        "convert them into a valid ASCII format. URL encoding replaces non-ASCII "
        "characters or reserved characters with a '%' followed by two hexadecimal "
        "digits representing the character’s ASCII code. For example, a space "
        "character, which is not allowed in a URL, is encoded as %20 or +. <br>"
        "e.g: https://example.com/search?q=C++ programming becomes: "
        "https://example.com/search?q=C%2B%2B%20programming <br><br>"
        "Useful links: <br>"
        "<a href=https://example.com/search?q=C%2B%2B%20programming>Wikipedia</a>")

        self.setWindowTitle("URL Decode")
        self.setFixedSize(700, 500)

        # URL Input
        url_label = QLabel("Give URL:", parent=self)
        url_label.setGeometry(300, 10, 100, 50)
        self.url_input = DefaultQLineEditStyle(parent=self)
        self.url_input.setGeometry(10, 60, 680, 50)

        decode_button = DefaultButtonStyle("Decode", parent=self, command=self.call_url_decode)
        decode_button.setGeometry(300, 160, 100, 50)

        self.decoded_text_label = QTextEdit(parent=self)
        self.decoded_text_label.setGeometry(10, 230, 680, 100)
        self.decoded_text_label.setReadOnly(True)
        self.decoded_text_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_url_decode(self):
        try:
            input = self.url_input.text()
            if not input:
                raise ValueError('Please enter url input.')
            decoded = self.url_to_text_converter(input)
            decoded = str(decoded)

            self.decoded_text_label.clear()
            self.decoded_text_label.setHtml(f"<b>Decoded text:</b><br>{str(decoded)}")
            self.decoded_text_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def url_to_text_converter(self, input):
        return urllib.parse.unquote_plus(input)

# =======================================================================================================================

class URLEncodeWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About URL Encode-Decode"
        msgbox_txt = (
        "URL encoding, also known as percent encoding, is a method "
        "used to encode special characters in a Uniform Resource Locator (URL) "
        "so they can be safely transmitted over the Internet. URLs can only be "
        "sent over the Internet using the ASCII character set. Since URLs often "
        "contain characters outside the ASCII set, URL encoding is used to "
        "convert them into a valid ASCII format. URL encoding replaces non-ASCII "
        "characters or reserved characters with a '%' followed by two hexadecimal "
        "digits representing the character’s ASCII code. For example, a space "
        "character, which is not allowed in a URL, is encoded as %20 or +. <br>"
        "e.g: https://example.com/search?q=C++ programming becomes: "
        "https://example.com/search?q=C%2B%2B%20programming <br><br>"
        "Useful links: <br>"
        "<a href=https://example.com/search?q=C%2B%2B%20programming>Wikipedia</a>")

        self.setWindowTitle("URL Encode")
        self.setFixedSize(700, 500)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        encode_button = DefaultButtonStyle("Encode", parent=self, command=self.call_url_encode)
        encode_button.setGeometry(300, 160, 100, 50)

        self.encoded_text_label = QTextEdit(parent=self)
        self.encoded_text_label.setGeometry(10, 230, 680, 100)
        self.encoded_text_label.setReadOnly(True)
        self.encoded_text_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_url_encode(self):
        try:
            input = self.plaintext_input.text()
            if not input:
                raise ValueError('Please enter plaintext.')
            encoded = self.text_to_url_converter(input)
            encoded = str(encoded)

            self.encoded_text_label.clear()
            self.encoded_text_label.setHtml(f"<b>Encoded text:</b><br>{str(encoded)}")
            self.encoded_text_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def text_to_url_converter(self, input):
        return urllib.parse.quote_plus(input)
