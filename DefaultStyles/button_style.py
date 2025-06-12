from PyQt6              import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets    import QMessageBox
from PyQt6.QtCore       import Qt
import os

base_dir = os.path.dirname(os.path.dirname(__file__)) # projet root directory
# icons for dark mode
help_icon_path = os.path.join(base_dir, 'icons', 'help_icon.png').replace("\\", "/")
settings_icon_path = os.path.join(base_dir, 'icons', 'settings_icon.png').replace("\\", "/")
sound_on_icon_path = os.path.join(base_dir, 'icons', 'sound_icon_on.png').replace("\\", "/")
sound_off_icon_path = os.path.join(base_dir, 'icons', 'sound_icon_off.png').replace("\\", "/")
# icons for light mode
help_icon_black_path = os.path.join(base_dir, 'icons', 'help_icon_black.png').replace("\\", "/")
settings_icon_black_path = os.path.join(base_dir, 'icons', 'settings_icon_black.png').replace("\\", "/")
sound_on_icon_black_path = os.path.join(base_dir, 'icons', 'sound_icon_on_black.png').replace("\\", "/")
sound_off_icon_black_path = os.path.join(base_dir, 'icons', 'sound_icon_off_black.png').replace("\\", "/")

class DefaultMenuButtonStyle(QtWidgets.QPushButton):

    def __init__(self, text, parent=None, object_name=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(object_name if object_name else text)

        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.setFont(font)

        self.setStyleSheet(self.get_style())
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
    
    def get_style(self):
        return """ 
        QPushButton {
            border-radius: 15px;
            border: 2px solid #5D6D7E;
            padding: 10px;
            min-width: 16px;
            min-height: 16px;
        }
        QPushButton:hover {
            background-color: grey;
        }
        QPushButton:pressed {
            background-color: #839192;
        }
        QPushButton:checked {
            background-color:#5D6D7E;
        }
        """

class DefaultButtonStyle(QtWidgets.QPushButton):

    def __init__(self, text, parent=None, object_name=None, command=None, music=None, bold=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(object_name if object_name else text)

        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(bold if bold else False)
        self.setFont(font)
        
        if music == None:
            self.setStyleSheet(self.get_style())

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        
        if command:
            self.clicked.connect(command)
    
    def update_theme_settings(self, theme_name):
        if theme_name == "dark":
            self.setStyleSheet(self.get_settings_style(dark=True))
        else:  # light
            self.setStyleSheet(self.get_settings_style(dark=False))
    
    def update_theme_help(self, theme_name):
        if theme_name == "dark":
            self.setStyleSheet(self.get_help_style(dark=True))
        else:  # light
            self.setStyleSheet(self.get_help_style(dark=False))
    
    def update_theme_music_on(self, theme_name):
        if theme_name == "dark":
            self.setStyleSheet(self.get_style_music_on(dark=True))
        else:  # light
            self.setStyleSheet(self.get_style_music_on(dark=False))
    
    def update_theme_music_off(self, theme_name):
        if theme_name == "dark":
            self.setStyleSheet(self.get_style_music_off(dark=True))
        else:  # light
            self.setStyleSheet(self.get_style_music_off(dark=False))

    def get_style(self):
        return """
        QPushButton {
            border-radius: 15px;
            border: 2px solid #5D6D7E;
            padding: 10px;
            min-width: 16px;
            min-height: 16px;
        }
        QPushButton:hover {
            background-color: grey;
        }
        QPushButton:pressed {
            background-color: #839192;
        }
        """
    
    @staticmethod
    def get_style_music_off(dark=True):
        icon_path = sound_off_icon_path if dark else sound_off_icon_black_path
        return f"""
        QPushButton {{
            border-radius: 25px;
            border: 2px solid #5D6D7E;
            image: url({icon_path});
            padding: 12px;
        }}
        QPushButton:hover {{
            background-color: grey;
        }}
        QPushButton:pressed {{
            background-color: #839192;
        }}"""
    
    @staticmethod
    def get_style_music_on(dark=True):
        icon_path = sound_on_icon_path if dark else sound_on_icon_black_path
        return f"""
        QPushButton {{
            border-radius: 25px;
            border: 2px solid #5D6D7E;
            padding: 10px;
            min-width: 16px;
            min-height: 16px;
            image: url({icon_path});
        }}
        QPushButton:hover {{
            background-color: grey;
        }}
        QPushButton:pressed {{
            background-color: #839192;
        }}"""
    
    @staticmethod
    def get_help_style(dark=True):
        icon_path = help_icon_path if dark else help_icon_black_path
        return f"""
        QPushButton {{
            border-radius: 25px;
            border: 2px solid #5D6D7E;
            padding: 10px;
            min-width: 16px;
            min-height: 16px;
            image: url({icon_path});
        }}
        QPushButton:hover {{
            background-color: grey;
        }}
        QPushButton:pressed {{
            background-color: #839192;
        }}
        QPushButton:checked {{
            background-color: #5D6D7E;
        }}"""
    
    @staticmethod
    def get_settings_style(dark=True):
        icon_path = settings_icon_path if dark else settings_icon_black_path
        return f"""
        QPushButton {{
        border-radius: 25px;
        border: 2px solid #5D6D7E;
        padding: 5px;
        min-width: 16px;
        min-height: 16px;
        image: url({icon_path});
        }}
        QPushButton:hover {{
            background-color: grey;
        }}
        QPushButton:pressed {{
            background-color: #839192;
        }}
        QPushButton:checked {{
            background-color: #5D6D7E;
        }}"""

    
class DefaultAboutButtonStyle(QtWidgets.QPushButton):

    def __init__(self, text, parent=None, object_name=None, txt=None, title=None, geometry=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(object_name if object_name else "DefaultAboutButton")
        self.title = title
        self.txt = txt
        self.setGeometry(QtCore.QRect(*geometry))

        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.setFont(font)
        self.setStyleSheet(self.get_help_style())

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        
        self.clicked.connect(self.command)

    def command(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.title)
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(self.txt)
        btn = msg_box.addButton("Close", QMessageBox.ButtonRole.RejectRole)
        btn.setStyleSheet(self.get_msgboxbtn_style())
        msg_box.exec()
    
    def update_theme(self, theme_name):
        if theme_name == "dark":
            self.setStyleSheet(self.get_help_style(dark=True))
        else:  # light
            self.setStyleSheet(self.get_help_style(dark=False))
    
    @staticmethod
    def get_help_style(dark=True):
        icon_path = help_icon_path if dark else help_icon_black_path
        return f"""
        QPushButton#DefaultAboutButton {{  /* Scoped to object name */
            border-radius: 25px;
            border: 2px solid #5D6D7E;
            padding: 10px;
            min-width: 16px;
            min-height: 16px;
            image: url({icon_path});
        }}
        QPushButton#DefaultAboutButton:hover {{
            background-color: grey;
        }}
        QPushButton#DefaultAboutButton:pressed {{
            background-color: #839192;
        }}
        QPushButton#DefaultAboutButton:checked {{
            background-color: #5D6D7E;
        }}
        """
    
    @staticmethod
    def get_msgboxbtn_style():
        return """
        QPushButton {
        border-radius: 15px;
        border: 2px solid #5D6D7E;
        padding: 0px;       
        width: 55px;        
        height: 40px;       
        min-width: 50px;    
        min-height: 30px;   
        max-width: 70px;    
        max-height: 50px;   
        }
        QPushButton:hover {
            background-color: grey;
        }
        QPushButton:pressed {
            background-color: #839192;
        }
        QPushButton:checked {
            background-color: #5D6D7E;
        }
        """
