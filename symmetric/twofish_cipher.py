from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from twofish                        import Twofish
from os                             import urandom
from base64                         import b64encode, b64decode

class TwofishEncryption:

    def __init__(self, key: bytes, plaintext: str):
        """Initialize the Twofish cipher with a key."""
        
        self.key = key
        self.block_size = 16  # Twofish block size is 16 bytes
        self.cipher = Twofish(key)
        self.ciphertext = self.encrypt(plaintext)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypt the plaintext using the Twofish cipher."""
        data = plaintext.encode('utf-8')

        # Pad using PKCS#7 to make data length a multiple of 16
        padding_len = self.block_size - (len(data) % self.block_size)
        padded_data = data + bytes([padding_len] * padding_len)

        ciphertext = b''
        for i in range(0, len(padded_data), self.block_size):
            block = padded_data[i:i + self.block_size]
            ciphertext += self.cipher.encrypt(block)

        return ciphertext

class TwofishDecryption:

    def __init__(self, key: bytes, ciphertext: bytes):
        self.key = key
        self.cipher = Twofish(key)
        self.block_size = 16
        self.plaintext = None
        try:
            self.plaintext = self.decrypt(ciphertext)
        except:
            pass # decrypt other modes

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypt ciphertext and remove PKCS#7 padding."""
        decrypted_data = b''
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            decrypted_data += self.cipher.decrypt(block)

        # Remove PKCS#7 padding
        padding_len = decrypted_data[-1]
        return decrypted_data[:-padding_len].decode('utf-8')

class TwofishWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Twofish symmetric key block cipher"
        msgbox_txt = """This application demonstrates the use of the <b>Twofish symmetric block cipher 
        algorithm</b> for secure encryption and decryption of text.<br><br>

        <b>Encryption:</b><br>
        &bull; Enter plaintext and choose a key length (16, 24, or 32 bytes).<br>
        &bull; A random key is generated and used to encrypt the message.<br>
        &bull; The output ciphertext is shown in Base64 format along with the encryption key.<br><br>

        <b>Decryption:</b><br>
        &bull; Paste a previously generated Base64 ciphertext and the corresponding key.<br>
        &bull; The tool will decrypt and display the original message.<br><br>

        <b>Security:</b><br>
        Twofish is a fast and secure block cipher with a block size of 128 bits and support for keys up to 256 bits. 
        It was one of the finalists in the AES competition.<br><br>

        <b>Important:</b><br>
        Always store your encryption key securely. If the key is lost, the encrypted data cannot be recovered."""

        self.setWindowTitle("Twofish symmetric key block cipher")
        self.setFixedSize(1100, 550)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(200, 10, 120, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 480, 50)

        # Key
        key_label = QLabel("Choose key length:", parent=self)
        key_label.setGeometry(50, 110, 300, 50)
        self.key_input = DefaultQComboBoxStyle(
            parent=self, items=["16", "24", "32"])
        self.key_input.setGeometry(60, 160, 80, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, bold=True, command=self.call_twofish_encryption)
        encrypt_button.setGeometry(300, 160, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 250, 480, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.generated_key_label = QTextEdit(parent=self)
        self.generated_key_label.setGeometry(10, 400, 480, 50)
        self.generated_key_label.setReadOnly(True)
        self.generated_key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(1050, 500, 50, 50))
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

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, bold=True, command=self.call_twofish_decryption)
        decrypt_button.setGeometry(800, 260, 100, 50)

        self.original_msg_label = QTextEdit(parent=self)
        self.original_msg_label.setGeometry(600, 340, 480, 100)
        self.original_msg_label.setReadOnly(True)
        self.original_msg_label.hide()
    
    def call_twofish_decryption(self):
        try:
            if self.ciphertext_input.text():
                if self.paste_key_input.text():
                    ciphertext_b64 = self.ciphertext_input.text()
                    key_b64 = self.paste_key_input.text()
                    key = b64decode(key_b64)
                    ciphertext = b64decode(ciphertext_b64)

                    twofish_decryption = TwofishDecryption(key, ciphertext)
                    plaintext = twofish_decryption.plaintext

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
    
    def call_twofish_encryption(self):
        try:
            if self.plaintext_input.text():
                plaintext = self.plaintext_input.text()
                key_length = int(self.key_input.currentText())
                key_bytes = urandom(key_length)

                towfish_encryption = TwofishEncryption(key_bytes, plaintext)
                ciphertext = towfish_encryption.ciphertext

                self.encrypted_text_label.clear()
                self.encrypted_text_label.setHtml(f"<b>Ciphertext (Base64):</b><br>{b64encode(ciphertext).decode()}")
                self.encrypted_text_label.show()

                self.generated_key_label.clear()
                self.generated_key_label.setHtml(f"<b>Generated key of {key_length} bytes (Base64):</b><br>{b64encode(key_bytes).decode()}")
                self.generated_key_label.show()

            else:
                raise ValueError('Please enter plaintext.')    
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
