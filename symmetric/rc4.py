from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from Crypto.Cipher                  import ARC4
from Crypto.Hash                    import SHA256, HMAC
from base64                         import b64encode, b64decode
from os                             import urandom

class RC4EncryptionWindow(QWidget):
    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About RC4 Encryption"
        msgbox_txt = ("RC4 (Rivest Cipher 4) is a stream cipher designed by Ron Rivest in 1987. "
        "It is widely used due to its simplicity and speed. RC4 generates a pseudo-random stream of bits (keystream) "
        "which is combined with the plaintext using the XOR operation to produce the ciphertext.<br><br>"
        "<b>Key Features of RC4:</b>"
        "<ul>"
        "<li>Symmetric Key Cipher: The same key is used for both encryption and decryption.</li>"
        "<li>Stream Cipher: Encrypts data one byte at a time, making it suitable for real-time applications.</li>"
        "<li>Variable Key Length: Supports key lengths from 40 to 2048 bits, with 128 bits being common.</li>"
        "<li>Simplicity: Easy to implement and requires minimal computational resources.</li>"
        "</ul>"
        "<b>Security Considerations:</b>"
        "<ul>"
        "<li>- Vulnerabilities: RC4 has known vulnerabilities, particularly in its key scheduling algorithm, making it less secure than modern ciphers.</li>"
        "<li>- Usage: Due to its vulnerabilities, RC4 is not recommended for new applications, and many protocols have moved away from it.</li>"
        "</ul>"
        "Overall, while RC4 was once a popular choice for encryption, its security weaknesses have led to a decline in its use in favor of more secure algorithms like AES.<br>"
        "<b>Useful links:</b> <ul>"
        "<li><a href='https://en.wikipedia.org/wiki/RC4'>RC4 - Wikipedia</a></li>"
        "<li><a href='https://www.geeksforgeeks.org/computer-networks/rc4-encryption-algorithm/'>Geeks for Geeks</a></li>"
        "</ul>")

        self.setWindowTitle("RC4 Encryption")
        self.setFixedSize(700, 600)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Key
        key_label = QLabel("Choose key length:", parent=self)
        key_label.setGeometry(170, 110, 150, 50)
        self.key_input = DefaultQComboBoxStyle(
            parent=self, items=["8", "16", "24", "32"])
        self.key_input.setGeometry(180, 150, 100, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, bold=True, command=self.rc4_encryption)
        encrypt_button.setGeometry(350, 150, 100, 50)

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 230, 680, 150)
        self.ciphertext_label.setReadOnly(True)
        self.ciphertext_label.hide()

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 400, 680, 100)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def rc4_encryption(self):
        plaintext = self.plaintext_input.text()
        if not plaintext:
            QMessageBox.warning(self, "Input Error", "Please enter plaintext to encrypt.")
            return

        key_bytes_length = int(self.key_input.currentText())
        key = urandom(key_bytes_length)  # Generate a random key of the selected length
        nonce = urandom(16)  # Generate a random nonce
        temp_key = HMAC.new(nonce, key, SHA256).digest()  # Derive a temporary key using HMAC-SHA256
        
        cipher = ARC4.new(temp_key)
        ciphertext = nonce + cipher.encrypt(plaintext.encode("utf-8"))

        b64_ciphertext = b64encode(ciphertext).decode()
        b64_key = b64encode(key).decode()

        self.ciphertext_label.clear()
        self.ciphertext_label.setHtml(f"<b>Ciphertext (Base64):</b><br> {b64_ciphertext}")
        self.ciphertext_label.show()

        self.key_label.clear()
        self.key_label.setHtml(f"<b>Generated Key (Base64):</b><br> {b64_key}")
        self.key_label.show()

# ================================================================================================================================================

class RC4DecryptionWindow(QWidget):
    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About RC4 Decryption"
        msgbox_txt = (
            "RC4 decryption reverses the encryption process using the same key. "
            "The ciphertext is Base64-decoded, the nonce is extracted, and the same "
            "temporary key derived using HMAC-SHA256 is used to restore the plaintext.")

        self.setWindowTitle("RC4 Decryption")
        self.setFixedSize(700, 600)

        # Ciphertext input
        ciphertext_label = QLabel("Enter Base64 Ciphertext:", parent=self)
        ciphertext_label.setGeometry(260, 10, 200, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(10, 60, 680, 50)

        # Key input
        key_label = QLabel("Enter Base64 Key:", parent=self)
        key_label.setGeometry(280, 110, 150, 50)
        self.key_input = DefaultQLineEditStyle(parent=self)
        self.key_input.setGeometry(10, 160, 680, 50)

        # Decrypt button
        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, bold=True, command=self.rc4_decryption)
        decrypt_button.setGeometry(300, 220, 100, 50)

        # Output area
        self.plaintext_label = QTextEdit(parent=self)
        self.plaintext_label.setGeometry(10, 300, 680, 250)
        self.plaintext_label.setReadOnly(True)
        self.plaintext_label.hide()

        # About button
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def rc4_decryption(self):
        b64_ciphertext = self.ciphertext_input.text().strip()
        b64_key = self.key_input.text().strip()

        if not b64_ciphertext or not b64_key:
            QMessageBox.warning(self, "Input Error", "Please provide both ciphertext and key.")
            return

        try:
            ciphertext = b64decode(b64_ciphertext)
            key = b64decode(b64_key)
        except Exception:
            QMessageBox.critical(self, "Decoding Error", "Invalid Base64 input.")
            return

        try:
            # Extract nonce (first 16 bytes)
            nonce = ciphertext[:16]
            ct = ciphertext[16:]

            # Derive same temp key
            temp_key = HMAC.new(nonce, key, SHA256).digest()

            cipher = ARC4.new(temp_key)
            plaintext_bytes = cipher.decrypt(ct)
            plaintext = plaintext_bytes.decode("utf-8", errors="replace")

            self.plaintext_label.clear()
            self.plaintext_label.setHtml(f"<b>Decrypted Plaintext:</b><br>{plaintext}")
            self.plaintext_label.show()

        except Exception as e:
            QMessageBox.critical(self, "Decryption Error", f"Decryption failed:\n{str(e)}")
