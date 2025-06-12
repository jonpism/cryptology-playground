from PyQt6 import QtWidgets, QtCore, QtGui
from DefaultStyles.button_style import DefaultButtonStyle

class ConvertersPageUI:
    def __init__(self, parent=None):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Set up the converters page, label, and buttons."""
        self.ConvertersPage = QtWidgets.QWidget(parent=self.parent)
        self.ConvertersPage.setObjectName("ConvertersPage")

        self.ConvertersLabel = QtWidgets.QLabel(parent=self.ConvertersPage)
        self.ConvertersLabel.setGeometry(QtCore.QRect(10, 0, 1041, 51))
        self.ConvertersLabel.setText("Converters")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.ConvertersLabel.setFont(font)
        self.ConvertersLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ConvertersLabel.setObjectName("ConvertersLabel")

        self.create_buttons()

    def create_buttons(self):
        button_data = [
            ("Text to Octal", "TexttoOctalButton"),
            ("Octal to Text", "OctaltoTextButton"),
            ("Text to Binary", "TxttoBinButton"),
            ("Binary to Text", "BintoTxtButton"),
            ("Text to ASCII", "TxttoASCIIButton"),
            ("ASCII to Text", "ASCIItoTxtButton"),
            ("Codepoint Converter", "CodepointConverterButton"),
            ("Decimal to Binary", "DecimaltoBinButton"),
            ("Binary to Decimal", "BintoDecimalButton"),
            ("Text to Hex", "TxttoHexButton"),
            ("Hex to Text", "HextoTxtButton"),
            ("Decimal to Radix", "DectoRadixButton"),
            ("Radix to Decimal", "RadixtoDecButton"),
            ("Decimal to BCD", "DectoBCDButton"),
            ("BCD to Decimal", "BCDtoDecButton"),
            ("Char to HTML Entity", "ChartoHTMLEntityBtn"),
            ("HTML Entity to Char", "HTMLEntitytoCharBtn"),
            ("PEM to DER", "PEMtoDERButton"),
            ("DER to PEM", "DERtoPEMButton"),
            ("To UNIX Timestamp", "ToUnixButton"),
            ("From UNIX Timestamp", "FromUnixButton"),
            ("to NATO Alphabet", "toNATOButton"),
            ("from NATO Alphabet", "fromNATOButton")
        ]

        self.converters_buttons = {}
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

            button = DefaultButtonStyle(text, parent=self.ConvertersPage, object_name=name)
            button.setGeometry(QtCore.QRect(x, y, btn_width, btn_height))
            self.converters_buttons[name] = button
