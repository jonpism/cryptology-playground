from PyQt6 import QtWidgets, QtCore, QtGui
from DefaultStyles.button_style import DefaultButtonStyle

class AsymmetricPageUI:
    
    def __init__(self, parent=None):
        self.parent = parent
        self.setup_asymmetric_ui()

    def setup_asymmetric_ui(self):
        """Set up the asymmetric encryption page, label, and buttons."""
        self.AsymmetricPage = QtWidgets.QWidget(parent=self.parent)
        self.AsymmetricPage.setObjectName("AsymmetricPage")

        self.AsymmetricLabel = QtWidgets.QLabel(parent=self.AsymmetricPage)
        self.AsymmetricLabel.setGeometry(QtCore.QRect(10, -1, 1041, 51))
        self.AsymmetricLabel.setText("Asymmetric Encryption")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.AsymmetricLabel.setFont(font)
        self.AsymmetricLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.AsymmetricLabel.setObjectName("AsymmetricLabel")

        self.create_asymmetric_buttons()

    def create_asymmetric_buttons(self):
        button_data = [
        ("Certificate Signing Request", "CSRButton"),
        ("Diffie-Hellman Key Exchange", "DHKeyExchangeButton"),
        ("Digital Signature Algorithm", "DSAButton"),
        ("El Gamal", "ElGamalButton"),
        ("RSA", "RSAButton"),
        ("RSA Wiener Attack", "RSAWienerAttackButton"),
        ("Cramer-Shoup Encryption", "CramerShoupEncButton"),
        ("Cramer-Shoup Decryption", "CramerShoupDecButton"),
        ("X509 Self Signed Certificate", "X509SelfSignedButton"),
        ("Paillier Encryption", "PaillierEncButton"),
        ("Paillier Decryption", "PaillierDecButton"),
        ("ECDSA", "ECDSAButton"),
        ("ECDH", "ECDHButton"),
        ("EdDSA", "EdDSAButton"),
        ("NTRU Encrypt", "NTRUEncryptButton"),
        ("Kyber KEM Encapsulation", "KyberKEMButton"),
        ("Kyber KEM Decapsulation", "KyberKEMDecButton"),
    ]

        self.asymmetric_buttons = {}
        start_x = 20
        start_y = 70
        btn_width = 220
        btn_height = 40
        h_spacing = 40
        v_spacing = 30
        max_cols = 4

        for index, (text, name) in enumerate(button_data):
            row = index // max_cols
            col = index % max_cols
            x = start_x + col * (btn_width + h_spacing)
            y = start_y + row * (btn_height + v_spacing)

            button = DefaultButtonStyle(text, parent=self.AsymmetricPage, object_name=name)
            button.setGeometry(QtCore.QRect(x, y, btn_width, btn_height))
            self.asymmetric_buttons[name] = button