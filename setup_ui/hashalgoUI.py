from PyQt6 import QtWidgets, QtCore, QtGui
from DefaultStyles.button_style import DefaultButtonStyle

class HashAlgoPageUI:
    
    def __init__(self, parent=None):
        self.parent = parent
        self.setup_hashalgo_ui()

    def setup_hashalgo_ui(self):
        """Set up the hashing algorithms page, label, and buttons."""
        self.HashAlgoPage = QtWidgets.QWidget(parent=self.parent)
        self.HashAlgoPage.setObjectName("HashAlgoPage")

        self.HashAlgoLabel = QtWidgets.QLabel(parent=self.HashAlgoPage)
        self.HashAlgoLabel.setGeometry(QtCore.QRect(10, 0, 1041, 51))
        self.HashAlgoLabel.setText("Hashing Algorithms")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.HashAlgoLabel.setFont(font)
        self.HashAlgoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.HashAlgoLabel.setObjectName("HashAlgoLabel")

        self.create_hashalgo_buttons()

    def create_hashalgo_buttons(self):
        button_data = [
            ("Bcrypt", "BcryptButton"),
            ("BLAKE2", "BLAKE2Button"),
            ("BLAKE3", "BLAKE3Button"),
            ("MD4", "MD4Button"),
            ("MD5", "MD5Button"),
            ("RIPEMD-160", "RIPEMD160Button"),
            ("SHA-1", "SHA1Button"),
            ("SHA-256", "SHA256Button"),
            ("SHA-384", "SHA384Button"),
            ("SHA-512", "SHA512Button"),
            ("Whirlpool", "WhirlpoolButton"),
            ("GOST hash function", "GostHfButton"),
            ("Hash Identifier", "HashIdentifier"),
            ("Tiger", "TigerHashFunctionButton"),
            ("Keccak", "KeccakButton")
        ]

        self.hash_algo_buttons = {}
        start_x = 70
        start_y = 90
        btn_width = 200
        btn_height = 40
        h_spacing = 40
        v_spacing = 30
        max_cols = 4

        for index, (text, name) in enumerate(button_data):
            row = index // max_cols
            col = index % max_cols
            x = start_x + col * (btn_width + h_spacing)
            y = start_y + row * (btn_height + v_spacing)

            button = DefaultButtonStyle(text, parent=self.HashAlgoPage, object_name=name)
            button.setGeometry(QtCore.QRect(x, y, btn_width, btn_height))
            self.hash_algo_buttons[name] = button
