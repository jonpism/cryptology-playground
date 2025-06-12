from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from binascii                       import hexlify
from os                             import urandom
import base64

# Implementation
class XTEAImp:
    def __init__(self, key: bytes):

        if len(key) != 16:
            raise ValueError("Key must be 128 bits (16 bytes) long.")
        self.key = self._key_schedule(key)

    def _key_schedule(self, key: bytes):
        """Divide the 128-bit key into four 32-bit blocks."""
        return [int.from_bytes(key[i:i+4], 'big') for i in range(0, 16, 4)]

    def _encrypt_block(self, block: bytes, num_rounds=64):
        v0, v1 = int.from_bytes(block[:4], 'big'), int.from_bytes(block[4:], 'big')
        delta = 0x9E3779B9
        sum_value = 0

        for _ in range(num_rounds):
            v0 = (v0 + (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum_value + self.key[sum_value & 3])) & 0xFFFFFFFF
            sum_value = (sum_value + delta) & 0xFFFFFFFF
            v1 = (v1 + (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum_value + self.key[(sum_value >> 11) & 3])) & 0xFFFFFFFF

        return v0.to_bytes(4, 'big') + v1.to_bytes(4, 'big')

    def _decrypt_block(self, block: bytes, num_rounds=64):
        v0, v1 = int.from_bytes(block[:4], 'big'), int.from_bytes(block[4:], 'big')
        delta = 0x9E3779B9
        sum_value = (delta * num_rounds) & 0xFFFFFFFF

        for _ in range(num_rounds):
            v1 = (v1 - (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum_value + self.key[(sum_value >> 11) & 3])) & 0xFFFFFFFF
            sum_value = (sum_value - delta) & 0xFFFFFFFF
            v0 = (v0 - (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum_value + self.key[sum_value & 3])) & 0xFFFFFFFF

        return v0.to_bytes(4, 'big') + v1.to_bytes(4, 'big')

    def encrypt(self, plaintext: bytes):
        if len(plaintext) % 8 != 0:
            raise ValueError("Plaintext must be a multiple of 8 bytes.")
        ciphertext = b""
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            ciphertext += self._encrypt_block(block)
        return ciphertext

    def decrypt(self, ciphertext: bytes):
        if len(ciphertext) % 8 != 0:
            raise ValueError("Ciphertext must be a multiple of 8 bytes.")
        plaintext = b""
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            plaintext += self._decrypt_block(block)
        return plaintext

class XTEAWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About XTEA"
        msgbox_txt = (
        "XTEA (eXtended Tiny Encryption Algorithm) is a block cipher designed "
        "to provide secure encryption using simple operations that are "
        "computationally efficient. It is an improvement on the original TEA "
        "(Tiny Encryption Algorithm) and was developed to address some of TEA's "
        "vulnerabilities. XTEA was proposed in 1997 by David Wheeler and Roger "
        "Needham at the Cambridge Computer Laboratory. XTEA, like its predecessor "
        "TEA, relies on a Feistel network. This structure divides the 64-bit block "
        "into two 32-bit halves and processes them over multiple rounds. The "
        "algorithm uses simple operations such as addition, subtraction, bitwise XOR, "
        "and bitwise shifts. These operations are chosen to be fast and efficient on "
        "most modern hardware. The main idea behind XTEA is to achieve diffusion and "
        "confusion through repetitive, simple operations. The algorithm is simple to "
        "implement, making it ideal for environments with constraints on computational power. "
        "XTEA is often used in scenarios where resources are constrained, such as: Embedded "
        "systems, IoT devices and lightweight cryptography in software applications"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/XTEA>Wikipedia</a><br>"
        "<a href=https://asecuritysite.com/encryption/xtea>Asecuritysite</a>")

        self.setWindowTitle("XTEA block cipher (Extended Tiny Encryption Algorithm)")
        self.setFixedSize(700, 700)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(
            parent=self,
            placeholder_text="Plaintext must be 8 bytes or multiple of 8 bytes.")
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

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_xtea)
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

    def call_xtea(self):
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
            
        xtea = XTEAImp(key=key_bytes)
        ciphertext = xtea.encrypt(plaintext=plaintext_bytes)

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
