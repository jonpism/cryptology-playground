from PyQt6 import QtWidgets, QtCore, QtGui
from DefaultStyles.button_style import DefaultButtonStyle

class EncodersPageUI:

    def __init__(self, parent=None):
        self.parent = parent
        self.setup_encoders_ui()

    def setup_encoders_ui(self):
        """Set up the hashing algorithms page, label, and buttons."""
        self.EncodersPage = QtWidgets.QWidget(parent=self.parent)
        self.EncodersPage.setObjectName("EncodersPage")

        self.EncodersLabel = QtWidgets.QLabel(parent=self.EncodersPage)
        self.EncodersLabel.setGeometry(QtCore.QRect(0, 0, 1041, 51))
        self.EncodersLabel.setText("Encoders")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.EncodersLabel.setFont(font)
        self.EncodersLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.EncodersLabel.setObjectName("EncodersLabel")

        self.create_encoders_buttons()

    def create_encoders_buttons(self):
        button_data = [
            ("A1Z26 Encode", "A1Z26EncButton"),
            ("A1Z26 Decode", "A1Z26DecButton"),
            ("BASE32", "BASE32Button"),
            ("BASE45", "BASE45Button"),
            ("BASE58", "BASE58Button"),
            ("BASE62", "BASE62Button"),
            ("BASE64", "BASE64Button"),
            ("BASE85", "BASE85Button"),
            ("BASE92", "BASE92Button"),
            ("Braille", "BrailleButton"),
            ("Morse Code", "MorseCodeButton"),
            ("URL Encode", "URLEncButton"),
            ("URL Decode", "URLDecButton"),
            ("Text to Charcode", "TxttoCharcodeButton"),
            ("Charcode to Text", "CharcodetoTxtButton"),
            ("To Quoted Printable", "ToQPButton"),
            ("From Quoted Printable", "FromQPButton"),
            ("To BCD", "ToBCDButton"),
            ("From BCD", "FromBCDButton"),
            ("Punycode Encode", "PunycodeEncButton"),
            ("Punycode Decode", "PunycodeDecButton"),
        ]

        self.encoders_buttons = {}
        start_x = 60
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

            button = DefaultButtonStyle(text, parent=self.EncodersPage, object_name=name)
            button.setGeometry(QtCore.QRect(x, y, btn_width, btn_height))
            self.encoders_buttons[name] = button
