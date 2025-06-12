from PyQt6.QtWidgets                import QWidget, QTextEdit, QMessageBox, QFileDialog, QLineEdit, QInputDialog
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from pathlib                        import Path
from PyQt6.QtCore                   import QProcess
import os, pgpy, sys, warnings

class PGPDecryptWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode
        
        msgbox_title = "About PGP Decryptor Tool"
        msgbox_txt = """<p>
        The <b>PGP Decryptor Tool</b> is a secure and user-friendly utility designed to <b>decrypt files</b> that were previously encrypted using a PGP public key. 
        It requires the matching <b>PGP private key</b> and passphrase (if protected) to decrypt the contents successfully.
        </p>

        <h3>Key Features:</h3>
        <ul>
          <li><b>Encrypted File Selection:</b> Easily choose any PGP-encrypted file (.enc) from your system.</li>
          <li><b>Private Key Loading:</b> Load your personal private key (.asc format) securely.</li>
          <li><b>Passphrase Support:</b> Decrypts keys protected by a passphrase via a secure input prompt.</li>
          <li><b>Decryption:</b> Extracts and saves the decrypted content into your <b>Downloads</b> folder.</li>
          <li><b>Cross-Platform:</b> Compatible with Windows, macOS, and Linux systems.</li>
        </ul>

        <h3>Security Notice:</h3>
        <p>
        This tool assumes that you are the legitimate owner of the private key being used. For your safety, 
        make sure to <b>never share your private key or passphrase</b> with untrusted sources.
        </p>

        <h3>Note:</h3>
        <p>
        Decrypted data is saved as a binary file. If the original file was text-based, it may need to be opened with a suitable text editor. 
        Private keys must be in valid <b>ASCII-armored (.asc)</b> format for compatibility.
        </p>"""

        self.setWindowTitle("PGP Decryptor")
        self.setFixedSize(700, 600)

        self.downloads_path = str(Path.home() / "Downloads")

        select_file_button = DefaultButtonStyle(
            'Select Encrypted file for Decryption',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(30, 30, 280, 50)

        load_prv_key_button = DefaultButtonStyle(
            'Load Receiver`s Private Key for Decryption',
            parent=self,
            bold=True, command=self.load_prv_key)
        load_prv_key_button.setGeometry(340, 30, 330, 50)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, command=self.decrypt_file, bold=True)
        decrypt_button.setGeometry(300, 120, 100, 50)

        self.selected_file_label = QTextEdit(parent=self)
        self.selected_file_label.setGeometry(10, 190, 680, 100)
        self.selected_file_label.setReadOnly(True)
        self.selected_file_label.hide()

        self.selected_prv_key_label = QTextEdit(parent=self)
        self.selected_prv_key_label.setGeometry(10, 300, 680, 100)
        self.selected_prv_key_label.setReadOnly(True)
        self.selected_prv_key_label.hide()

        self.decrypted_file_label = QTextEdit(parent=self)
        self.decrypted_file_label.setGeometry(10, 420, 680, 100)
        self.decrypted_file_label.setReadOnly(True)
        self.decrypted_file_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select an Encrypted file', filter="Encrypted files (*.enc)")
        try:
            if file_path:
                self.selected_file = file_path
                QMessageBox.information(self, 'File Selected', f'Selected file: {file_path}')
                self.selected_file_label.clear()
                self.selected_file_label.setHtml(f"<b>Current selected file:</b><br>{str(file_path)}")
                self.selected_file_label.show()
        except Exception as e:
            QMessageBox.critical(self, 'An error occured', f'An error occured while selecting file: {str(e)}')

    def load_prv_key(self):
        file_dialog = QFileDialog()
        prv_key_file_path, _ = file_dialog.getOpenFileName(self, 'Load Receiver`s Private Key', filter="Key files (*.asc)")
        try:
            if prv_key_file_path:
                self.prv_key_file = prv_key_file_path
                QMessageBox.information(self, 'Private Key Selected', f'Selected Private key: {prv_key_file_path}')
                self.selected_prv_key_label.clear()
                self.selected_prv_key_label.setHtml(f"<b>Current loaded receiver`s private key:</b><br>{str(prv_key_file_path)}")
                self.selected_prv_key_label.show()
        except Exception as e:
            QMessageBox.critical(self, 'An error occured', f'An error occured while loading private key: {str(e)}')

    def decrypt_file(self):
        if hasattr(self, 'selected_file'):
            if hasattr(self, 'prv_key_file'):
                file_name = os.path.basename(self.selected_file)
                decrypted_file_path = os.path.join(self.downloads_path, f'{file_name}.dec')

                try:
                    warnings.filterwarnings("ignore", category=UserWarning)
                    warnings.filterwarnings("ignore", category=DeprecationWarning)

                    # Load private key
                    with open(self.prv_key_file, 'rb') as key_file:
                        key_data = key_file.read()
                        private_key, _ = pgpy.PGPKey.from_blob(key_data)

                    # Unlock private key if needed
                    if private_key.is_protected:
                        passphrase, ok = QInputDialog.getText(
                            self, "Enter Passphrase", "Private Key Passphrase:",
                            echo=QLineEdit.EchoMode.Password)
                        if not ok:
                            return  # User canceled
                        try:
                            private_key.unlock(passphrase)
                        except Exception as e:
                            QMessageBox.critical(self, "Decryption Failed", f"Failed to unlock private key: {str(e)}")
                            return

                    # Read and decrypt the encrypted file
                    with open(self.selected_file, 'rb') as file:
                        file_data = file.read()

                    try:
                        encrypted_message = pgpy.PGPMessage.from_blob(file_data)
                    except Exception as e:
                        QMessageBox.critical(self, "Invalid PGP File", f"Failed to read PGP message: {str(e)}")
                        return

                    try:
                        decrypted_msg = private_key.decrypt(encrypted_message)
                        decrypted_data = decrypted_msg.message

                        # Convert to bytes if it's a string
                        if isinstance(decrypted_data, str):
                            decrypted_data = decrypted_data.encode('utf-8')

                    except Exception as e:
                        QMessageBox.critical(self, "Decryption Error", f"Failed to decrypt message: {str(e)}")
                        return

                    if not decrypted_data.strip():
                        QMessageBox.warning(self, "Decryption Warning", "The decrypted content is empty.")
                        return

                    with open(decrypted_file_path, 'wb') as decrypted_file:
                        decrypted_file.write(decrypted_data)

                    # Show a message box with option to open Downloads folder
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Decryption Successful')
                    msg_box.setText(f'File decrypted and saved at:\n{decrypted_file_path}')
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                    msg_box.exec()

                    if msg_box.clickedButton() == open_folder_btn:
                        self.open_downloads_folder()

                    self.decrypted_file_label.clear()
                    self.decrypted_file_label.setHtml(f'<b>File successfully decrypted and saved at:</b><br>{decrypted_file_path}')
                    self.decrypted_file_label.show()

                except Exception as e:
                    QMessageBox.critical(self, 'An error occurred', f'An error occurred during decryption:\n{str(e)}')
            else:
                QMessageBox.warning(self, 'No Private Key Selected', 'Please load a private key first.')
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select an encrypted file first.')

    def open_downloads_folder(self):
        # Open the Downloads folder using the appropriate command for the OS
        if sys.platform == 'win32':
            os.startfile(self.downloads_path)
        elif sys.platform == 'darwin':  # macOS
            QProcess.execute('open', [self.downloads_path])
        else:  # Linux and other Unix-like systems
            QProcess.execute('xdg-open', [self.downloads_path])
