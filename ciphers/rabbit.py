from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from binascii                       import hexlify
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
import struct, base64, os

# Implementation
class RabbitStreamCipherImp:

    def __init__(self, key):
        # Initial state variables (X, A, G)
        self.X = [0] * 8
        self.A = [0] * 8
        self.G = [0] * 8
        self.C = [0] * 8
        self.Carry = 0
        self.key_setup(key)

    def _rotate_left(self, x, bits, size=32):
        """Left rotation of `x` by `bits` in a word of `size` bits."""
        return ((x << bits) & ((1 << size) - 1)) | (x >> (size - bits))

    def key_setup(self, key):
        """Sets up the key and initializes internal state."""
        key = struct.unpack("<LLLL", key)
        for i in range(4):
            self.X[i] = key[i]
            self.X[i + 4] = key[(i + 1) % 4]
            self.A[i] = key[(i + 3) % 4]
            self.A[i + 4] = key[i]

        self.C = [(self.A[i] ^ self.X[(i + 3) % 8]) for i in range(8)]
        self.Carry = 0
        self.cycle()
        self.cycle()

    def cycle(self):
        """Performs one full cycle of the Rabbit cipher's state update function."""
        for i in range(8):
            self.C[i] = (self.C[i] + self.A[i] + self.Carry) & 0xFFFFFFFF
            self.Carry = (self.C[i] < self.A[i] + self.Carry)

        for i in range(8):
            self.G[i] = (self.X[i] + self.C[i]) & 0xFFFFFFFF
            self.G[i] = (self.G[i] * self.G[i]) & 0xFFFFFFFF
            self.G[i] ^= self.G[i] >> 16

        self.X[0] = (self.G[0] + self._rotate_left(self.G[7], 16) + self._rotate_left(self.G[6], 16)) & 0xFFFFFFFF
        self.X[1] = (self.G[1] + self._rotate_left(self.G[0], 8) + self.G[7]) & 0xFFFFFFFF
        self.X[2] = (self.G[2] + self._rotate_left(self.G[1], 16) + self.G[0]) & 0xFFFFFFFF
        self.X[3] = (self.G[3] + self._rotate_left(self.G[2], 8) + self.G[1]) & 0xFFFFFFFF
        self.X[4] = (self.G[4] + self._rotate_left(self.G[3], 16) + self._rotate_left(self.G[2], 16)) & 0xFFFFFFFF
        self.X[5] = (self.G[5] + self._rotate_left(self.G[4], 8) + self.G[3]) & 0xFFFFFFFF
        self.X[6] = (self.G[6] + self._rotate_left(self.G[5], 16) + self.G[4]) & 0xFFFFFFFF
        self.X[7] = (self.G[7] + self._rotate_left(self.G[6], 8) + self.G[5]) & 0xFFFFFFFF

    def generate_keystream_block(self):
        """Generates a 128-bit block of keystream."""
        self.cycle()
        keystream = [0] * 8
        keystream[0] = (self.X[0] ^ (self.X[5] >> 16) ^ (self.X[3] << 16)) & 0xFFFFFFFF
        keystream[1] = (self.X[2] ^ (self.X[7] >> 16) ^ (self.X[5] << 16)) & 0xFFFFFFFF
        keystream[2] = (self.X[4] ^ (self.X[1] >> 16) ^ (self.X[7] << 16)) & 0xFFFFFFFF
        keystream[3] = (self.X[6] ^ (self.X[3] >> 16) ^ (self.X[1] << 16)) & 0xFFFFFFFF
        # Ensure all values are within the 32-bit unsigned integer range
        return struct.pack("<LLLL", *[k & 0xFFFFFFFF for k in keystream[:4]])

    def encrypt(self, plaintext):
        """Encrypts or decrypts the plaintext by XORing with the keystream."""
        ciphertext = bytearray(plaintext)
        for i in range(0, len(ciphertext), 16):
            keystream_block = self.generate_keystream_block()
            for j in range(16):
                if i + j < len(ciphertext):
                    ciphertext[i + j] ^= keystream_block[j]
        return bytes(ciphertext)


class RabbitStreamCipherWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Rabbit"
        msgbox_txt = (
        "The Rabbit stream cipher is a high-speed symmetric encryption algorithm developed "
        "in 2003 by Martin Boesgaard, Mette Vesterager, Thomas Pedersen, Jesper Christiansen, "
        "and Ove Scavenius at Cryptico A/S. Rabbit was designed for efficiency on both software "
        "and hardware platforms, making it suitable for constrained environments like embedded systems, "
        "and was optimized specifically for fast encryption in software. Rabbit is based on a "
        "pseudorandom number generator (PRNG) that uses a combination of bitwise and arithmetic "
        "operations to generate a keystream. <br> "
        "Rabbit was selected for the eSTREAM project, a European Union effort to identify secure "
        "and efficient stream ciphers, where it was in the final portfolio for software applications. "
        "Due to its high speed and low computational overhead, Rabbit is used in applications "
        "requiring fast, lightweight encryption, such as mobile devices, embedded systems, and other "
        "resource-limited environments. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Rabbit_(cipher)>Wikipedia</a><br>"
        "<a href=https://eprint.iacr.org/2004/291.pdf>CRYPTICO A/S</a>")

        self.setWindowTitle("Rabbit Stream Cipher")
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
            max_length=16,
            placeholder_text="Key must be 16 bytes.")
        self.key_input.setGeometry(10, 160, 320, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(150, 210, 120, 50)
        output_format_items = ['Base64', 'Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(150, 260, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_rabbit)
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
        
    def call_rabbit(self):
        plaintext = self.plaintext_input.text()
        plaintext_bytes = plaintext.encode('utf-8')
        key = self.key_input.text()
        output_format = self.output_format_options.currentText()

        if key == "":
            key_bytes = os.urandom(16)
        else:
            if len(key) == 16:
                key_bytes = key.encode('utf-8')
            else:
                raise ValueError("Give Key with 16 bytes")

        rabbit = RabbitStreamCipherImp(key=key_bytes)
        ciphertext = rabbit.encrypt(plaintext=plaintext_bytes)

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

'''
# Decrypt back to plaintext
decrypted = cipher.encrypt(ciphertext)  # XORing twice with the keystream decrypts
print("Decrypted:", decrypted)
'''