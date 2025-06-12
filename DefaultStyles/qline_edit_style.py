from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QIntValidator

class DefaultQLineEditStyle(QtWidgets.QLineEdit):

    def __init__(self, placeholder_text="", parent=None, object_name=None, int_validator = None, max_length=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setObjectName(object_name if object_name else placeholder_text)
        self.setStyleSheet(self.get_style())
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        if int_validator:
            self.setValidator(QIntValidator(-2147483648, 2147483647, self))
        if max_length:
            self.setMaxLength(max_length)

    def get_style(self):
        return """
            border-radius: 15px; 
            border: 2px solid #5D6D7E;"""