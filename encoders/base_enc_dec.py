from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
import base64, base45, base58, string, math

# ==================================================================================================================

class Base32Converter:
    @staticmethod
    def text_to_base32(text):
        """Convert text to Base32 encoding."""
        # text to bytes
        text_bytes = text.encode('utf-8')
        # bytes to Base32 encoding
        base32_encoded = base64.b32encode(text_bytes)
        # bytes to string
        return base32_encoded.decode('utf-8')

    @staticmethod
    def base32_to_text(base32_string):
        """Convert Base32 encoded string back to original text."""
        # Base32 string to bytes
        base32_bytes = base32_string.encode('utf-8')
        # Base32 to bytes decoding
        decoded_bytes = base64.b32decode(base32_bytes)
        # bytes to original text
        return decoded_bytes.decode('utf-8')

class BASE32Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Base32"
        msgbox_txt = (
        "BASE32 is a binary-to-text encoding scheme that is used to represent "
        "binary data in an ASCII string format. It is designed to encode data  "
        "in a way that is more efficient than some other encoding methods, "
        "such as BASE64, when dealing with systems that are case-insensitive or "
        "when working with text that needs to avoid special characters. "
        "The character set used in BASE32 is: ABCDEFGHIJKLMNOPQRSTUVWXYZ234567 "
        "Each character in the BASE32 alphabet encodes 5 bits of binary data "
        "(since 2**5 = 32). BASE32 uses the '=' character for padding to make "
        "the length of the encoded output a multiple of 8 characters, ensuring "
        "proper decoding. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Base32>Wikipedia</a><br>")

        self.setWindowTitle("BASE32")
        self.setFixedSize(700, 700)

        # Text
        text_input_label = QLabel("Give text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        to_base32_button = DefaultButtonStyle("To Base32", parent=self, command=self.to_base32)
        to_base32_button.setGeometry(300, 120, 100, 50)

        self.to_base32_result_label = QTextEdit(parent=self)
        self.to_base32_result_label.setGeometry(10, 200, 680, 100)
        self.to_base32_result_label.setReadOnly(True)
        self.to_base32_result_label.hide()

        # Base32 encoded
        encoded_input_label = QLabel("Give base32 encoded text:", parent=self)
        encoded_input_label.setGeometry(300, 300, 250, 50)
        self.encoded_input = DefaultQLineEditStyle(parent=self)
        self.encoded_input.setGeometry(10, 360, 680, 50)

        to_text_button = DefaultButtonStyle("To Text", parent=self, command=self.to_text)
        to_text_button.setGeometry(300, 420, 100, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 520, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.converter = Base32Converter()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_base32(self):
        try:
            text = self.text_input.text()

            encoded = self.converter.text_to_base32(text)

            self.to_base32_result_label.clear()
            self.to_base32_result_label.setHtml(f"<b>BASE32:</b><br>{str(encoded)}")
            self.to_base32_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def to_text(self):
        try:
            base32 = self.encoded_input.text()

            decoded = self.converter.base32_to_text(base32)

            self.to_text_result_label.clear()
            self.to_text_result_label.setHtml(f"<b>Decoded Text:</b><br>{str(decoded)}")
            self.to_text_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

# ==================================================================================================================

class BASE45Converter:

    def text_to_base45_converter(self, input):
        bytes = input.encode('utf-8')
        encoded = base45.b45encode(bytes)
        return encoded.decode('utf-8')

    def base45_to_text_converter(self, input):
        bytes = input.encode('utf-8')
        decoded = base45.b45decode(bytes)
        return decoded.decode('utf-8')


class BASE45Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Base45"
        msgbox_txt = (
        "Base45 is a relatively newer binary-to-text encoding scheme compared "
        "to common encoding schemes like Base64 and Base32. It has emerged with "
        "specific use cases where compact data representation is needed, "
        "especially in environments that may have character restrictions. "
        "A notable application of Base45 is in encoding information for EU "
        "Digital COVID Certificates. The Base45 character set includes the "
        "following characters:0-9 (digits), A-Z (uppercase letters), and "
        "space plus the characters: $%*+-./: <br> "
        "Each character in the Base45 alphabet represents 45 possible values, "
        "which is enough to encode 2 bytes (16 bits) into 3 characters (since "
        "452>256452>256, where 256 represents 8-bit data for a byte).<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Binary-to-text_encoding>Wikipedia</a><br>")

        self.setWindowTitle("BASE45")
        self.setFixedSize(700, 700)

        # Text
        text_input_label = QLabel("Give text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        to_base45_button = DefaultButtonStyle("To Base45", parent=self, command=self.to_base45)
        to_base45_button.setGeometry(300, 120, 100, 50)

        self.to_base45_result_label = QTextEdit(parent=self)
        self.to_base45_result_label.setGeometry(10, 200, 680, 100)
        self.to_base45_result_label.setReadOnly(True)
        self.to_base45_result_label.hide()

        # Base45 encoded
        encoded_input_label = QLabel("Give base45 encoded text:", parent=self)
        encoded_input_label.setGeometry(300, 300, 250, 50)
        self.encoded_input = DefaultQLineEditStyle(parent=self)
        self.encoded_input.setGeometry(10, 360, 680, 50)

        to_text_button = DefaultButtonStyle("To Text", parent=self, command=self.to_text)
        to_text_button.setGeometry(300, 420, 100, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 520, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.converter = BASE45Converter()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_base45(self):
        try:
            text = self.text_input.text()

            encoded = self.converter.text_to_base45_converter(text)

            self.to_base45_result_label.clear()
            self.to_base45_result_label.setHtml(f"<b>BASE45:</b><br>{str(encoded)}")
            self.to_base45_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def to_text(self):
        try:
            base45 = self.encoded_input.text()

            decoded = self.converter.base45_to_text_converter(base45)

            self.to_text_result_label.clear()
            self.to_text_result_label.setHtml(f"<b>Decoded Text:</b><br>{str(decoded)}")
            self.to_text_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

# ==================================================================================================================

class Base58Converter:

    @staticmethod
    def text_to_base58(text):
        """Convert text to Base58 encoding."""
        # text to bytes
        text_bytes = text.encode('utf-8')
        # bytes to Base58
        base58_encoded = base58.b58encode(text_bytes)
        # bytes to string
        return base58_encoded.decode('utf-8')

    @staticmethod
    def base58_to_text(base58_string):
        """Convert Base58 encoded string back to original text."""
        # Base58 to bytes
        base58_bytes = base58_string.encode('utf-8')
        # Base58 to bytes
        decoded_bytes = base58.b58decode(base58_bytes)
        # bytes to original text conversion
        return decoded_bytes.decode('utf-8')

class BASE58Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Base58"
        msgbox_txt = (
        "Base58 is a binary-to-text encoding scheme designed to "
        "represent large integers in a compact and human-friendly "
        "way. It is used in various applications where shortened "
        "representations of binary data are needed, particularly "
        "in cryptocurrencies and blockchain technology. Base58 "
        "uses a set of 58 alphanumeric characters: 123456789ABCDE"
        "FGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz. <br> "
        "e.g: A typical Bitcoin address might look like this: "
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa. This address is "
        "encoded in Base58Check.<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Binary-to-text_encoding>Wikipedia</a><br>")

        self.setWindowTitle("BASE58")
        self.setFixedSize(700, 700)

        # Text
        text_input_label = QLabel("Give text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        to_base58_button = DefaultButtonStyle("To Base58", parent=self, command=self.to_base58)
        to_base58_button.setGeometry(300, 120, 100, 50)

        self.to_base58_result_label = QTextEdit(parent=self)
        self.to_base58_result_label.setGeometry(10, 200, 680, 100)
        self.to_base58_result_label.setReadOnly(True)
        self.to_base58_result_label.hide()

        # Base58 encoded
        encoded_input_label = QLabel("Give base58 encoded text:", parent=self)
        encoded_input_label.setGeometry(300, 300, 250, 50)
        self.encoded_input = DefaultQLineEditStyle(parent=self)
        self.encoded_input.setGeometry(10, 360, 680, 50)

        to_text_button = DefaultButtonStyle("To Text", parent=self, command=self.to_text)
        to_text_button.setGeometry(300, 420, 100, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 520, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.converter = Base58Converter()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_base58(self):
        try:
            text = self.text_input.text()

            encoded = self.converter.text_to_base58(text)

            self.to_base58_result_label.clear()
            self.to_base58_result_label.setHtml(f"<b>BASE58:</b><br>{str(encoded)}")
            self.to_base58_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def to_text(self):
        try:
            base58 = self.encoded_input.text()

            decoded = self.converter.base58_to_text(base58)

            self.to_text_result_label.clear()
            self.to_text_result_label.setHtml(f"<b>Decoded Text:</b><br>{str(decoded)}")
            self.to_text_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

# ==================================================================================================================

class Base62Converter:

    BASE62_ALPHABET = string.digits + string.ascii_letters

    @staticmethod
    def text_to_base62(text):
        """Convert text to Base62 encoding."""
        # text to integer (representing the binary data of the text)
        text_bytes = text.encode('utf-8')
        int_value = int.from_bytes(text_bytes, 'big')
        # Convert the integer to a Base62 encoded string
        base62_encoded = Base62Converter.int_to_base62(int_value)
        return base62_encoded

    @staticmethod
    def base62_to_text(base62_string):
        """Convert Base62 encoded string back to original text."""
        # Base62 string to integer
        int_value = Base62Converter.base62_to_int(base62_string)
        # integer to bytes
        text_bytes = int_value.to_bytes((int_value.bit_length() + 7) // 8, 'big')
        return text_bytes.decode('utf-8')

    @staticmethod
    def int_to_base62(n):
        """Convert an integer to a Base62 string."""
        if n == 0:
            return Base62Converter.BASE62_ALPHABET[0]
        base62 = []
        base = len(Base62Converter.BASE62_ALPHABET)
        while n:
            n, rem = divmod(n, base)
            base62.append(Base62Converter.BASE62_ALPHABET[rem])
        return ''.join(reversed(base62))

    @staticmethod
    def base62_to_int(base62_string):
        """Convert a Base62 string back to an integer."""
        base = len(Base62Converter.BASE62_ALPHABET)
        int_value = 0
        for char in base62_string:
            int_value = int_value * base + Base62Converter.BASE62_ALPHABET.index(char)
        return int_value

class BASE62Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Base62"
        msgbox_txt = (
        "Base62 is a binary-to-text encoding scheme that is often used "
        "to represent large integers or binary data in a shorter and "
        "more human-readable form. It is commonly used in scenarios "
        "where data needs to be compact yet readable, such as URL "
        "shorteners, unique identifiers for database records, and cases "
        "where a high-density encoding is needed that can be transmitted "
        "using alphanumeric characters. The full character set for Base62 "
        "looks like this: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "
        "Base62 provides a compact representation. Since it uses 62 characters, "
        "it can represent data more efficiently than Base10, Base16, or Base32. "
        "For example, a shorter URL generated using Base62 is easier to type "
        "and more visually manageable. <br><br> "
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Base62>Wikipedia</a><br>")

        self.setWindowTitle("BASE62")
        self.setFixedSize(700, 700)

        # Text
        text_input_label = QLabel("Give text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        to_base62_button = DefaultButtonStyle("To Base62", parent=self, command=self.to_base62)
        to_base62_button.setGeometry(300, 120, 100, 50)

        self.to_base62_result_label = QTextEdit(parent=self)
        self.to_base62_result_label.setGeometry(10, 200, 680, 100)
        self.to_base62_result_label.setReadOnly(True)
        self.to_base62_result_label.hide()

        # Base62 encoded
        encoded_input_label = QLabel("Give base62 encoded text:", parent=self)
        encoded_input_label.setGeometry(300, 300, 250, 50)
        self.encoded_input = DefaultQLineEditStyle(parent=self)
        self.encoded_input.setGeometry(10, 360, 680, 50)

        to_text_button = DefaultButtonStyle("To Text", parent=self, command=self.to_text)
        to_text_button.setGeometry(300, 420, 100, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 520, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.converter = Base62Converter()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_base62(self):
        try:
            text = self.text_input.text()

            encoded = self.converter.text_to_base62(text)

            self.to_base62_result_label.clear()
            self.to_base62_result_label.setHtml(f"<b>BASE62:</b><br>{str(encoded)}")
            self.to_base62_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def to_text(self):
        try:
            base62 = self.encoded_input.text()

            decoded = self.converter.base62_to_text(base62)

            self.to_text_result_label.clear()
            self.to_text_result_label.setHtml(f"<b>Decoded Text:</b><br>{str(decoded)}")
            self.to_text_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

# ==================================================================================================================

class BASE64Converter:

    def text_to_base64(self, input):
        bytes = input.encode('utf-8')
        encoded = base64.b64encode(bytes)
        return encoded.decode('utf-8')

    def base64_to_text(self, input):
        bytes = input.encode('utf-8')
        decoded = base64.b64decode(bytes)
        return decoded.decode('utf-8')

class BASE64Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Base64"
        msgbox_txt = (
        "Base64 is a binary-to-text encoding scheme that represents binary "
        "data in an ASCII string format. It is commonly used to encode "
        "data when transmitting it over media that are designed to handle text, "
        "ensuring that the data remains intact without modification during transport. "
        "Here is the full set of characters used in Base64 encoding: <br>"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/ <br>"
        "Base64 is not a secure way to encode data; it's simply a reversible "
        "encoding mechanism. It's not intended to hide information, as anyone "
        "who understands Base64 can easily decode it. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Base64>Wikipedia</a><br>")

        self.setWindowTitle("BASE64")
        self.setFixedSize(700, 700)

        # Text
        text_input_label = QLabel("Give text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        to_base64_button = DefaultButtonStyle("To Base64", parent=self, command=self.to_base64)
        to_base64_button.setGeometry(300, 120, 100, 50)

        self.to_base64_result_label = QTextEdit(parent=self)
        self.to_base64_result_label.setGeometry(10, 200, 680, 100)
        self.to_base64_result_label.setReadOnly(True)
        self.to_base64_result_label.hide()

        # Base64 encoded
        encoded_input_label = QLabel("Give base64 encoded text:", parent=self)
        encoded_input_label.setGeometry(300, 300, 250, 50)
        self.encoded_input = DefaultQLineEditStyle(parent=self)
        self.encoded_input.setGeometry(10, 360, 680, 50)

        to_text_button = DefaultButtonStyle("To Text", parent=self, command=self.to_text)
        to_text_button.setGeometry(300, 420, 100, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 520, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.converter = BASE64Converter()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_base64(self):
        try:
            text = self.text_input.text()

            encoded = self.converter.text_to_base64(text)

            self.to_base64_result_label.clear()
            self.to_base64_result_label.setHtml(f"<b>BASE64:</b><br>{str(encoded)}")
            self.to_base64_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def to_text(self):
        try:
            base64 = self.encoded_input.text()

            decoded = self.converter.base64_to_text(base64)

            self.to_text_result_label.clear()
            self.to_text_result_label.setHtml(f"<b>Decoded Text:</b><br>{str(decoded)}")
            self.to_text_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

# ==================================================================================================================

class BASE85Converter:

    def text_to_base85(self, input):
        bytes = input.encode('utf-8')
        encoded = base64.b85encode(bytes)
        return encoded.decode('utf-8')

    def base85_to_text(self, input):
        bytes = input.encode('utf-8')
        decoded = base64.b85decode(bytes)
        return decoded.decode('utf-8')

class BASE85Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Base85"
        msgbox_txt = (
        "Base85, also known as Ascii85, is a binary-to-text encoding scheme "
        "used to encode binary data into a string of ASCII characters. "
        "This is useful when transmitting binary data over channels that are "
        "designed to handle only text, such as email or certain internet protocols. "
        "Base85 is more efficient than Base64. While Base64 uses 4 characters to "
        "represent every 3 bytes of binary data (a 33% increase in size), Base85 "
        "uses 5 characters to encode every 4 bytes of binary data, resulting in "
        "only a 25% increase in size. Thus, Base85 is more space-efficient. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Ascii85>Wikipedia</a><br>")

        self.setWindowTitle("BASE85")
        self.setFixedSize(700, 700)

        # Text
        text_input_label = QLabel("Give text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        to_base85_button = DefaultButtonStyle("To Base85", parent=self, command=self.to_base85)
        to_base85_button.setGeometry(300, 120, 100, 50)

        self.to_base85_result_label = QTextEdit(parent=self)
        self.to_base85_result_label.setGeometry(10, 200, 680, 100)
        self.to_base85_result_label.setReadOnly(True)
        self.to_base85_result_label.hide()

        # Base85 encoded
        encoded_input_label = QLabel("Give base85 encoded text:", parent=self)
        encoded_input_label.setGeometry(300, 300, 250, 50)
        self.encoded_input = DefaultQLineEditStyle(parent=self)
        self.encoded_input.setGeometry(10, 360, 680, 50)

        to_text_button = DefaultButtonStyle("To Text", parent=self, command=self.to_text)
        to_text_button.setGeometry(300, 420, 100, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 520, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.converter = BASE85Converter()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_base85(self):
        try:
            text = self.text_input.text()

            encoded = self.converter.text_to_base85(text)

            self.to_base85_result_label.clear()
            self.to_base85_result_label.setHtml(f"<b>BASE85:</b><br>{str(encoded)}")
            self.to_base85_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def to_text(self):
        try:
            base85 = self.encoded_input.text()

            decoded = self.converter.base85_to_text(base85)

            self.to_text_result_label.clear()
            self.to_text_result_label.setHtml(f"<b>Decoded Text:</b><br>{str(decoded)}")
            self.to_text_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

# ==================================================================================================================

class Base92Converter:
    # Base92 character set (ASCII printable characters, excluding '"' and '\')
    BASE92_ALPHABET = ''.join([chr(i) for i in range(33, 127) if i not in (34, 92)])
    BASE92_LEN = len(BASE92_ALPHABET)

    @staticmethod
    def text_to_base92(text):
        """Convert text to Base92 encoding."""
        # text to bytes
        text_bytes = text.encode('utf-8')
        # Convert bytes to an integer representation
        int_value = int.from_bytes(text_bytes, 'big')
        # Encode integer as Base92
        return Base92Converter.int_to_base92(int_value)

    @staticmethod
    def base92_to_text(base92_string):
        """Convert Base92 encoded string back to original text."""
        # Convert Base92 string to an integer
        int_value = Base92Converter.base92_to_int(base92_string)
        # Convert integer back to bytes
        byte_length = math.ceil(int_value.bit_length() / 8)
        text_bytes = int_value.to_bytes(byte_length, 'big')
        # Convert bytes to original text
        return text_bytes.decode('utf-8')

    @staticmethod
    def int_to_base92(n):
        """Convert an integer to a Base92 encoded string."""
        if n == 0:
            return Base92Converter.BASE92_ALPHABET[0]
        base92 = []
        while n:
            n, rem = divmod(n, Base92Converter.BASE92_LEN)
            base92.append(Base92Converter.BASE92_ALPHABET[rem])
        return ''.join(reversed(base92))

    @staticmethod
    def base92_to_int(base92_string):
        """Convert a Base92 string back to an integer."""
        int_value = 0
        for char in base92_string:
            int_value = int_value * Base92Converter.BASE92_LEN + Base92Converter.BASE92_ALPHABET.index(char)
        return int_value

class BASE92Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Base92"
        msgbox_txt = (
        "Base 92 is an encoding system designed to efficiently represent "
        "binary data using a subset of ASCII characters. It is similar to "
        "other encoding schemes like Base64, but it optimizes for cases where "
        "minimizing the output size is important. The idea behind Base 92 "
        "is to use a set of 92 printable ASCII characters to represent data, "
        "which reduces the expansion factor compared to Base64. The character "
        "set for Base 92 encoding includes printable ASCII characters, excluding "
        "characters that might cause issues in text processing or when displayed. "
        "Specifically, it uses a set of 92 characters selected from the printable "
        "range of ASCII characters (33 to 126). <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Binary-to-text_encoding>Wikipedia</a><br>")

        self.setWindowTitle("BASE92")
        self.setFixedSize(700, 700)

        # Text
        text_input_label = QLabel("Give text:", parent=self)
        text_input_label.setGeometry(300, 10, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        to_base85_button = DefaultButtonStyle("To Base92", parent=self, command=self.to_base92)
        to_base85_button.setGeometry(300, 120, 100, 50)

        self.to_base92_result_label = QTextEdit(parent=self)
        self.to_base92_result_label.setGeometry(10, 200, 680, 100)
        self.to_base92_result_label.setReadOnly(True)
        self.to_base92_result_label.hide()

        # Base92 encoded
        encoded_input_label = QLabel("Give base92 encoded text:", parent=self)
        encoded_input_label.setGeometry(300, 300, 250, 50)
        self.encoded_input = DefaultQLineEditStyle(parent=self)
        self.encoded_input.setGeometry(10, 360, 680, 50)

        to_text_button = DefaultButtonStyle("To Text", parent=self, command=self.to_text)
        to_text_button.setGeometry(300, 420, 100, 50)

        self.to_text_result_label = QTextEdit(parent=self)
        self.to_text_result_label.setGeometry(10, 520, 680, 100)
        self.to_text_result_label.setReadOnly(True)
        self.to_text_result_label.hide()

        self.converter = Base92Converter()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def to_base92(self):
        try:
            text = self.text_input.text()

            encoded = self.converter.text_to_base92(text)

            self.to_base92_result_label.clear()
            self.to_base92_result_label.setHtml(f"<b>BASE92:</b><br>{str(encoded)}")
            self.to_base92_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

    def to_text(self):
        try:
            base92 = self.encoded_input.text()

            decoded = self.converter.base92_to_text(base92)

            self.to_text_result_label.clear()
            self.to_text_result_label.setHtml(f"<b>Decoded Text:</b><br>{str(decoded)}")
            self.to_text_result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
