from PyQt6.QtWidgets                import QWidget, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle
from DefaultStyles.qtextedit_style  import DefaultQTextEditStyle
from .file_conversion                import FileConversionWindow
from cryptography.fernet            import Fernet
import os

class FernetFileEncWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About Fernet File Encryption Tool"
        about_text = ("Fernet is a high-level cryptography mechanism in Python, "
        "provided by the cryptography package. It is used for "
        "symmetric encryption, meaning the same key is used for "
        "both encryption and decryption. The main purpose of Fernet "
        "is to make it easy to securely encrypt and decrypt data "
        "using modern cryptographic techniques, and it's well-suited "
        "for encrypting files in a straightforward manner. Fernet uses "
        "AES (Advanced Encryption Standard) in CBC (Cipher Block Chaining) "
        "mode with a 128-bit key. AES is a widely adopted and secure block cipher. "
        "Fernet also includes HMAC (Hash-based Message Authentication Code) "
        "to ensure the integrity of the encrypted data. It uses SHA256 for hashing "
        "to verify that the data has not been tampered with. <br><br>"
        "Useful links: <br>"
        "<a href=https://cryptography.io/en/latest/fernet>Cryptography.io</a><br>"
        "<a href=https://www.geeksforgeeks.org/fernet-symmetric-encryption-using-cryptography-module-in-python>Geeks for Geeks</a>")

        ax, ay, aw, ah = 650, 450, 50, 50
        file_filter = "All files (*)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Encrypt files with Fernet")
        self.setFixedSize(700, 500)

        select_file_button = DefaultButtonStyle(
            'Select File for Encryption',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, bold=True, command=self.encrypt_file)
        encrypt_button.setGeometry(450, 50, 100, 50)

        self.selected_file_label = DefaultQTextEditStyle(parent=self)
        self.selected_file_label.setGeometry(150, 180, 350, 100)
        self.set_selected_file_label(selected_file=None)

        self.encrypted_path_label = DefaultQTextEditStyle(parent=self)
        self.encrypted_path_label.setGeometry(150, 300, 400, 160)
        self.set_encrypted_path_label(encrypted_file=None, encryption_key=None)
    
    def set_selected_file_label(self, selected_file):
        self.selected_file_label.setHtml(f"<b>Current selected file:</b><br><br>{selected_file}")

    def set_encrypted_path_label(self, encrypted_file, encryption_key):
        self.encrypted_path_label.setHtml(
            f"<b>Encrypted file location: </b><br>{encrypted_file} <br><br><br><b>Encryption key location:</b><br>{encryption_key}")

    def encrypt_file(self):
        try:
            if hasattr(self, 'selected_file'):
                self.set_selected_file_label(selected_file=self.selected_file)
                key = Fernet.generate_key()
                cipher = Fernet(key)
                key_file_path = os.path.join(self.downloads_path, 'encryption_key.key')
                with open(key_file_path, 'wb') as key_file:
                    key_file.write(key)

                file_name = os.path.basename(self.selected_file)
                encrypted_file_path = os.path.join(self.downloads_path, f'{file_name}.encrypted')

                with open(self.selected_file, 'rb') as file:
                    file_data = file.read()
                encrypted_data = cipher.encrypt(file_data)

                # Write the encrypted data to the specified path
                with open(encrypted_file_path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_data)

                # custom message box with a button to open the Downloads folder
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('Encryption Successful')
                msg_box.setText(
                    f'Encrypted file saved at:\n {encrypted_file_path}\n\n Encryption key saved at:\n {key_file_path}')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                msg_box.exec()
                self.set_encrypted_path_label(encrypted_file=encrypted_file_path, encryption_key=key_file_path)

                if msg_box.clickedButton() == open_folder_btn:
                    self.open_downloads_folder()
            else:
                raise ValueError('Please select a file first.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

# ===================================================================================================================================

class FernetFileDecWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About Fernet File Encryption Tool"
        about_text = ("Fernet is a high-level cryptography mechanism in Python, "
        "provided by the cryptography package. It is used for "
        "symmetric encryption, meaning the same key is used for "
        "both encryption and decryption. The main purpose of Fernet "
        "is to make it easy to securely encrypt and decrypt data "
        "using modern cryptographic techniques, and it's well-suited "
        "for encrypting files in a straightforward manner. Fernet uses "
        "AES (Advanced Encryption Standard) in CBC (Cipher Block Chaining) "
        "mode with a 128-bit key. AES is a widely adopted and secure block cipher. "
        "Fernet also includes HMAC (Hash-based Message Authentication Code) "
        "to ensure the integrity of the encrypted data. It uses SHA256 for hashing "
        "to verify that the data has not been tampered with. <br><br>"
        "Useful links: <br>"
        "<a href=https://cryptography.io/en/latest/fernet>Cryptography.io</a><br>"
        "<a href=https://www.geeksforgeeks.org/fernet-symmetric-encryption-using-cryptography-module-in-python>Geeks for Geeks</a>")

        ax, ay, aw, ah = 550, 450, 50, 50
        file_filter = "Encryption files (*.encrypted *.key)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Decrypt files with Fernet")
        self.setFixedSize(600, 500)

        select_encrypted_file_button = DefaultButtonStyle(
            'Select Encrypted File', parent=self, bold=True, command=self.select_file)
        select_encrypted_file_button.setGeometry(20, 60, 180, 50)

        select_key_button = DefaultButtonStyle(
            'Select Key File', parent=self, bold=True, command=self.select_file)
        select_key_button.setGeometry(215, 60, 150, 50)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, bold=True, command=self.decrypt_file)
        decrypt_button.setGeometry(420, 60, 100, 50)

        self.selected_file_label = DefaultQTextEditStyle(parent=self)
        self.selected_file_label.setGeometry(20, 150, 470, 100)
        self.set_selected_file_label(selected_file=None)

        self.selected_key_label = DefaultQTextEditStyle(parent=self)
        self.selected_key_label.setGeometry(20, 270, 470, 100)
        self.set_selected_key_label(selected_encryption_key=None)

        self.decrypted_path_label = DefaultQTextEditStyle(parent=self)
        self.decrypted_path_label.setGeometry(20, 390, 470, 100)
        self.set_decrypted_path_label(decrypted_file=None)

    def set_selected_file_label(self, selected_file):
        self.selected_file_label.setHtml(f"<b>Current selected encrypted file:</b><br>{selected_file}")

    def set_selected_key_label(self, selected_encryption_key):
        self.selected_key_label.setHtml(f"<b>Current selected encryption key:</b><br>{selected_encryption_key}")

    def set_decrypted_path_label(self, decrypted_file):
        self.decrypted_path_label.setHtml(f"<b>Decrypted file location: </b><br>{decrypted_file}")  
    
    def decrypt_file(self):
        try:
            if not hasattr(self, 'selected_file_path'):
                raise ValueError('Please select an encrypted file first.')
            if not hasattr(self, 'selected_key_file_path'):
                raise ValueError('Please select the encryption key file first.')

            self.set_selected_file_label(selected_file=self.selected_file)
            self.set_selected_key_label(selected_encryption_key=self.selected_key_file_path)

            # Read the encryption key
            with open(self.selected_key_file_path, 'rb') as key_file:
                key = key_file.read()
            cipher = Fernet(key)

            # Read the encrypted file
            with open(self.selected_file_path, 'rb') as encrypted_file:
                encrypted_data = encrypted_file.read()

            # Decrypt the data
            decrypted_data = cipher.decrypt(encrypted_data)

            # Save the decrypted file
            original_file_name = os.path.basename(self.selected_file_path).replace('.encrypted', '')
            decrypted_file_path = os.path.join(self.downloads_path, f'decrypted_{original_file_name}')

            with open(decrypted_file_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Decryption Successful')
            msg_box.setText(f'File decrypted and saved at: {decrypted_file_path}')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
            msg_box.exec()
            
            self.set_decrypted_path_label(decrypted_file=decrypted_file_path)
            if msg_box.clickedButton() == open_folder_btn:
                self.open_downloads_folder()
            
            self.set_decrypted_path_label(decrypted_file=decrypted_file_path)

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error: Decryption failed', str(e))