from PyQt6.QtWidgets                import QWidget, QTextEdit, QMessageBox, QFileDialog
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from pathlib                        import Path
from PyQt6.QtCore                   import QProcess
import os, pgpy, sys, warnings

class PGPEncryptWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About PGP Encryptor Tool"
        msgbox_txt = """<p>The <b>PGP Encryptor Tool</b> is a lightweight desktop utility that allows users to securely encrypt files using the 
        recipient's <b>PGP public key</b>. It provides a simple graphical interface for selecting files and keys, 
        and performs fast encryption using the OpenPGP standard.
        </p>

        <h3>Key Features:</h3>
        <ul>
          <li><b>File Selection:</b> Choose any file on your system to encrypt.</li>
          <li><b>Public Key Loading:</b> Import a recipient's public key (.asc) for secure encryption.</li>
          <li><b>Encryption:</b> Encrypt your file using strong OpenPGP encryption.</li>
          <li><b>Download Location:</b> Encrypted files are automatically saved to your <b>Downloads</b> folder.</li>
          <li><b>Cross-Platform:</b> Works on Windows, macOS, and Linux.</li>
        </ul>

        <h3>Security Notice:</h3>
        <p>
        This tool only performs <b>encryption</b> — make sure the recipient owns the matching <b>private key</b> 
        to decrypt the file. Your original file remains unchanged, and the encrypted output is stored separately.
        </p>

        <h3>Note:</h3>
        <p>
        Supports PGP public keys in ASCII-armored format (.asc). Make sure to verify the recipient's key 
        authenticity before use.
        </p>"""

        self.setWindowTitle("PGP Encryptor")
        self.setFixedSize(700, 600)

        self.downloads_path = str(Path.home() / "Downloads")

        select_file_button = DefaultButtonStyle(
            'Select File for Encryption',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(50, 30, 230, 50)

        load_pbl_key_button = DefaultButtonStyle(
            'Load Receiver`s Public Key for Encryption',
            parent=self,
            bold=True, command=self.load_pbl_key)
        load_pbl_key_button.setGeometry(340, 30, 320, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.encrypt_file, bold=True)
        encrypt_button.setGeometry(300, 120, 100, 50)

        self.selected_file_label = QTextEdit(parent=self)
        self.selected_file_label.setGeometry(10, 190, 680, 100)
        self.selected_file_label.setReadOnly(True)
        self.selected_file_label.hide()

        self.selected_pbl_key_label = QTextEdit(parent=self)
        self.selected_pbl_key_label.setGeometry(10, 300, 680, 100)
        self.selected_pbl_key_label.setReadOnly(True)
        self.selected_pbl_key_label.hide()

        self.encrypted_file_label = QTextEdit(parent=self)
        self.encrypted_file_label.setGeometry(10, 420, 680, 100)
        self.encrypted_file_label.setReadOnly(True)
        self.encrypted_file_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def load_pbl_key(self):
        file_dialog = QFileDialog()
        pbl_key_file_path, _ = file_dialog.getOpenFileName(self, 'Load Public Key', filter="Key files (*.asc)")
        try:
            if pbl_key_file_path:
                self.pbl_key_file = pbl_key_file_path
                QMessageBox.information(self, 'Public Key Selected', f'Selected Public key: {pbl_key_file_path}')
                self.selected_pbl_key_label.clear()
                self.selected_pbl_key_label.setHtml(f"<b>Current loaded public key:</b><br>{str(pbl_key_file_path)}")
                self.selected_pbl_key_label.show()
        except Exception as e:
            QMessageBox.critical(self, 'An error occured', f'An error occured while loading public key: {str(e)}')

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select a file to encrypt')
        try:
            if file_path:
                self.selected_file = file_path
                QMessageBox.information(self, 'File Selected', f'Selected file: {file_path}')
                self.selected_file_label.clear()
                self.selected_file_label.setHtml(f"<b>Current selected file:</b><br>{str(file_path)}")
                self.selected_file_label.show()
        except Exception as e:
            QMessageBox.critical(self, 'An error occured', f'An error occured while selecting file: {str(e)}')

    def encrypt_file(self):
        try:
            if hasattr(self, 'selected_file'):
                if hasattr(self, 'pbl_key_file'):
                    file_name = os.path.basename(self.selected_file)
                    encrypted_file_path = os.path.join(self.downloads_path, f'{file_name}.enc')

                    try:
                        warnings.filterwarnings("ignore", category=UserWarning)
                        warnings.filterwarnings("ignore", category=DeprecationWarning)

                        # Load public key
                        with open(self.pbl_key_file, 'r') as key_file:
                            key_data = key_file.read()
                            public_key, _ = pgpy.PGPKey.from_blob(key_data)

                        # Read and encrypt file
                        with open(self.selected_file, 'rb') as file:
                            file_data = file.read()
                            data = pgpy.PGPMessage.new(file_data, file=True)
                            encrypted_data = public_key.encrypt(data)

                        with open(encrypted_file_path, 'w') as encrypted_file:
                            encrypted_file.write(str(encrypted_data))

                        # Show a custom message box with a button to open the Downloads folder
                        msg_box = QMessageBox(self)
                        msg_box.setWindowTitle('Encryption Successful')
                        msg_box.setText(f'File encrypted and saved at: {encrypted_file_path}')
                        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

                        # Add a custom button for opening the Downloads folder
                        open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                        msg_box.exec()

                        # If the user clicks "Open Downloads", open the Downloads folder
                        if msg_box.clickedButton() == open_folder_btn:
                            self.open_downloads_folder()

                        self.encrypted_file_label.clear()
                        self.encrypted_file_label.setHtml(f'<b>File Successfully encrypted and saved at:</b><br> {str(encrypted_file_path)}')
                        self.encrypted_file_label.show()

                    except Exception as e:
                        QMessageBox.critical(self, 'An error occured', f'An error occured during encryption: {str(e)}')
                else:
                    raise ValueError('Please load a public key first.')
            else:
                raise ValueError('Please select a file first.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def open_downloads_folder(self):
        # Open the Downloads folder using the appropriate command for the OS
        if sys.platform == 'win32':
            os.startfile(self.downloads_path)
        elif sys.platform == 'darwin':  # macOS
            QProcess.execute('open', [self.downloads_path])
        else:  # Linux and other Unix-like systems
            QProcess.execute('xdg-open', [self.downloads_path])
