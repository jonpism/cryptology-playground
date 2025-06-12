from PyQt6.QtWidgets                import QWidget, QTextEdit, QLabel, QMessageBox
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from Crypto.Cipher                  import ChaCha20
from binascii                       import hexlify
import base64, os

# Implementation
class ChaCha20Imp:

    def __init__(self, key: bytes, nonce: bytes):
        """
        Initializes the ChaCha20 cipher. Generates random key and nonce if not provided.
        
        :param key: 32-byte key for encryption (if None, a random key is generated)
        :param nonce: 12-byte nonce (if None, a random nonce is generated)
        """
        # ChaCha20 requires a 32-byte (256-bit) key and 12-byte (96-bit) nonce.
        self.key = key
        self.nonce = nonce

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypts the given plaintext using ChaCha20.
        
        :param plaintext: The plaintext to encrypt (bytes)
        :return: The ciphertext (nonce + encrypted data) as bytes
        """
        cipher = ChaCha20.new(key=self.key, nonce=self.nonce)
        ciphertext = cipher.encrypt(plaintext)
        return self.nonce + ciphertext  # Prefix the nonce for decryption

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypts the given ciphertext using ChaCha20.
        
        :param ciphertext: The ciphertext to decrypt (bytes), must contain the nonce as a prefix
        :return: The decrypted plaintext (bytes)
        """
        nonce = ciphertext[:12]  # Extract the first 12 bytes as the nonce
        encrypted_message = ciphertext[12:]  # The rest is the encrypted message
        cipher = ChaCha20.new(key=self.key, nonce=nonce)
        plaintext = cipher.decrypt(encrypted_message)
        return plaintext

    def get_key(self) -> bytes:
        """
        Returns the encryption key.
        
        :return: The key used for encryption (32 bytes)
        """
        return self.key

    def get_nonce(self) -> bytes:
        """
        Returns the nonce used for encryption.
        
        :return: The nonce (12 bytes)
        """
        return self.nonce

class ChaCha20Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About ChaCha20"
        msgbox_txt = (
        "ChaCha20 is a high-speed, secure symmetric stream cipher designed by "
        "cryptographer Daniel J. Bernstein. It is an improved variant of "
        "the earlier Salsa20 cipher, and it has gained popularity due to its "
        "performance, simplicity, and robustness against cryptographic attacks. "
        "ChaCha20 is often used in applications requiring high security and speed, "
        "such as TLS for encrypted internet connections and mobile communications. "
        "It operates on 512-bit blocks of data, processed in 20 rounds (by default) "
        "to increase security. Each round consists of a series of quarter-round "
        "transformations that mix data in a way that ensures diffusion and confusion, "
        "making it resistant to cryptographic attacks. <br>"
        "Major tech companies like Google have adopted ChaCha20 for encrypting "
        "HTTPS traffic in Google Chrome, especially for mobile clients. <br><br>"
        "Useful links: <br>"
        "<a href=https://asecuritysite.com/encryption/salsa20>Asecuritysite</a><br>"
        "<a href=https://www.cryptography-primer.info/algorithms/chacha>Cryptography Primer</a>")        

        self.setWindowTitle("ChaCha20")
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

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_chacha20)
        encrypt_button.setGeometry(300, 260, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 340, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 450, 680, 100)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

        self.nonce_label = QTextEdit(parent=self)
        self.nonce_label.setGeometry(10, 560, 680, 50)
        self.nonce_label.setReadOnly(True)
        self.nonce_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        
    def call_chacha20(self):
        plaintext = self.plaintext_input.text()
        if plaintext:
            plaintext_bytes = plaintext.encode('utf-8')
        else:
            QMessageBox.warning(self, 'No input given', 'Please enter text')
            raise ValueError("Enter some text")
        
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

        chacha = ChaCha20Imp(key=key_bytes, nonce=nonce_bytes)
        ciphertext = chacha.encrypt(plaintext=plaintext_bytes)

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
            self.nonce_label.setHtml(f"<b>Nonce:</b><br>{str(nonce_bytes)}")
            self.nonce_label.show()
