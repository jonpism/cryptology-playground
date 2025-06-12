from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox, QFileDialog
from PyQt6                          import QtWidgets, QtCore, QtGui
from PyQt6.QtCore                   import QProcess, QObject, pyqtSignal
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from pathlib                        import Path
import os, pgpy, sys, warnings

class SettingsPageUI(QWidget):
    song_selected = pyqtSignal(str)
    theme_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_settings_ui()

    def setup_settings_ui(self):
        """Set up the settings page, label, and content."""
        self.SettingsPage = QtWidgets.QWidget(parent=self.parent)
        self.SettingsPage.setObjectName("SettingsPage")

        self.SettingsLabel = QtWidgets.QLabel(parent=self.SettingsPage)
        self.SettingsLabel.setGeometry(QtCore.QRect(10, -1, 1041, 51))
        self.SettingsLabel.setText("Settings")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.SettingsLabel.setFont(font)
        self.SettingsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SettingsLabel.setObjectName("SettingsLabel")

        # select song
        select_song_button = DefaultButtonStyle('Select song', parent=self.SettingsPage, bold=True, command=self.select_song)
        select_song_button.setGeometry(30, 130, 180, 50)
        self.selected_song_label = QTextEdit(parent=self.SettingsPage)
        self.selected_song_label.setGeometry(10, 190, 220, 90)
        self.selected_song_label.setReadOnly(True)
        self.selected_song_label.show()

        # dark or light mode selection
        theme_label = QtWidgets.QLabel("Select Theme:", parent=self.SettingsPage)
        theme_label.setGeometry(350, 130, 100, 30)
        self.theme_combo = DefaultQComboBoxStyle(parent=self.SettingsPage, items=["dark", "light"])
        self.theme_combo.setGeometry(460, 130, 150, 30)
        self.theme_combo.currentTextChanged.connect(self.change_theme)
    
    def change_theme(self, theme_name):
        self.theme_changed.emit(theme_name.lower())
    
    def select_song(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
            self.SettingsPage,
            "Select a song",
            str(Path.home() / "Music"),
            "Audio Files (*.mp3 *.wav *.flac);;All Files (*)")
            if file_path:
                self.selected_song = file_path
                self.selected_song_label.setHtml(f"<b>Selected song:</b><br>{self.selected_song}")
                self.selected_song_label.show()
                self.song_selected.emit(file_path)
        except ValueError as ve:
            QMessageBox.warning(self.SettingsPage, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self.SettingsPage, 'Unexpected Error', str(e))