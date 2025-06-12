from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from cryptography.hazmat.primitives import padding
from base64                         import b64encode, b64decode
from os                             import urandom 
import camellia

BLOCK_SIZE = camellia.block_size

class CamelliaEncryption:

    def __init__(self, key: bytes, mode: str, plaintext: str):
        # Camellia accepts key sizes of 128, 192, or 256 bits.
        self.key = key
        self.ciphertext = None
        if mode == "ECB":
            self.mode = 1
            self.ciphertext = self.encrypt_ECB(plaintext)

    def encrypt_ECB(self, plaintext: str) -> bytes:
        c = camellia.CamelliaCipher(self.key, mode=self.mode)
        plaintext = plaintext.encode('utf-8')

        padded = padding.PKCS7(128).padder()
        padded_data = padded.update(plaintext) + padded.finalize()

        ciphertext = c.encrypt(padded_data)
        return ciphertext

class CamelliaDecryption:

    def __init__(self, key: bytes, ciphertext: bytes):
        self.key = key
        self.plaintext = None
        try:
            self.plaintext = self.decrypt_ECB(ciphertext)
        except:
            pass # decrypt other modes

    def decrypt_ECB(self, ciphertext: bytes) -> str:
        c = camellia.CamelliaCipher(self.key, mode=1)
        decrypted_data = c.decrypt(ciphertext)

        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(decrypted_data) + unpadder.finalize()

        return plaintext.decode('utf-8')

class CamelliaWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Camellia symmetric key block cipher"
        msgbox_txt = """
        This tool implements the Camellia block cipher, which is a symmetric-key encryption algorithm designed by Mitsubishi Electric and NTT. It is known for its high security and efficiency, providing encryption and decryption with key sizes of 128, 192, or 256 bits.<br><br>
        <b>Key Features:</b>
        <ul>
            <li>Supports key sizes of 128, 192, or 256 bits.</li>
            <li>Offers multiple encryption modes: ECB (for now).</li>
            <li>Provides secure encryption and decryption of data using a secret key.</li>
        </ul>
        <b>Instructions:</b><br>
        1. Enter the <b>plaintext</b> you wish to encrypt in the provided field.<br>
        2. Specify the <b>key</b> for encryption (16, 24, or 32 bytes long).<br>
        3. Choose the <b>encryption mode</b> you would like to use: ECB (for now).<br>
        4. Click <b>Encrypt</b> to perform the encryption.<br><br>
        <b>Important Notes:</b><br>
        - For modes like ECB, no IV is used, but other modes such as CBC, CFB, and OFB require an IV.<br>
        - For CTR mode, a nonce will be generated if not provided.<br>"""

        self.setWindowTitle("Camellia symmetric key block cipher")
        self.setFixedSize(1100, 700)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(200, 10, 120, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 480, 50)

        # Key
        key_label = QLabel("Choose key length:", parent=self)
        key_label.setGeometry(10, 120, 150, 50)
        self.key_input = DefaultQComboBoxStyle(
            parent=self, items=["16", "24", "32"])
        self.key_input.setGeometry(20, 160, 100, 50)

        # mode
        mode_label = QLabel("Select mode:", parent=self)
        mode_label.setGeometry(200, 120, 100, 50)
        self.mode_input = DefaultQComboBoxStyle(
            parent=self, items=["ECB"])
        self.mode_input.setGeometry(200, 160, 100, 50) 

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, bold=True, command=self.call_camellia_encryption)
        encrypt_button.setGeometry(350, 160, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 260, 480, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.generated_key_label = QTextEdit(parent=self)
        self.generated_key_label.setGeometry(10, 380, 480, 50)
        self.generated_key_label.setReadOnly(True)
        self.generated_key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(1050, 650, 50, 50))
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

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, bold=True, command=self.call_camellia_decryption)
        decrypt_button.setGeometry(800, 260, 100, 50)

        self.original_msg_label = QTextEdit(parent=self)
        self.original_msg_label.setGeometry(600, 370, 480, 100)
        self.original_msg_label.setReadOnly(True)
        self.original_msg_label.hide()
    
    def call_camellia_decryption(self):
        try:
            if self.ciphertext_input.text():
                if self.paste_key_input.text():
                    ciphertext_b64 = self.ciphertext_input.text()
                    key_b64 = self.paste_key_input.text()
                    key = b64decode(key_b64)
                    ciphertext = b64decode(ciphertext_b64)

                    decryption = CamelliaDecryption(key, ciphertext)
                    plaintext = decryption.plaintext

                    self.original_msg_label.clear()
                    self.original_msg_label.setHtml(f"<b>Decrypted text:</b><br>{plaintext}")
                    self.original_msg_label.show()

                else:
                    raise ValueError('Please enter key.')
            else:
                raise ValueError('Please paste ciphertext.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def call_camellia_encryption(self):
        try:
            if self.plaintext_input.text():
                plaintext = self.plaintext_input.text()
                mode = self.mode_input.currentText()
                key_length = int(self.key_input.currentText())
                key = urandom(key_length)

                encryption = CamelliaEncryption(key, mode, plaintext)
                ciphertext = encryption.ciphertext

                self.encrypted_text_label.clear()
                self.encrypted_text_label.setHtml(f"<b>Encrypted text:</b><br>{b64encode(ciphertext).decode()}")
                self.encrypted_text_label.show()

                self.generated_key_label.clear()
                self.generated_key_label.setHtml(f"<b>Generated key of {key_length} bytes:</b><br>{b64encode(key).decode()}")
                self.generated_key_label.show()
            else:
                raise ValueError('Please enter plaintext.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
