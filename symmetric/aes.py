from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox, QInputDialog
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from Crypto.Cipher                  import AES
from Crypto.Random                  import get_random_bytes
from Crypto.Util.Padding            import pad, unpad
from os                             import urandom
from base64                         import b64encode, b64decode

# Implementation
class AES_Imp:

    def __init__(self, mode):
        self.mode = mode
    
    def encrypt(self, plaintext, key):
        if self.mode == "ECB":
            cipher = AES.new(key, AES.MODE_ECB)
            ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
            return ciphertext
        elif self.mode == "CBC":
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
            encrypted_data = iv + ciphertext
            return encrypted_data
 
    def decrypt_ECB(self, ciphertext, key):
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_data

    def decrypt_CBC(self, ciphertext, key):
        iv = ciphertext[: AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext[AES.block_size :]), AES.block_size)
        return decrypted_data

class AESEncryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About AES (Advanced Encryption Standard) Encryption"
        msgbox_txt = (
            "<p><strong>Advanced Encryption Standard (AES)</strong> is a symmetric key block cipher, standardized by the National Institute of Standards and Technology (NIST) in 2001. "
            "It is used worldwide to secure data and communications and has become the most widely adopted encryption algorithm.</p>"

            "<p><strong>AES Key Features:</strong></p>"
            "<ul>"
            "<li><strong>Symmetric Encryption:</strong> AES uses the same key for both encryption and decryption, making it faster and more efficient compared to asymmetric encryption methods like RSA.</li>"
            "<li><strong>Block Cipher:</strong> AES processes data in fixed-size blocks (128 bits). If the input data is larger, it is divided into multiple blocks and processed sequentially.</li>"
            "<li><strong>Key Sizes:</strong> AES supports three different key sizes: 128, 192, and 256 bits. AES-128 is commonly used, but AES-256 is preferred for higher security levels.</li>"
            "<li><strong>Security:</strong> AES is considered secure against all practical cryptographic attacks, including brute force, and has been extensively analyzed by cryptographers. As of now, no effective attack has been found.</li>"
            "</ul>"

            "<h3>AES Encryption Tool:</h3>"
            "<ul>"
            "<li><strong>Algorithms: </strong>AES-256 for key sizes of 32 bytes</li>"
            "<li><strong>Modes: </strong>The tool supports the modes: CBC, ECB(not secure)</li>"
            "</ul>"

            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/Advanced_Encryption_Standard'>AES - Wikipedia</a></li>"
            "<li><a href='https://crypto.stackexchange.com/questions/3926/how-does-aes-work'>How Does AES Work? - Crypto StackExchange</a></li>"
            "<li><a href='https://www.keylength.com/en/4/'>AES Key Lengths - Keylength.com</a></li>"
            "</ul>")

        self.setWindowTitle("AES Encryption")
        self.setFixedSize(700, 500)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 110, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, bold=True, command=self.call_aes_encryption)
        encrypt_button.setGeometry(300, 140, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 230, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 340, 680, 50)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

        self.selected_mode_label = QTextEdit(parent=self)
        self.selected_mode_label.setGeometry(10, 400, 180, 50)
        self.selected_mode_label.setReadOnly(True)
        self.selected_mode_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_aes_encryption(self):
        try:
            if self.plaintext_input.text():
                modes = ['CBC', 'ECB']
                mode, ok = QInputDialog.getItem(self,
                    "Select AES Mode",
                    "Choose an AES mode for encryption:",
                    modes, 0, False)
                if ok:
                    plaintext = self.plaintext_input.text().encode('utf-8')
                    key = urandom(32)
                    aes_enc = AES_Imp(mode=mode)
                    
                    ciphertext = aes_enc.encrypt(plaintext, key)
                    QMessageBox.information(self, 'Encryption successfull', f'Plaintext encrypted in mode: {mode}')

                    self.key_label.clear()
                    self.key_label.setHtml(f"<b>Key (Base64):</b><br> {b64encode(key).decode()}")
                    self.key_label.show()
                    self.encrypted_text_label.clear()
                    self.encrypted_text_label.setHtml(f"<b>Ciphertext (Base64):</b><br> {b64encode(ciphertext).decode()}")
                    self.encrypted_text_label.show()
                    self.selected_mode_label.clear()
                    self.selected_mode_label.setHtml(f"<b>Selected mode:</b><br> {str(mode)}")
                    self.selected_mode_label.show()                    
                else:
                    return
            else:
                raise ValueError('Please enter a plaintext.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

# ============================================================================================================================================

class AESDecryptionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About AES (Advanced Encryption Standard) Decryption"
        msgbox_txt = (
            "<p><strong>Advanced Encryption Standard (AES)</strong> is a symmetric key block cipher, standardized by the National Institute of Standards and Technology (NIST) in 2001. "
            "It is used worldwide to secure data and communications and has become the most widely adopted encryption algorithm.</p>"

            "<p><strong>AES Key Features:</strong></p>"
            "<ul>"
            "<li><strong>Symmetric Encryption:</strong> AES uses the same key for both encryption and decryption, making it faster and more efficient compared to asymmetric encryption methods like RSA.</li>"
            "<li><strong>Block Cipher:</strong> AES processes data in fixed-size blocks (128 bits). If the input data is larger, it is divided into multiple blocks and processed sequentially.</li>"
            "<li><strong>Key Sizes:</strong> AES supports three different key sizes: 128, 192, and 256 bits. AES-128 is commonly used, but AES-256 is preferred for higher security levels.</li>"
            "<li><strong>Security:</strong> AES is considered secure against all practical cryptographic attacks, including brute force, and has been extensively analyzed by cryptographers. As of now, no effective attack has been found.</li>"
            "</ul>"

            "<h3>AES Decryption Tool:</h3>"
            "<ul>"
            "<li><strong>Ciphertext: </strong>Paste the Base64 generated ciphertext during encryption</li>"
            "<li><strong>Key: </strong>Paste the Base64 generated 32 bytes key during encryption</li>"
            "</ul>"

            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/Advanced_Encryption_Standard'>AES - Wikipedia</a></li>"
            "<li><a href='https://crypto.stackexchange.com/questions/3926/how-does-aes-work'>How Does AES Work? - Crypto StackExchange</a></li>"
            "<li><a href='https://www.keylength.com/en/4/'>AES Key Lengths - Keylength.com</a></li>"
            "</ul>")

        self.setWindowTitle("AES Decryption")
        self.setFixedSize(700, 500)

        # Ciphertext input
        ciphertext_label = QLabel("Paste ciphertext:", parent=self)
        ciphertext_label.setGeometry(300, 10, 120, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(10, 60, 680, 50)

        # Key input
        key_label = QLabel("Paste key:", parent=self)
        key_label.setGeometry(300, 130, 100, 50)
        self.key_input = DefaultQLineEditStyle(parent=self)
        self.key_input.setGeometry(10, 180, 680, 50)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, bold=True, command=self.call_aes_decryption)
        decrypt_button.setGeometry(300, 270, 100, 50)

        self.original_msg_label = QTextEdit(parent=self)
        self.original_msg_label.setGeometry(10, 340, 680, 100)
        self.original_msg_label.setReadOnly(True)
        self.original_msg_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        
    def call_aes_decryption(self):
        try:
            if self.ciphertext_input.text():
                if self.key_input.text():
                    ciphertext_b64 = self.ciphertext_input.text()
                    key_b64 = self.key_input.text()

                    ciphertext = b64decode(ciphertext_b64)
                    key = b64decode(key_b64)

                    aes_dec = AES_Imp(mode=None)
                    decrypted_msg = None

                    try:
                        decrypted_msg = aes_dec.decrypt_ECB(ciphertext, key)
                        QMessageBox.information(self, 'Decryption successfull', 'Ciphertext decrypted successfully')
                        self.original_msg_label.clear()
                        self.original_msg_label.setHtml(f"<b>Original message/plaintext: (ECB mode)</b><br>{decrypted_msg.decode()}")
                        self.original_msg_label.show()
                    except:
                        try:
                            decrypted_msg = aes_dec.decrypt_CBC(ciphertext, key)
                            QMessageBox.information(self, 'Decryption successfull', 'Ciphertext decrypted successfully')
                            self.original_msg_label.clear()
                            self.original_msg_label.setHtml(f"<b>Original message/plaintext (CBC mode): </b><br>{decrypted_msg.decode()}")
                            self.original_msg_label.show()
                        except Exception as e:
                            raise Exception(str(e))
                else:
                    raise ValueError('Please enter key.')
            else:
                raise ValueError('Please paste ciphertext.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
