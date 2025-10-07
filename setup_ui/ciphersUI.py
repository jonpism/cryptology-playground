from PyQt6 import QtWidgets, QtCore, QtGui
from DefaultStyles.button_style import DefaultButtonStyle

class CiphersPageUI:
    
    def __init__(self, parent=None):
        self.parent = parent
        self.setup_ciphers_ui()

    def setup_ciphers_ui(self):
        """Set up the ciphers page, label, and buttons."""
        self.CiphersPage = QtWidgets.QWidget(parent=self.parent)
        self.CiphersPage.setObjectName("CiphersPage")

        self.CiphersLabel = QtWidgets.QLabel(parent=self.CiphersPage)
        self.CiphersLabel.setGeometry(QtCore.QRect(0, 0, 1041, 51))
        self.CiphersLabel.setText("Ciphers")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.CiphersLabel.setFont(font)
        self.CiphersLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CiphersLabel.setObjectName("CiphersLabel")

        self.create_ciphers_buttons()

    def create_ciphers_buttons(self):
        button_data = [
            ("Bacon Cipher", "BaconCipherButton"),
            ("Caesar Cipher", "CaesarCipherButton"),
            ("ChaCha20", "ChaCha20Button"),
            ("ChaCha20-Poly1305", "ChaChaPolyButton"),
            ("Enigma Machine", "EnigmaButton"),
            ("GOST (magma)", "GOSTButton"),
            ("Rabbit stream cipher", "RabbitButton"),
            ("ROT13", "ROT13Button"),
            ("ROT47", "ROT47Button"),
            ("ROT13 Bruteforce", "ROT13BFButton"),
            ("ROT47 Bruteforce", "ROT47BFButton"),
            ("Simple Substitution", "SimpleSubButton"),
            ("TEA", "TEAButton"),
            ("XTEA", "XTEAButton"),
            ("XXTEA", "XXTEAButton"),
            ("Vigenere Encryption", "VigenereEncButton"),
            ("Vigenere Decryption", "VigenereDecButton"),
            ("SM4 Encrypt", "SM4EncryptButton"),
            ("SM4 Decrypt", "SM4DecryptButton"),
            ("Bifid Cipher", "BifidCipherButton"),
            ("Affine Cipher Encryption", "AffineCipherEncButton"),
            ("Affine Cipher Decryption", "AffineCipherDecButton")
        ]

        self.ciphers_buttons = {}
        start_x = 20
        start_y = 70
        btn_width = 210
        btn_height = 40
        h_spacing = 40
        v_spacing = 30
        max_cols = 4

        for index, (text, name) in enumerate(button_data):
            row = index // max_cols
            col = index % max_cols
            x = start_x + col * (btn_width + h_spacing)
            y = start_y + row * (btn_height + v_spacing)

            button = DefaultButtonStyle(text, parent=self.CiphersPage, object_name=name)
            button.setGeometry(QtCore.QRect(x, y, btn_width, btn_height))
            self.ciphers_buttons[name] = button
