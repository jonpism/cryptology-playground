from PyQt6 import QtWidgets, QtGui

class DefaultQTextEditStyle(QtWidgets.QTextEdit):

    def __init__(self, placeholder_text="", parent=None, object_name=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setObjectName(object_name if object_name else placeholder_text)
        self.setStyleSheet(self.get_style())
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

    def get_style(self):
        return """
            border-radius: 5px; 
            border: 2px solid #5D6D7E;"""