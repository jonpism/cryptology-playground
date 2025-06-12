from cryptography.hazmat.primitives.ciphers.aead    import ChaCha20Poly1305
from binascii                                       import hexlify
from PyQt6.QtWidgets                                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style                 import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style                 import DefaultQLineEditStyle 
import os, base64

# Implementation
class ChaCha20Poly1305Imp:
    
    def __init__(self, key: bytes, nonce: bytes):
        
        self.key = key if key else os.urandom(32)
        self.cipher = ChaCha20Poly1305(self.key)
        self.nonce = nonce if nonce else os.urandom(12)

    def encrypt(self, plaintext: bytes, associated_data: bytes = None) -> bytes:
        
        # Encrypt the plaintext, authenticate with associated data if provided
        ciphertext = self.cipher.encrypt(self.nonce, plaintext, associated_data)
        
        return self.nonce, ciphertext

    def decrypt(self, nonce: bytes, ciphertext: bytes, associated_data: bytes = None) -> bytes:
        # Decrypt the ciphertext, authenticate with associated data if provided
        try:
            plaintext = self.cipher.decrypt(nonce, ciphertext, associated_data)
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
        
        return plaintext
    
    def get_key(self) -> bytes:
        return self.key

    def get_nonce(self) -> bytes:
        return self.nonce

class ChaCha20Poly1305Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About ChaCha20-Poly1305"
        msgbox_txt = (
        "ChaCha20-Poly1305 is an authenticated encryption algorithm that combines the ChaCha20 "
        "stream cipher with the Poly1305 message authentication code (MAC) to provide both "
        "encryption and integrity for data. It's widely used for securing communications, "
        "notably in modern protocols like TLS, due to its strong security properties "
        "and performance advantages. <br> "
        "ChaCha20 encrypts the plaintext into ciphertext, and Poly1305 computes an "
        "authentication tag over the ciphertext, nonce, and optional associated data (AAD). "
        "The recipient can decrypt the message only if they can validate the tag, ensuring "
        "both confidentiality (only the recipient can decrypt) and integrity (ensuring no tampering). "
        "You can include unencrypted metadata (e.g., headers) in the authentication process "
        "without actually encrypting it. This is useful for data where confidentiality isn’t "
        "necessary but integrity is essential. <br> "
        "To secure HTTPS connections, ChaCha20-Poly1305 is often used as an alternative "
        "to AES-GCM, especially on mobile devices. <br>"
        "WireGuard uses ChaCha20-Poly1305 for its encryption and authentication, "
        "partly due to its efficiency on smaller devices. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/ChaCha20-Poly1305>Wikipedia</a><br>"
        "<a href=https://www.wikiwand.com/en/articles/ChaCha20-Poly1305>wikiwand</a>")

        self.setWindowTitle("ChaCha20-Poly1305")
        self.setFixedSize(700, 700)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Key
        key_label = QLabel("Give key.\nGenerates a random if none given:", parent=self)
        key_label.setGeometry(10, 110, 300, 50)
        self.key_input = DefaultQLineEditStyle(
            parent=self,
            max_length=32,
            placeholder_text="Key must be 32 bytes long.")
        self.key_input.setGeometry(10, 160, 320, 50)

        # Nonce
        nonce_label = QLabel("Give Nonce. \nGenerates a random if none given:", parent=self)
        nonce_label.setGeometry(410, 110, 240, 50)
        self.nonce_input = DefaultQLineEditStyle(
            parent=self,
            max_length=12,
            placeholder_text="Must be 12 bytes long.")
        self.nonce_input.setGeometry(410, 160, 200, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(150, 210, 120, 50)
        output_format_items = ['Base64', 'Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(150, 260, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_chachapoly)
        encrypt_button.setGeometry(300, 260, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 380, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 530, 680, 50)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

        self.nonce_label = QTextEdit(parent=self)
        self.nonce_label.setGeometry(10, 630, 680, 50)
        self.nonce_label.setReadOnly(True)
        self.nonce_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        
    def call_chachapoly(self):
        plaintext = self.plaintext_input.text()
        if plaintext:
            plaintext_bytes = plaintext.encode('utf-8')
        else:
            raise ValueError("Give some text")
        
        key = self.key_input.text()
        if key:
            key_bytes = key.encode('utf-8')
        else:
            key_bytes = os.urandom(32)

        nonce = self.nonce_input.text()
        if nonce:
            nonce_bytes = nonce.encode('utf-8')
        else:
            nonce_bytes = os.urandom(12)

        output_format = self.output_format_options.currentText()
        associated_data = None

        chachapoly = ChaCha20Poly1305Imp(key=key_bytes, nonce=nonce_bytes)
        nonce, ciphertext = chachapoly.encrypt(plaintext=plaintext_bytes, associated_data=associated_data)

        formatted_ciphertext = ciphertext
        if output_format == "Base64":
            formatted_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        if output_format == "Hex":
            formatted_ciphertext = hexlify(ciphertext).decode('utf-8')

        self.encrypted_text_label.clear()
        self.encrypted_text_label.setHtml(f"<b>Encrypted text:</b><br>{str(formatted_ciphertext)}")
        self.encrypted_text_label.show()

        if key == "":
            self.key_label.clear()
            self.key_label.setHtml(f"<b>Random Key:</b><br>{str(key_bytes)}")
            self.key_label.show()
        else:
            self.key_label.clear()
            self.key_label.setHtml(f"<b>Key:</b><br>{str(key)}")
            self.key_label.show()
        
        if nonce == "":
            self.nonce_label.clear()
            self.nonce_label.setHtml(f"<b>Nonce:</b><br>{str(nonce)}")
            self.nonce_label.show()
