from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from binascii                       import hexlify
from os                             import urandom
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
import base64

# Implementation
class TEAImp:
    def __init__(self, key: bytes):
        """Initialize the TEA cipher with a 128-bit key (16 bytes)."""
        if len(key) != 16:
            raise ValueError("Key must be 128 bits (16 bytes).")
        
        # Split the key into four 32-bit parts
        self.k = [int.from_bytes(key[i:i + 4], byteorder='big') for i in range(0, 16, 4)]
        self.delta = 0x9E3779B9
        self.num_rounds = 32  # Typically 64 Feistel rounds

    def encrypt(self, block: bytes) -> bytes:
        """Encrypt a 64-bit block of data."""
        if len(block) != 8:
            raise ValueError("Block must be 64 bits (8 bytes).")
        
        v0, v1 = int.from_bytes(block[:4], byteorder='big'), int.from_bytes(block[4:], byteorder='big')
        sum_val = 0

        for _ in range(self.num_rounds):
            sum_val = (sum_val + self.delta) & 0xFFFFFFFF
            v0 = (v0 + (((v1 << 4) + self.k[0]) ^ (v1 + sum_val) ^ ((v1 >> 5) + self.k[1]))) & 0xFFFFFFFF
            v1 = (v1 + (((v0 << 4) + self.k[2]) ^ (v0 + sum_val) ^ ((v0 >> 5) + self.k[3]))) & 0xFFFFFFFF

        return v0.to_bytes(4, byteorder='big') + v1.to_bytes(4, byteorder='big')

    def decrypt(self, block: bytes) -> bytes:
        """Decrypt a 64-bit block of data."""
        if len(block) != 8:
            raise ValueError("Block must be 64 bits (8 bytes).")
        
        v0, v1 = int.from_bytes(block[:4], byteorder='big'), int.from_bytes(block[4:], byteorder='big')
        sum_val = (self.delta * self.num_rounds) & 0xFFFFFFFF

        for _ in range(self.num_rounds):
            v1 = (v1 - (((v0 << 4) + self.k[2]) ^ (v0 + sum_val) ^ ((v0 >> 5) + self.k[3]))) & 0xFFFFFFFF
            v0 = (v0 - (((v1 << 4) + self.k[0]) ^ (v1 + sum_val) ^ ((v1 >> 5) + self.k[1]))) & 0xFFFFFFFF
            sum_val = (sum_val - self.delta) & 0xFFFFFFFF

        return v0.to_bytes(4, byteorder='big') + v1.to_bytes(4, byteorder='big')

class TEAWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About TEA"
        msgbox_txt = (
        "The Tiny Encryption Algorithm (TEA) is a simple yet effective symmetric "
        "key block cipher that was designed by David Wheeler and Roger Needham "
        "of the Cambridge Computer Laboratory in 1994. TEA is known for its simplicity, "
        "efficiency, and ease of implementation, making it suitable for environments "
        "where resources are constrained, like embedded systems. TEA is a Feistel cipher, "
        "which means it divides the input block into two halves and repeatedly applies "
        "a round function to scramble the data. This structure is similar to other block "
        "ciphers, like DES (Data Encryption Standard). <br> "
        "TEA's design philosophy is simplicity. It uses only primitive operations that are "
        "available in most instruction sets, like addition, XOR, and shifts. This simplicity "
        "allows for straightforward and fast implementations in both software and hardware. <br> "
        "Due to its known weaknesses, for more sensitive applications, it is recommended "
        "to use stronger ciphers like AES (Advanced Encryption Standard) or at least the "
        "improved variants like XTEA or XXTEA. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm>Wikipedia</a><br>"
        "<a href=https://link.springer.com/content/pdf/10.1007/3-540-60590-8_29.pdf>Springer</a>")        

        self.setWindowTitle("TEA block cipher (Tiny Encryption Algorithm)")
        self.setFixedSize(700, 700)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self, placeholder_text="Plaintext must be 8 bytes only.", max_length=8)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Key
        key_label = QLabel("Give key.\nGenerates a random if none given:", parent=self)
        key_label.setGeometry(10, 110, 300, 50)
        self.key_input = DefaultQLineEditStyle(
            parent=self,
            max_length=16,
            placeholder_text="Key must be 16 bytes long.")
        self.key_input.setGeometry(10, 160, 320, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(150, 210, 120, 50)
        output_format_items = ['Base64', 'Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(150, 260, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_tea)
        encrypt_button.setGeometry(300, 260, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 380, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 530, 680, 50)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        
    def call_tea(self):
        plaintext = self.plaintext_input.text()
        plaintext_bytes = plaintext.encode('utf-8')
        key = self.key_input.text()
        output_format = self.output_format_options.currentText()

        if key == "":
            key_bytes = urandom(16)
        else:
            if len(key) == 16:
                key_bytes = key.encode('utf-8')
            else:
                raise ValueError("Give Key with 16 bytes")
            
        tea = TEAImp(key=key_bytes)
        ciphertext = tea.encrypt(block=plaintext_bytes)

        formatted_ciphertext = ciphertext
        if output_format == "Base64":
            formatted_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        if output_format == "Hex":
            formatted_ciphertext = hexlify(ciphertext).decode('utf-8')

        self.encrypted_text_label.clear()
        self.encrypted_text_label.setHtml(f"<b>Ciphertext:</b><br>{str(formatted_ciphertext)}")
        self.encrypted_text_label.show()

        if key == "":
            self.key_label.clear()
            self.key_label.setHtml(f"<b>Random Key:</b><br>{str(key_bytes)}")
            self.key_label.show()
        else:
            self.key_label.clear()
            self.key_label.setHtml(f"<b>Key:</b><br>{str(key)}")
            self.key_label.show()

'''DECRYPT

decrypted = tea.decrypt(ciphertext)
print(f"Decrypted: {decrypted.decode('utf-8')}")

'''