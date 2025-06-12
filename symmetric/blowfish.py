from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from base64                         import b64encode, b64decode
from Crypto.Cipher                  import Blowfish
from Crypto.Util.Padding            import pad, unpad
from os                             import urandom

# Implementation
class BlowfishImp:

    def __init__(self, key: bytes):
        """Initializes the Blowfish cipher with a key and mode.
        The key length should be between 4 and 56 bytes."""
        self.key = key
        self.block_size = Blowfish.block_size # 8 bytes

    def encrypt_ECB(self, plaintext: str) -> bytes:
        blowfish_encryption = Blowfish.new(self.key, Blowfish.MODE_ECB)
        plaintext = plaintext.encode('utf-8')
        padded = pad(plaintext, self.block_size)
        ciphertext = blowfish_encryption.encrypt(padded)
        return ciphertext

    def decrypt_ECB(self, ciphertext: bytes) -> str:
        cipher = Blowfish.new(self.key, Blowfish.MODE_ECB)
        decrypted_padded = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_padded, self.block_size)
        return plaintext

# Encryption and Decryption Windo
class BlowfishWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Blowfish"
        msgbox_txt = """
        This tool implements the Blowfish block cipher, which is a symmetric-key encryption algorithm designed by Bruce Schneier. It is known for its simplicity and speed, and can be used to securely encrypt and decrypt data using a secret key.<br><br>
        <b>Key Features:</b>
        <ul>
            <li>Supports encryption modes (for now): ECB(not secure).</li>
            <li>Allows you to specify a custom key (between 4 and 56 bytes) for encryption and decryption.</li>
            <li>Supports encryption of plaintext and decryption of ciphertext.</li>
        </ul>
        <b>Instructions:</b><br>
        1. Enter the plaintext you wish to encrypt in the <b>Plaintext</b> field.<br>
        2. Choose a <b>key length</b> for encryption (it must be between 4 and 56 bytes long).<br>
        3. Click <b>Encrypt</b> to encrypt the plaintext using the Blowfish cipher.<br><br>
        <b>Important:</b><br>
        - Make sure the key is of appropriate length.<br>
        - For modes like ECB, no IV is used."""

        self.setWindowTitle("Blowfish symmetric key block cipher")
        self.setFixedSize(1100, 550)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(200, 10, 120, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 500, 50)

        # Key
        key_label = QLabel("Choose key length \n (4 to 56 bytes long):", parent=self)
        key_label.setGeometry(10, 120, 150, 50)
        self.key_input = DefaultQLineEditStyle(parent=self,max_length=56)
        self.key_input.setGeometry(170, 120, 50, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, bold=True, command=self.call_blowfish_encryption)
        encrypt_button.setGeometry(300, 150, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 250, 500, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 370, 500, 50)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

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

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, bold=True, command=self.call_blowfish_decryption)
        decrypt_button.setGeometry(800, 260, 100, 50)

        self.original_msg_label = QTextEdit(parent=self)
        self.original_msg_label.setGeometry(600, 370, 480, 100)
        self.original_msg_label.setReadOnly(True)
        self.original_msg_label.hide()
    
    def call_blowfish_decryption(self):
        try:
            if self.ciphertext_input.text():
                if self.paste_key_input.text():
                    ciphertext_b64 = self.ciphertext_input.text()
                    key_b64 = self.paste_key_input.text()
                    key = b64decode(key_b64)
                    ciphertext = b64decode(ciphertext_b64)

                    blowfish = BlowfishImp(key=key)
                    plaintext = blowfish.decrypt_ECB(ciphertext)

                    self.original_msg_label.clear()
                    self.original_msg_label.setHtml(f"<b>Original plaintext: </b><br>{plaintext.decode('utf-8')}")
                    self.original_msg_label.show()
                else:
                    raise ValueError('Please paste the key.')
            else:
                raise ValueError('Please paste the ciphertext.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def call_blowfish_encryption(self):
        try:
            if self.plaintext_input.text():
                if self.key_input.text():
                    if int(self.key_input.text()) > 3 or int(self.key_input.text()) < 57:
                        plaintext = self.plaintext_input.text()
                        key_length = int(self.key_input.text())
                        key = urandom(key_length)

                        blowfish = BlowfishImp(key=key)
                        ciphertext = blowfish.encrypt_ECB(plaintext)

                        self.encrypted_text_label.clear()
                        self.encrypted_text_label.setHtml(f"<b>Ciphertext (Base64): </b><br>{b64encode(ciphertext).decode()}")
                        self.encrypted_text_label.show()

                        self.key_label.clear()
                        self.key_label.setHtml(f"<b>Key (Base64):</b><br> {b64encode(key).decode()}")
                        self.key_label.show()
                    else:
                        raise ValueError('Key must be from 4 to 56 bytes.')
                else:
                    raise ValueError('Please enter key length.')
            else:
                raise ValueError('Please enter plaintext.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
