from PyQt6.QtWidgets            import QWidget, QFileDialog, QMessageBox
from PyQt6.QtCore               import QProcess, Qt
from pathlib                    import Path
import os, sys

class FileConversionWindow(QWidget):
    """Base class for file conversion windows"""

    def __init__(self, about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode):
        super().__init__()
        self.downloads_path = str(Path.home() / "Downloads")

        self.about_title = about_title
        self.about_text = about_text
        self.file_filter = file_filter
        self.theme_mode = theme_mode

        self.setup_about_button(ax, ay, aw, ah)

    def select_file(self):
        """Opens a file dialog for the user to select a file."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select a file', '', self.file_filter)
        if file_path:
            if file_path.endswith('.encrypted'):
                self.selected_file_path = file_path
                self.selected_file = os.path.basename(file_path)
                QMessageBox.information(self, 'Encrypted File Selected', f'Selected file: {file_path}')
            elif file_path.endswith('.key'):
                self.selected_key_file_path = file_path
                QMessageBox.information(self, 'Encryption key Selected', f'Selected file: {file_path}')
            else:
                self.selected_file = file_path
                QMessageBox.information(self, 'File Selected', f'Selected file: {file_path}')

    def open_downloads_folder(self):
        """Opens the Downloads folder using the appropriate command for the OS."""
        if sys.platform == 'win32':
            os.startfile(self.downloads_path)
        elif sys.platform == 'darwin':  # macOS
            QProcess.execute('open', [self.downloads_path])
        else:  # Linux and other Unix-like systems
            QProcess.execute('xdg-open', [self.downloads_path])

    def setup_about_button(self, ax, ay, aw, ah):
        """Sets up the About button with custom geometry."""
        from DefaultStyles.button_style import DefaultAboutButtonStyle # avoid circular imports
        self.aboutButton = DefaultAboutButtonStyle(
            "", parent=self, title=self.about_title, txt=self.about_text, geometry=(ax, ay, aw, ah))
        self.aboutButton.update_theme(self.theme_mode)
