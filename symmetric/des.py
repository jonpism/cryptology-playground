from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from Crypto.Util.Padding            import pad, unpad
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from os                             import urandom
from base64                         import b64encode, b64decode
import des

class DES_Encryption_Imp:

    def __init__(self, key: bytes, plaintext: str, mode: str):
        self.key = des.DesKey(key)
        self.plaintext = plaintext
        self.ciphertext = None
        if mode == "ECB":
            self.ciphertext = self.encrypt_ECB(plaintext)

    def encrypt_ECB(self, plaintext: str) -> bytes:
        plaintext = plaintext.encode('utf-8')
        ciphertext = self.key.encrypt(plaintext, padding=True)
        return ciphertext

class DESEncryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Data Encryption Standard - Encryption"
        msgbox_txt = (
        "<b>DES Encryption Tool</b><br><br>"
        "This tool implements Data Encryption Standard (DES) for encrypting text.<br><br>"
        "You can choose from various DES modes, each offering different features:<br>"
        "<ul>"
        "<li><b>ECB (Electronic Codebook):</b> Simplest form, but less secure.</li>"
        "<li><b>CBC (Cipher Block Chaining):</b> Uses an initialization vector (IV) for better security.</li>"
        "<li><b>CFB (Cipher Feedback):</b> Suitable for stream ciphers.</li>"
        "<li><b>CTR (Counter):</b> Converts the block cipher into a stream cipher using a nonce.</li>"
        "<li><b>EAX:</b> A mode that combines both encryption and authentication.</li>"
        "<li><b>OFB (Output Feedback):</b> Another stream cipher mode similar to CFB.</li>"
        "</ul><br>"
        "<b>Instructions:</b><br>"
        "To use, simply enter your plaintext, select key bytes, choose mode and Encrypt.<br>"
        "Once encrypted, the result will be shown in Base64 output format.<br>")

        self.setWindowTitle("DES Encryption")
        self.setFixedSize(700, 600)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 120, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Key
        key_label = QLabel("Choose key length:", parent=self)
        key_label.setGeometry(10, 120, 150, 50)
        self.key_input = DefaultQComboBoxStyle(
            parent=self, items=["8", "16", "24"])
        self.key_input.setGeometry(20, 160, 100, 50)

        # mode
        mode_label = QLabel("Select mode:", parent=self)
        mode_label.setGeometry(200, 120, 100, 50)
        self.mode_input = DefaultQComboBoxStyle(
            parent=self, items=["ECB"])
        self.mode_input.setGeometry(200, 160, 100, 50) 

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, bold=True, command=self.call_des_encryption)
        encrypt_button.setGeometry(350, 160, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 280, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.generated_key_label = QTextEdit(parent=self)
        self.generated_key_label.setGeometry(10, 430, 680, 50)
        self.generated_key_label.setReadOnly(True)
        self.generated_key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_des_encryption(self):
        try:
            if self.plaintext_input.text():
                plaintext = self.plaintext_input.text()
                key_length = int(self.key_input.currentText())
                key = urandom(key_length)
                mode = self.mode_input.currentText()

                des_encryption = DES_Encryption_Imp(key, plaintext, mode)
                ciphertext = des_encryption.ciphertext

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

# ==========================================================================================================

class DES_Decryption_Imp:

    def __init__(self, key: bytes, ciphertext: bytes):
        self.key = key
        self.plaintext = None
        try:
            self.plaintext = self.decrypt_ECB(ciphertext)
        except:
            pass # decrypt other modes

    def decrypt_ECB(self, ciphertext: bytes) -> str:
        key_obj = des.DesKey(self.key)
        plaintext_bytes = key_obj.decrypt(ciphertext, padding=True)
        return plaintext_bytes.decode('utf-8')

class DESDecryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = ""
        msgbox_txt = ""

        self.setWindowTitle("DES Decryption")
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

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, bold=True, command=self.call_des_decryption)
        decrypt_button.setGeometry(300, 260, 100, 50)

        self.original_msg_label = QTextEdit(parent=self)
        self.original_msg_label.setGeometry(10, 370, 680, 100)
        self.original_msg_label.setReadOnly(True)
        self.original_msg_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def call_des_decryption(self):
        try:
            if self.ciphertext_input.text():
                if self.paste_key_input.text():
                    ciphertext_b64 = self.ciphertext_input.text()
                    key_b64 = self.paste_key_input.text()

                    key = b64decode(key_b64)
                    ciphertext = b64decode(ciphertext_b64)

                    decryption = DES_Decryption_Imp(key, ciphertext)
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
