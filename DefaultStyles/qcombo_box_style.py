from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
import os

base_dir = os.path.dirname(os.path.dirname(__file__)) # projet root directory
# down arrow icon for dark mode
down_arrow_icon_path = os.path.join(base_dir, 'icons', 'down_arrow_icon.png').replace("\\", "/")
# down arrow icon for light mode
# ...

class DefaultQComboBoxStyle(QtWidgets.QComboBox):

    def __init__(self, parent=None, object_name=None, items=None, visible_items=None):
        super().__init__(parent)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setObjectName(object_name if object_name else "comboBox")
        self.setStyleSheet(self.get_style())
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.addItems(items)
        for i in range(self.count()):
            self.setItemData(i, Qt.AlignmentFlag.AlignCenter, Qt.ItemDataRole.TextAlignmentRole)
        if visible_items:
            self.setMaxVisibleItems(visible_items)

    def get_style(self):
        return f"""
            QComboBox {{
                border-radius: 15px;
                border: 2px solid #5D6D7E;
                padding: 5px;
                font-size: 12pt;
                text-align: center;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 1px;
                border-left-color: #5D6D7E;
                border-left-style: solid;
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
            }}
            QComboBox::down-arrow {{
                image: url({down_arrow_icon_path});
                width: 30px;
                height: 30px;
            }}
            QComboBox QAbstractItemView {{
                border-radius: 15x;
                border: 3px solid #5D6D7E;
            }}"""
