from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class Hash_Identifier:

    HASH_ALGORITHMS = {
        'MD2': 32, 'MD4': 32, 'MD5': 32, 'SHA-1': 40, 'SHA-224': 56, 'SHA-256': 64, 'SHA-384': 96,
        'SHA-512': 128, 'SHA-512/224': 56, 'SHA-512/256': 64, 'SHA3-224': 56, 'SHA3-256': 64,
        'SHA3-384': 96, 'SHA3-512': 128, 'BLAKE2s': 64, 'BLAKE2b': 128, 'RIPEMD-160': 40, 'Whirlpool': 128,
        "CRC-8": 8, "CRC-16": 16, "CRC-32": 32, "CRC-64": 64, "BSD checksum": 16, "SYSV checksum": 16,
        "BLAKE3": 256, "MD6": 512, "Poly1305-AES": 128, "BLAKE-512": 512, "GOST": 256, "RIPEMD": 320, 
        "Tiger": 192,}

    def __init__(self, input_hash: str = None):
        self.input_hash = input_hash
        self.possible_algorithms = []

    def identify_hash(self) -> list:
        hash_length = len(self.input_hash)
        possible_algorithms = [
            algo for algo, length in self.HASH_ALGORITHMS.items() if length == hash_length]
        return possible_algorithms

    def get_possible_algorithms(self) -> list:
        return self.possible_algorithms

    def __repr__(self) -> str:
        return f"HashIdentifier(input_hash={self.input_hash}, possible_algorithms={self.possible_algorithms})"


class HashIdentifierWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Hash Identifier"
        msgbox_txt = (
        "<p>The Hash Identifier is designed to help you identify the possible hash "
        "algorithm used to generate a given hash string based on its length. It is useful in "
        "cryptography, digital forensics, and other security-related fields.</p>"
        "<p>Supported hash algorithms include but are not limited to:</p>"
        "<ul>"
        "<li>MD2, MD4, MD5</li>"
        "<li>SHA-1, SHA-224, SHA-256, SHA-384, SHA-512</li>"
        "<li>SHA3 family: SHA3-224, SHA3-256, SHA3-384, SHA3-512</li>"
        "<li>Checksum algorithms: CRC-8, CRC-16, CRC-32, CRC-64</li>"
        "<li>RIPEMD, Whirlpool, Tiger, BLAKE2s, BLAKE2b, BLAKE3</li>"
        "<li>Other algorithms: GOST, Poly1305-AES, BSD checksum, SYSV checksum</li>"
        "</ul>"
        "<p>To use this tool, simply enter your hash string in the input field and click 'Submit'. "
        "The algorithm will attempt to identify the possible hash algorithms based on the "
        "length of the provided hash.</p>"
        "<p><strong>Note:</strong> Some algorithms may have the same hash length, so multiple "
        "results may be returned.</p>"
        "<h3>Useful Links:</h3>"
        "<ul>"
        "<li><a href='https://en.wikipedia.org/wiki/Hash_function'>Hash Function - Wikipedia</a></li>"
        "<li><a href='https://www.cryptographyworld.com/hash.htm'>Cryptography World - Hash Functions</a></li>"
        "</ul>")

        self.setWindowTitle("Hash Identifier")
        self.setFixedSize(700, 500)

        # Text
        hash_input_label = QLabel("Give hash:", parent=self)
        hash_input_label.setGeometry(300, 10, 100, 50)
        self.hash_input = DefaultQLineEditStyle(parent=self)
        self.hash_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.hash_identifier_command)
        submit_button.setGeometry(300, 160, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 280, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def hash_identifier_command(self):
        try:
            hash = self.hash_input.text()
            if not hash:
                raise ValueError('Please enter hash value')

            h = Hash_Identifier(hash)

            possible_algorithms = h.identify_hash()

            self.result_label.clear()
            self.result_label.setHtml(h.__repr__())
            self.result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))