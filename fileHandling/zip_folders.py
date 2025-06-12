from PyQt6.QtWidgets                import QWidget, QLabel, QMessageBox, QFileDialog, QTextEdit
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle
from .file_conversion               import FileConversionWindow
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from datetime                       import datetime
import pyminizip, os, zipfile

class ZipWithPassword:
    def __init__(self, zip_filename: str):
        # Store the zip file in the Downloads folder
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.zip_filename = os.path.join(downloads_folder, zip_filename)

    def add_folder(self, folder_path: str, password: str, compression_level: int = 5):
        files = []
        relative_paths = []
        for root, _, filenames in os.walk(folder_path):
            for file in filenames:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=os.path.dirname(folder_path))
                files.append(file_path)
                relative_paths.append(arcname)
        pyminizip.compress_multiple(files, relative_paths, self.zip_filename, password, compression_level)

class ZipFolderWithPwdWindow(FileConversionWindow):
    
    def __init__(self, theme_mode):
        about_title = "About Folders files With Password"
        about_text = ("<p>This tool zips folders with AES encryption and a password.</p>"
        "<ul>"
            "<li><b>Folder Selection:</b> Users can select a folder to be zipped through a file selection dialog.</li>"
            "<li><b>Password Protection:</b> The tool applies a user-provided password to secure the ZIP file using AES-256 encryption.</li>"
            "<li><b>File Storage:</b> The ZIP file is saved directly in the Downloads folder for easy access.</li>"
        "</ul>")
        
        ax, ay, aw, ah = 650, 250, 50, 50
        file_filter = "All folders (*)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Zip Folders with password")
        self.setFixedSize(700, 300)

        select_folder_button = DefaultButtonStyle(
            'Select a folder',
            parent=self,
            bold=True, command=self.select_folder)
        select_folder_button.setGeometry(10, 60, 230, 50)

        pwd_input_label = QLabel("Enter password:", parent=self)
        pwd_input_label.setGeometry(350, 10, 150, 50)
        self.pwd_input = DefaultQLineEditStyle(parent=self)
        self.pwd_input.setEchoMode(self.pwd_input.EchoMode.Password)
        self.pwd_input.setGeometry(300, 60, 200, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.zip_folder)
        submit_button.setGeometry(550, 60, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 70)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def select_folder(self):
        """Opens a dialog to select a folder and stores the path."""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.selected_folder = folder_path
            QMessageBox.information(self, "Folder Selected!", f"Selected folder: {folder_path}")

    def zip_folder(self):
        """Zips the selected folder with the given password."""
        if hasattr(self, 'selected_folder'):
            if not self.selected_folder:
                QMessageBox.warning(self, "Error", "No folder selected. Please select a folder first.")

            password = self.pwd_input.text()
            if not password:
                QMessageBox.warning(self, "No password entered", "Please enter a password.")

            try:
                # Save zip file in Downloads as "zipped_folder.zip"
                zip_filename = f"zipped_folder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                zip_util = ZipWithPassword(zip_filename)
                zip_util.add_folder(self.selected_folder, password)
                QMessageBox.information(
                    self,
                    "Success",
                    f"Folder zipped successfully and saved in Downloads folder as {zip_util.zip_filename}")
                
                self.output_label.clear()
                self.output_label.setHtml(f"<b>Folder successfully zipped with password and saved at:</b><br>{zip_util.zip_filename}")
                self.output_label.show()

            except Exception as e:
                QMessageBox.critical(self, "Unexpected Error", f"An error occurred: {str(e)}")
        else:
            QMessageBox.warning(self, 'No folder selected', 'Please select a folder')
