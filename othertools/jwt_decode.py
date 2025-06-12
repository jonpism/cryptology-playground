from PyQt6.QtWidgets                import QWidget, QLabel, QMessageBox, QTextEdit
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qtextedit_style  import DefaultQTextEditStyle
import jwt, json

class JWTDecodeWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About JWT Decode Tool"
        msgbox_txt = ("...")

        self.setWindowTitle("JWT Decode - JSON Web Token Decode")
        self.setFixedSize(700, 800)

        