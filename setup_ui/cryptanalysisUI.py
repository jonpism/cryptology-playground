from PyQt6 import QtWidgets, QtCore, QtGui
from DefaultStyles.button_style import DefaultButtonStyle

class CryptanalysisPageUI:
    def __init__(self, parent=None):
        self.parent = parent
        self.setup_cryptanalysis_ui()

    def setup_cryptanalysis_ui(self):
        """Set up the cryptanalysis page, label, and buttons."""
        self.CryptanalysisPage = QtWidgets.QWidget(parent=self.parent)
        self.CryptanalysisPage.setObjectName("CryptanalysisPage")

        self.CryptanalysisLabel = QtWidgets.QLabel(parent=self.CryptanalysisPage)
        self.CryptanalysisLabel.setGeometry(QtCore.QRect(10, 0, 1041, 51))
        self.CryptanalysisLabel.setText("Cryptanalysis")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.CryptanalysisLabel.setFont(font)
        self.CryptanalysisLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CryptanalysisLabel.setObjectName("CryptanalysisLabel")

        self.create_cryptanalysis_buttons()

    def create_cryptanalysis_buttons(self):
        """Create uniformly sized and aligned buttons for the Cryptanalysis page."""
        button_data = [
            ("Known-Plaintext Analysis", "KPAButton"),
            ("Chosen-Plaintext Analysis", "CPAButton"),
            ("Ciphertext-Only Analysis", "COAButton"),
            ("Adaptive Chosen-Plaintext Attack", "ACPAButton"),
            ("Birthday Attack", "BirthdayAttackButton"),
            ("Side-channel Attack", "SideChannelAButton"),
            ("MITM Attack", "MITMButton"),
            ("Brute force Attack", "BruteForceAButton"),
            ("Differential cryptanalysis", "DiffAnalysisButton"),
            ("Related-key Attack", "RelatedKeyAButton"),
            ("Boomerang Attack", "BoomerangAButton"),
            ("Davies' Attack", "DaviesAttackButton"),
            ("Harvest now, decrypt later", "HarvestNowDLButton"),
            ("Slide Attack", "SlideAttackButton"),
            ("Integral cryptanalysis", "IntegralCryptanalysisButton"),
            ("Linear cryptanalysis", "LinearCryptanalysisButton"),
            ("Mod-n cryptanalysis", "ModnCryptanalysisButton"),
            ("XSL Attack", "XSLAttackButton"),
            ("Rainbow Table", "RainbowTableButton"),
            ("Black-bag cryptanalysis", "BlackBagCButton"),
            ("Power Analysis", "PowerAnalysisButton"),
            ("Replay Attack", "ReplayAttackButton"),
            ("Rubber-hose cryptanalysis", "RubberHoseCButton"),
            ("Timing Analysis", "TimingAnalysisButton")
        ]

        self.cryptanalysis_buttons = {}
        start_x = 40
        start_y = 80
        btn_width = 260
        btn_height = 40
        h_spacing = 50
        v_spacing = 20
        max_cols = 3

        for index, (text, name) in enumerate(button_data):
            row = index // max_cols
            col = index % max_cols
            x = start_x + col * (btn_width + h_spacing)
            y = start_y + row * (btn_height + v_spacing)

            button = DefaultButtonStyle(text, parent=self.CryptanalysisPage, object_name=name)
            button.setGeometry(QtCore.QRect(x, y, btn_width, btn_height))
            self.cryptanalysis_buttons[name] = button
