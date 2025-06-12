from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from Crypto.Cipher                  import DES3
from os                             import urandom
from Crypto.Util.Padding            import pad, unpad
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from base64                         import b64encode, b64decode

class TripleDESEncryption:
    
    def __init__(self, key: bytes, mode: str, plaintext: str):
        # Adjust the key to ensure it meets parity requirements
        self.key = DES3.adjust_key_parity(key)
        self.mode = mode
        self.ciphertext = None

        if self.mode == 'ECB':
            self.cipher_mode = DES3.MODE_ECB
            self.ciphertext = self.encrypt_ECB(plaintext)

    def encrypt_ECB(self, plaintext: str) -> bytes:
        cipher = DES3.new(self.key, self.cipher_mode)

        # Pad the plaintext and encrypt it
        padded_data = pad(plaintext.encode('utf-8'), DES3.block_size)
        ciphertext = cipher.encrypt(padded_data)

        return ciphertext
    
class TripleDESEncryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Triple DES Encryption"
        msgbox_txt = """
        <p><b>Triple DES (3DES)</b> is a symmetric-key block cipher that applies the DES algorithm three times to each data block.</p>
        <ul>
            <li><b>Key Length:</b> Choose 16 or 24 bytes.</li>
            <li><b>Block Size:</b> Fixed at 64 bits (8 bytes).</li>
            <li><b>Mode Used:</b> ECB (Electronic Codebook) — each block is encrypted independently.</li>
        </ul>
        <p><b>Note:</b> ECB mode is generally not recommended for sensitive data, as it does not hide data patterns.</p>
        <p style="color:gray; font-size:small;">For demonstration purposes only.</p>"""

        self.setWindowTitle("Triple DES Encryption")
        self.setFixedSize(700, 550)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 120, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Key
        key_label = QLabel("Choose key bytes:", parent=self)
        key_label.setGeometry(10, 110, 300, 50)
        self.key_input = DefaultQComboBoxStyle(
            parent=self,
            items=["16", "24"])
        self.key_input.setGeometry(20, 160, 80, 50)

        # Mode
        modes_list = [
            "ECB", "CBC", "CFB", "CTR", "EAX", "OFB"]
        mode_label = QLabel("MODE:", parent=self)
        mode_label.setGeometry(240, 110, 120, 50)
        self.mode_options = DefaultQComboBoxStyle(parent=self, items=modes_list)
        self.mode_options.setGeometry(220, 160, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, bold=True, command=self.call_3des_encryption)
        encrypt_button.setGeometry(420, 160, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 280, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.generated_key_label = QTextEdit(parent=self)
        self.generated_key_label.setGeometry(10, 430, 680, 50)
        self.generated_key_label.setReadOnly(True)
        self.generated_key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 500, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_3des_encryption(self):
        try:
            if self.plaintext_input.text():
                plaintext_str = self.plaintext_input.text()
                key_length = int(self.key_input.currentText())
                key = urandom(key_length)
                mode = self.mode_options.currentText()

                if mode != "ECB":
                    raise ValueError('Only ECB mode is implemented.')

                tdesencryption = TripleDESEncryption(key, mode, plaintext_str)
                ciphertext = tdesencryption.ciphertext

                self.encrypted_text_label.clear()
                self.encrypted_text_label.setHtml(f"<b>Ciphertext (Base64):</b><br>{b64encode(ciphertext).decode()}")
                self.encrypted_text_label.show()

                self.generated_key_label.clear()
                self.generated_key_label.setHtml(f"<b>Generated {key_length} byte length key (Base64):</b><br>{b64encode(key).decode()}")
                self.generated_key_label.show()

            else:
                raise ValueError('Please enter plaintext.')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

# ===================================================================================================================================

class TripleDESDecryption:
    
    def __init__(self, key: bytes, ciphertext: bytes):
        # Adjust the key for parity as required by DES3
        self.key = DES3.adjust_key_parity(key)
        self.ciphertext = ciphertext
        self.plaintext = None
        try:
            self.plaintext = self.decrypt_ECB(ciphertext)
        except: # another mode
            pass

    def decrypt_ECB(self, ciphertext: bytes) -> str:
        cipher = DES3.new(self.key, DES3.MODE_ECB)
        decrypted_data = cipher.decrypt(ciphertext)
        try:
            unpadded_data = unpad(decrypted_data, DES3.block_size)
            return unpadded_data.decode('utf-8')
        except ValueError:
            raise ValueError("Incorrect decryption or padding.")

class TripleDESDecryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Triple DES Deryption"
        msgbox_txt = """
        <p>This tool decrypts ciphertext that was encrypted using <b>Triple DES</b> in <b>ECB mode</b>.</p>
        <ul>
            <li>Paste the <b>Base64-encoded ciphertext</b> and the <b>Base64-encoded key</b>.</li>
            <li>Ensure the key length matches (16 or 24 bytes) and was generated correctly.</li>
            <li>ECB mode decrypts each block independently.</li>
        </ul>
        <p style="color:gray; font-size:small;">Make sure the data has not been altered; incorrect keys or padding will raise an error.</p>"""

        self.setWindowTitle("Triple DES Decryption")
        self.setFixedSize(700, 600)

        # ciphertext
        ciphertext_label = QLabel("Paste ciphertext:", parent=self)
        ciphertext_label.setGeometry(300, 10, 120, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(10, 60, 680, 50)

        paste_key_label = QLabel("Paste key:", parent=self)
        paste_key_label.setGeometry(300, 130, 100, 50)
        self.paste_key_input = DefaultQLineEditStyle(parent=self)
        self.paste_key_input.setGeometry(10, 180, 680, 50)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, bold=True, command=self.call_3des_decryption)
        decrypt_button.setGeometry(300, 260, 100, 50)

        self.original_msg_label = QTextEdit(parent=self)
        self.original_msg_label.setGeometry(10, 370, 680, 100)
        self.original_msg_label.setReadOnly(True)
        self.original_msg_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def call_3des_decryption(self):
        try:
            if self.ciphertext_input.text():
                if self.paste_key_input.text():
                    ciphertext_b64 = self.ciphertext_input.text()
                    key_b64 = self.paste_key_input.text()

                    key = b64decode(key_b64)
                    ciphertext = b64decode(ciphertext_b64)

                    decryption = TripleDESDecryption(key, ciphertext)
                    plaintext = decryption.plaintext

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

