from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from Cryptodome.Cipher              import ARC2
from base64                         import b64encode, b64decode
from os                             import urandom

class RC2Encryption:

    def __init__(self, key: bytes, effective_keylen: int = 1024):
        """Initialize the RC2 cipher.
        
        :param key: The key used for encryption/decryption (up to 128 bits).
        :param effective_keylen: Effective key length in bits (default is 1024 bits)."""
        self.key = key
        self.effective_keylen = effective_keylen

    def encrypt_ECB(self, plaintext: bytes) -> bytes:
        """Encrypt plaintext using RC2 in ECB mode.
        
        :param plaintext: The plaintext to encrypt (must be a multiple of the block size).
        :return: Encrypted ciphertext."""
        cipher = ARC2.new(self.key, ARC2.MODE_ECB, effective_keylen=self.effective_keylen)
        padded = self.pad(plaintext)
        return cipher.encrypt(padded)
    
    def pad(self, data: bytes, block_size: int = 8) -> bytes:
        padding_len = block_size - len(data) % block_size
        return data + bytes([padding_len] * padding_len)

class RC2EncryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About RC2 Encryption"
        msgbox_txt = """<p><b>RC2</b> (Rivest Cipher 2) is a symmetric block cipher developed by Ron Rivest in 1987. It operates on 64-bit blocks using variable-length keys (up to 128 bits).</p>
        <p>This tool encrypts data using the <b>RC2 algorithm in ECB (Electronic Codebook) mode</b>. In this mode:</p>
        <ul>
            <li>Plaintext is divided into fixed-size blocks (8 bytes for RC2).</li>
            <li>Each block is encrypted independently.</li>
        </ul>
        <p><b>Note:</b> ECB mode is <i>not semantically secure</i> for large or repeating data patterns. For better security, consider using CBC or other modes in future updates.</p>
        <p>A random 128-bit key is generated automatically for each encryption. You must securely store this key to decrypt the ciphertext later.</p>
        <p style="color:darkred;"><b>Supported Mode:</b> Only ECB mode is currently implemented in this tool.</p>"""

        self.setWindowTitle("RC2 Encryption")
        self.setFixedSize(700, 600)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Modes
        modes_list = ["ECB", "CFB", "CTR", "EAX", "CBC", "OFB"]
        mode_label = QLabel("MODE:", parent=self)
        mode_label.setGeometry(200, 130, 120, 50)
        self.mode_options = DefaultQComboBoxStyle(parent=self, items=modes_list)
        self.mode_options.setGeometry(180, 180, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, bold=True, command=self.call_rc2_encryption)
        encrypt_button.setGeometry(350, 180, 100, 50)

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 280, 680, 100)
        self.ciphertext_label.setReadOnly(True)
        self.ciphertext_label.hide()

        self.generated_key_label = QTextEdit(parent=self)
        self.generated_key_label.setGeometry(10, 400, 680, 100)
        self.generated_key_label.setReadOnly(True)
        self.generated_key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def call_rc2_encryption(self):
        try:
            if self.plaintext_input.text():
                plaintext = self.plaintext_input.text()
                plaintext_bytes = plaintext.encode()
                key_bytes = urandom(16)
                mode = self.mode_options.currentText()

                rc2_encryption = RC2Encryption(key_bytes, 1024)
                if mode == "ECB":
                    ciphertext = rc2_encryption.encrypt_ECB(plaintext_bytes)
                    self.ciphertext_label.clear()
                    self.ciphertext_label.setHtml(f"<b>Ciphertext:</b><br>{b64encode(ciphertext).decode('utf-8')}")
                    self.ciphertext_label.show()

                    self.generated_key_label.clear()
                    self.generated_key_label.setHtml(f"<b>Generated key:</b><br>{b64encode(key_bytes).decode('utf-8')}")
                    self.generated_key_label.show()
                else:
                    raise ValueError('The tool supports only ECB mode for now.')
            else:
                raise ValueError('Please enter plaintext.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

# ========================================================================================================================

class RC2Decryption:

    def __init__(self, key: bytes, effective_keylen: int = 1024):
        self.key = key
        self.effective_keylen = effective_keylen
    
    def decrypt_ECB(self, ciphertext: bytes) -> bytes:
        """Decrypt ciphertext using RC2 in ECB mode.
        
        :param ciphertext: The ciphertext to decrypt.
        :return: Decrypted plaintext."""
        cipher = ARC2.new(self.key, ARC2.MODE_ECB, effective_keylen=self.effective_keylen)
        return cipher.decrypt(ciphertext)
    
    def unpad(self, data: bytes) -> bytes:
        padding_len = data[-1]
        return data[:-padding_len]

class RC2DecryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About RC2 Decryption"
        msgbox_txt = """<p>This tool decrypts ciphertext that was encrypted using the <b>RC2 algorithm in ECB mode</b>.</p>
        <p>To decrypt successfully, you must:</p>
        <ul>
            <li>Paste the Base64-encoded ciphertext.</li>
            <li>Paste the exact Base64-encoded key that was used for encryption.</li>
        </ul>
        <p>The tool automatically removes padding that was added during encryption to restore the original plaintext.</p>
        <p style="color:darkred;"><b>Important:</b> If you lose the encryption key or input an incorrect one, decryption will fail or return invalid text.</p>
        <p style="color:darkred;"><b>Note:</b> Only ECB mode decryption is currently supported.</p>"""

        self.setWindowTitle("RC2 Decryption")
        self.setFixedSize(700, 600)

        # ciphertext
        ciphertext_label = QLabel("Paste ciphertext:", parent=self)
        ciphertext_label.setGeometry(300, 10, 120, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(10, 60, 680, 50)

        paste_key_label = QLabel("Paste key:", parent=self)
        paste_key_label.setGeometry(320, 130, 100, 50)
        self.paste_key_input = DefaultQLineEditStyle(parent=self)
        self.paste_key_input.setGeometry(10, 180, 680, 50)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, bold=True, command=self.call_rc2_decryption)
        decrypt_button.setGeometry(300, 260, 100, 50)

        self.original_msg_label = QTextEdit(parent=self)
        self.original_msg_label.setGeometry(10, 370, 680, 100)
        self.original_msg_label.setReadOnly(True)
        self.original_msg_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_rc2_decryption(self):
        try:
            if self.ciphertext_input.text():
                if self.paste_key_input.text():
                    b64_ciphertext = self.ciphertext_input.text().strip()
                    b64_key = self.paste_key_input.text().strip()

                    ciphertext = b64decode(b64_ciphertext)
                    key = b64decode(b64_key)

                    rc2_decryption = RC2Decryption(key, 1024)
                    decrypted_padded = rc2_decryption.decrypt_ECB(ciphertext)
                    plaintext = rc2_decryption.unpad(decrypted_padded).decode('utf-8')

                    self.original_msg_label.clear()
                    self.original_msg_label.setHtml(f"<b>Decrypted Plaintext:</b><br>{plaintext}")
                    self.original_msg_label.show()
                else:
                    raise ValueError('Please paste key.')
            else:
                raise ValueError('Please paste plaintext')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
