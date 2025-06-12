from PyQt6 import QtWidgets, QtCore, QtGui
from DefaultStyles.button_style import DefaultButtonStyle

class OtherToolsPageUI:

    def __init__(self, parent=None):
        self.parent = parent
        self.setup_other_tools_ui()

    def setup_other_tools_ui(self):
        """Set up the other tools page, label, and buttons."""
        self.OtherToolsPage = QtWidgets.QWidget(parent=self.parent)
        self.OtherToolsPage.setObjectName("OtherToolsPage")

        self.OtherToolsLabel = QtWidgets.QLabel(parent=self.OtherToolsPage)
        self.OtherToolsLabel.setGeometry(QtCore.QRect(10, 0, 1041, 51))
        self.OtherToolsLabel.setText("Other Tools")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.OtherToolsLabel.setFont(font)
        self.OtherToolsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.OtherToolsLabel.setObjectName("OtherToolsLabel")

        self.create_other_tools_buttons()

    def create_other_tools_buttons(self):
        button_data = [
            ("Circular Bit Shift", "CircBitShiftButton"),
            ("Frequency Analysis", "FreqAnalysisButton"),
            ("One Time Pad", "OTPButton"),
            ("PBKDF2", "PBKDF2Button"),
            ("Prime Number Generator", "PrimeNumGenButton"),
            ("P-R Number Generator", "PRNGButton"),
            ("RSA Key Generator", "RSAKeyGenButton"),
            ("Strong Password Generator", "PwdGenButton"),
            ("Scrypt", "ScryptButton"),
            ("XOR Operation", "XORButton"),
            ("Reverse Text", "ReverseTextButton"),
            ("Integer Factorization", "IntFactorButton"),
            ("Swap Endianess", "SwapEndianButton"),
            ("HMAC", "HMACButton"),
            ("ASN1 Custom Encode", "ASN1EncButton"),
            ("ASN1 Custom Decode", "ASN1DecButton"),
            ("Argon2 KDF", "Argon2Button"),
            ("Show on Map", "ShowOnMapButton"),
            ("Show on Map 2", "ShowOnMap2Button"),
            ("EC Key Pair Window", "ECKeyPairButton"),
            ("Entropy", "EntropyButton"),
            ("Data differencing", "DataDiffButton"),
            ("Data compression", "DataCompressionButton"),
            ("Randomness Tester", "RandomnessTesterButton"),
            ("PGP Key Pair Generate", "PGPKeyPairButton"),
            ("DSA Key Pair Generate", "DSAKeyPairGenButton"),
            ("EdDSA Key Pair Generate", "EdDSAKeyPairGenButton"),
            ("Generate Lorem Ipsum", "LoremIpsumGenButton"),
            ("Mod calculator", "ModCalcButton"),
            ("JWT Sign", "JWTSignButton"),
            ("JWT Verify", "JWTVerifyButton"),
            ("JWT Decode", "JWTDecodeButton"),
            ("Generate QR Code", "QRCodeGenButton"),
        ]

        self.other_tools_buttons = {}
        start_x = 20
        start_y = 60
        btn_width = 220
        btn_height = 40
        h_spacing = 20
        v_spacing = 20
        max_cols = 4

        for index, (text, name) in enumerate(button_data):
            row = index // max_cols
            col = index % max_cols
            x = start_x + col * (btn_width + h_spacing)
            y = start_y + row * (btn_height + v_spacing)

            button = DefaultButtonStyle(text, parent=self.OtherToolsPage, object_name=name)
            button.setGeometry(QtCore.QRect(x, y, btn_width, btn_height))
            self.other_tools_buttons[name] = button
