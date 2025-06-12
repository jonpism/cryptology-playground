from PyQt6 import QtWidgets, QtCore, QtGui
from DefaultStyles.button_style import DefaultButtonStyle

class SymmetricPageUI:
    
    def __init__(self, parent=None):
        self.parent = parent
        self.setup_symmetric_ui()

    def setup_symmetric_ui(self):
        """Set up the symmetric encryption page, label, and buttons."""
        self.SymmetricPage = QtWidgets.QWidget(parent=self.parent)
        self.SymmetricPage.setObjectName("SymmetricPage")

        self.SymmetricLabel = QtWidgets.QLabel(parent=self.SymmetricPage)
        self.SymmetricLabel.setGeometry(QtCore.QRect(10, 0, 1041, 51))
        self.SymmetricLabel.setText("Symmetric Encryption")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.SymmetricLabel.setFont(font)
        self.SymmetricLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SymmetricLabel.setObjectName("SymmetricLabel")

        self.create_symmetric_buttons()

    def create_symmetric_buttons(self):
        button_data = [
            ("AES Encryption", "AESEncButton"),
            ("AES Decryption", "AESDecButton"),
            ("DES Encryption", "DESEncButton"),
            ("DES Decryption", "DESDecButton"),
            ("Blowfish", "BlowfishButton"),
            ("Camellia", "CamelliaButton"),
            ("RC2 Encryption", "RC2EncButton"),
            ("RC2 Decryption", "RC2DecButton"),
            ("RC5 Encryption", "RC5EncButton"),
            ("RC5 Decryption", "RC5DecButton"),
            ("Serpent", "SerpentButton"),
            ("3DES Encryption", "TripleDESEncButton"),
            ("3DES Decryption", "TripleDESDecButton"),
            ("FERNET", "FERNETButton"),
            ("Twofish", "TwofishButton"),
        ]

        self.symmetric_buttons = {}
        start_x = 50
        start_y = 80
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

            button = DefaultButtonStyle(text, parent=self.SymmetricPage, object_name=name)
            button.setGeometry(QtCore.QRect(x, y, btn_width, btn_height))
            self.symmetric_buttons[name] = button
