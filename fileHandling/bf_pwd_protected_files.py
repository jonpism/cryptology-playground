from PyQt6.QtWidgets                import QMessageBox, QFileDialog, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from .file_conversion               import FileConversionWindow
import os, time, zlib, pyzipper

class BfPwdProtectedFilesWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About Brute force password protected zip files"
        about_text = (
            "Brute force password protected zip files.")
        
        ax, ay, aw, ah = 650, 450, 50, 50
        file_filter = (
        "All Supported Archives (*.zip *.zipx *.z01 *.rar *.gz *.7z);;"
        "ZIP files (*.zip);;"
        "ZIPX files (*.zipx);;"
        "Split ZIP files (*.z01);;"
        "RAR files (*.rar);;"
        "GZip files (*.gz);;"
        "7-Zip files (*.7z);;")
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Brute force password protected zip files")
        self.setFixedSize(700, 500)

        self.wordlist_file = None

        select_file_button = DefaultButtonStyle(
            'Select a zip file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(30, 60, 190, 50)

        select_wordlist_button = DefaultButtonStyle(
            'Select wordlist file',
            parent=self,
            bold=True, command=self.select_wl_file)
        select_wordlist_button.setGeometry(250, 60, 190, 50)

        bf_button = DefaultButtonStyle("Brute Force", parent=self, bold=True, command=self.bf_file)
        bf_button.setGeometry(500, 60, 130, 50)

        self.selected_zipfile_label = QTextEdit(parent=self)
        self.selected_zipfile_label.setGeometry(30, 200, 300, 80)
        self.selected_zipfile_label.setReadOnly(True)
        self.selected_zipfile_label.hide()

        self.selected_wordlist_label = QTextEdit(parent=self)
        self.selected_wordlist_label.setGeometry(370, 200, 300, 80)
        self.selected_wordlist_label.setReadOnly(True)
        self.selected_wordlist_label.hide()

        self.pwd_found = QTextEdit(parent=self)
        self.pwd_found.setGeometry(10, 300, 680, 100)
        self.pwd_found.setReadOnly(True)
        self.pwd_found.hide()

    def select_wl_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select a file', '', 'txt files (*.txt)')
        if file_path:
            self.selected_wl_file = file_path
            QMessageBox.information(self, 'File Selected', f'Selected file: {file_path}')
        else:
            QMessageBox.critical(self, 'Unexpected Error', 'Something happened during wordlist selection.')

    def bf_file(self):
        try:
            if hasattr(self, 'selected_file'):
                if hasattr(self, 'selected_wl_file'):
                    file_extension = os.path.splitext(self.selected_file)[1].lower()
                    if file_extension in ['.zip', '.zipx', '.z01', 'zx01', '.rar', '.gz', '.7z']:
                        self.selected_zipfile_label.clear()
                        self.selected_zipfile_label.setHtml(f"<b>Selected zip file to brute force:</b><br>{self.selected_file} ")
                        self.selected_zipfile_label.show()

                        self.selected_wordlist_label.clear()
                        self.selected_wordlist_label.setHtml(f"<b>Selected wordlist file:</b><br>{self.selected_wl_file} ")
                        self.selected_wordlist_label.show()

                        if os.path.exists(self.selected_wl_file):
                            start_bf = time.time()
                            password = self.brute_force_zip(self.selected_file, self.selected_wl_file)
                            end_bf = time.time()
                            elapsed_time = end_bf - start_bf
                            if password:
                                msg_box = QMessageBox(self)
                                msg_box.setWindowTitle('Brute Force Successful')
                                msg_box.setText(f'File extracted at: {self.downloads_path}')
                                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                                open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                                msg_box.exec()
                                if msg_box.clickedButton() == open_folder_btn:
                                    self.open_downloads_folder()

                                QMessageBox.warning(self, 'Success', f"Password found: {str(password)}")
                                self.pwd_found.clear()
                                self.pwd_found.setHtml(
                                    f"<b>Password found:</b><br>{str(password)}<br>"
                                    f"Time needed: {elapsed_time:.2f} seconds")
                                self.pwd_found.show()
                            else:
                                QMessageBox.warning(self, 'Password Not Found', "No matching password was found in the wordlist.")
                                self.pwd_found.clear()
                                self.pwd_found.setHtml(
                                    f"<b>Password Not found</b><br>"
                                    f"Time passed: {elapsed_time:.2f} seconds")
                                self.pwd_found.show()
                        else:
                            QMessageBox.warning(self, 'No Wordlist Selected', 'Please select a wordlist file.')
                    else:
                        raise ValueError('Error: Select a zip password protected file.')
                else:
                    raise ValueError('Please select a wordlist file (like rockyou.txt)')
            else:
                raise ValueError('Error: No file selected. Please select a file first.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
        
    def brute_force_zip(self, zip_path, wordlist_path):
        """Attempts to brute-force the password for the zip file using the provided wordlist.
        Returns the password if found, else None."""
        try:
            with pyzipper.AESZipFile(zip_path, 'r') as zip_file:
                # Open the wordlist with a more lenient encoding
                with open(wordlist_path, 'r', encoding='ISO-8859-1', errors='ignore') as wordlist:
                    for line in wordlist:
                        password = line.strip()
                        self.pwd_found.clear()
                        self.pwd_found.setHtml(f"Trying password: {password}")
                        self.pwd_found.show()
                        try:
                            zip_file.extractall(path=self.downloads_path, pwd=password.encode("utf-8"))
                            return password  # Password found
                        except (RuntimeError, zlib.error, pyzipper.BadZipFile):
                            continue  # Ignore and try next password
            return None  # Password not found
        except FileNotFoundError:
            QMessageBox.warning(self, 'File Not Found', 'The selected zip file or wordlist file could not be found.')
        except pyzipper.BadZipFile as e:
            QMessageBox.warning(self, 'BadZipFile', f'{e}')
