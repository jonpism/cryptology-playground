from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from cryptography.fernet            import Fernet

class FernetEncryption:

    def __init__(self, key=None):
        self.key = key
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext: str) -> str:
        encrypted_data = self.cipher.encrypt(plaintext.encode())
        return encrypted_data.decode('utf-8')

    def get_key(self) -> str:
        """Returns the encryption key in base64 encoded form."""
        return self.key.decode('utf-8')

class FernetDecryption:

    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def decrypt(self, encrypted_data: str) -> bytes:
        decrypted_data = self.cipher.decrypt(encrypted_data.encode())
        return decrypted_data.decode('utf-8')

class FERNETWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Fernet Encryption - Decryption"
        msgbox_txt = (
        "<p>This application uses <b>Fernet</b> from the <i>cryptography</i> library.</p>"
        "<ul>"
        "<li><b>Encryption:</b> Enter plaintext and click Encrypt to generate an encrypted message and a key.</li>"
        "<li><b>Decryption:</b> Paste the encrypted message and key, then click Decrypt to recover the original plaintext.</li>"
        "</ul>"
        "<p><b>Note:</b> Fernet uses AES in CBC mode with HMAC for authentication.</p>")

        self.setWindowTitle("FERNET Encrypt - Decrypt")
        self.setFixedSize(1100, 500)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(225, 10, 120, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(20, 60, 480, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, bold=True, command=self.call_fernet_encryption)
        encrypt_button.setGeometry(225, 140, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(20, 210, 480, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.generated_key_label = QTextEdit(parent=self)
        self.generated_key_label.setGeometry(20, 330, 480, 100)
        self.generated_key_label.setReadOnly(True)
        self.generated_key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(1050, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        _label = QLabel(
            '|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n'
            '|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n', 
            parent=self)
        _label.setGeometry(550, 5, 20, 1000)

        # ciphertext
        ciphertext_label = QLabel("Paste ciphertext:", parent=self)
        ciphertext_label.setGeometry(780, 10, 120, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(600, 60, 480, 50)

        paste_key_label = QLabel("Paste key:", parent=self)
        paste_key_label.setGeometry(800, 130, 100, 50)
        self.paste_key_input = DefaultQLineEditStyle(parent=self)
        self.paste_key_input.setGeometry(600, 180, 480, 50)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, bold=True, command=self.call_fernet_decryption)
        decrypt_button.setGeometry(800, 260, 100, 50)

        self.original_msg_label = QTextEdit(parent=self)
        self.original_msg_label.setGeometry(600, 340, 480, 100)
        self.original_msg_label.setReadOnly(True)
        self.original_msg_label.hide()

    def fix_base64_padding(s: str) -> str:
        return s + '=' * (-len(s) % 4)

    def call_fernet_decryption(self):
        try:
            if self.ciphertext_input.text():
                if self.paste_key_input.text():
                    ciphertext_b64 = self.ciphertext_input.text()
                    key_b64 = self.paste_key_input.text()
                    
                    def fix_base64_padding(data: str) -> str:
                        return data + '=' * (-len(data) % 4)

                    key_b64 = fix_base64_padding(key_b64)
                    key_bytes = key_b64.encode('utf-8')

                    decryption = FernetDecryption(key_bytes)
                    plaintext = decryption.decrypt(ciphertext_b64)

                    self.original_msg_label.clear()
                    self.original_msg_label.setHtml(f"<b>Decrypted text:</b><br>{plaintext}")
                    self.original_msg_label.show()

                else:
                    raise ValueError('Please paste key.')
            else:
                raise ValueError('Please paste ciphertext.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def call_fernet_encryption(self):
        try:
            if self.plaintext_input.text():
                plaintext = self.plaintext_input.text()
                key_bytes = Fernet.generate_key()
                
                object = FernetEncryption(key_bytes)
                encrypted_text = object.encrypt(plaintext)

                self.encrypted_text_label.clear()
                self.encrypted_text_label.setHtml(f"<b>Encrypted text:</b><br>{encrypted_text}")
                self.encrypted_text_label.show()

                self.generated_key_label.clear()
                self.generated_key_label.setHtml(f"<b>Generated key:</b><br>{object.get_key()}")
                self.generated_key_label.show()
            else:
                raise ValueError('Please enter plaintext')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
