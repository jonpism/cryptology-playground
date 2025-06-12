from PyQt6.QtWidgets                import QLabel, QMessageBox, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from .file_conversion               import FileConversionWindow
import pyminizip, os, zipfile

class ZipWithPassword:
    def __init__(self, zip_filename: str):
        self.zip_filename = zip_filename
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.zip_filename = os.path.join(downloads_folder, zip_filename)

    def add_file(self, file_path: str, password: str, compression_level: int):
        """Adds a file to the zip with AES-256 encryption."""
        pyminizip.compress(file_path, None, self.zip_filename, password, compression_level)

    def extract_all(self, extract_to: str, password: str):
        """Extracts the zip file to the specified directory using the password."""
        with zipfile.ZipFile(self.zip_filename, 'r') as zipf:
            zipf.extractall(path=extract_to, pwd=password.encode())

class ZipFileWithPwdWindow(FileConversionWindow):
    
    def __init__(self, theme_mode):
        about_title = "About Zip files With Password"
        about_text = ("This tool zips files with AES encryption and a password.")
        
        ax, ay, aw, ah = 650, 250, 50, 50
        file_filter = "All files (*)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Zip Files with password")
        self.setFixedSize(700, 300)

        select_file_button = DefaultButtonStyle(
            'Select a file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(10, 60, 230, 50)

        pwd_input_label = QLabel("Enter password:", parent=self)
        pwd_input_label.setGeometry(350, 10, 150, 50)
        self.pwd_input = DefaultQLineEditStyle(parent=self)
        self.pwd_input.setEchoMode(self.pwd_input.EchoMode.Password)
        self.pwd_input.setGeometry(300, 60, 200, 50)

        submit_button = DefaultButtonStyle("Submit", bold=True, parent=self, command=self.zip_file)
        submit_button.setGeometry(550, 60, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 70)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def zip_file(self):
        try:
            if hasattr(self, 'selected_file'):
                if not self.pwd_input.text():
                    raise ValueError('No password entered. Please enter a password.')
                
                password = self.pwd_input.text()
                filename_only = os.path.basename(self.selected_file)
                zipper = ZipWithPassword(f"{filename_only}.zip")
                zipper.add_file(self.selected_file, password, compression_level=9)

                # Show a custom message box with a button to open the Downloads folder
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('Conversion Successful')
                msg_box.setText(f'File zipped and saved at: {self.downloads_path}')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                msg_box.exec()
                if msg_box.clickedButton() == open_folder_btn:
                    self.open_downloads_folder()
                
                self.output_label.clear()
                self.output_label.setHtml(f"<b>File successfully zipped with password and saved at:</b><br>{self.downloads_path}")
                self.output_label.show()

                # zipper.extract_all(self.downloads_path, password)
            else:
                raise ValueError('Please select a file first.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
