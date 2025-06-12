from PyQt6.QtWidgets                    import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QTextEdit
from Crypto.Random                      import get_random_bytes
from binascii                           import hexlify
from random                             import randint
from DefaultStyles.button_style         import DefaultButtonStyle
from DefaultStyles.qcombo_box_style     import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style     import DefaultQLineEditStyle
import base64

# Implementation
class RC5_EncryptionImp:

    def __init__(self, key, word_size=16, rounds=12):
        self.word_size = word_size
        self.rounds = rounds
        self.modulo = 2 ** word_size
        self.key_size = len(key)
        self.S = []  # Key schedule array
        self.P = 0xB7E15163  # Magic constant P for word size of 32 bits
        self.Q = 0x9E3779B9  # Magic constant Q for word size of 32 bits
        self.key_expansion(key)

    def _rotate_left(self, x, y):
        """Performs cyclic left rotation on x by y bits"""
        return ((x << y) & (self.modulo - 1)) | (x >> (self.word_size - y))

    def _rotate_right(self, x, y):
        """Performs cyclic right rotation on x by y bits"""
        return (x >> y) | ((x << (self.word_size - y)) & (self.modulo - 1))

    def key_expansion(self, key):
        # Calculate the number of words L should hold
        u = self.word_size // 8  # Bytes per word (for word_size = 16, u = 2)
        c = max(1, (self.key_size + u - 1) // u)  # Number of key bytes divided by word size in bytes
        L = [0] * c

        # Convert key to words
        for i in range(self.key_size - 1, -1, -1):
            L[i // u] = (L[i // u] << 8) + key[i]

        # Initialize S array
        self.S = [self.P]
        for i in range(1, 2 * (self.rounds + 1)):
            self.S.append((self.S[i - 1] + self.Q) % self.modulo)

        # Mix the key
        i = j = A = B = 0
        for _ in range(3 * max(len(L), len(self.S))):
            A = self.S[i] = self._rotate_left((self.S[i] + A + B) % self.modulo, 3)
            B = L[j] = self._rotate_left((L[j] + A + B) % self.modulo, (A + B) % self.word_size)
            i = (i + 1) % len(self.S)
            j = (j + 1) % len(L)


    def encrypt(self, plaintext):
        # Convert plaintext into two halves
        A = plaintext[0]
        B = plaintext[1]

        # Initial key whitening
        A = (A + self.S[0]) % self.modulo
        B = (B + self.S[1]) % self.modulo

        # Rounds of encryption
        for i in range(1, self.rounds + 1):
            A = (self._rotate_left((A ^ B), B % self.word_size) + self.S[2 * i]) % self.modulo
            B = (self._rotate_left((B ^ A), A % self.word_size) + self.S[2 * i + 1]) % self.modulo

        return A, B

    def decrypt(self, ciphertext):
        # Convert ciphertext into two halves
        A = ciphertext[0]
        B = ciphertext[1]

        # Rounds of decryption
        for i in range(self.rounds, 0, -1):
            B = self._rotate_right((B - self.S[2 * i + 1]) % self.modulo, A % self.word_size) ^ A
            A = self._rotate_right((A - self.S[2 * i]) % self.modulo, B % self.word_size) ^ B

        # Final key whitening
        B = (B - self.S[1]) % self.modulo
        A = (A - self.S[0]) % self.modulo

        return A, B

    def divide_to_16bit_words(self, plaintext_bytes):
        # Ensure that the plaintext is at least 4 bytes (2 * 16 bits)
        if len(plaintext_bytes) < 4:
            # Pad with zeros if too short
            plaintext_bytes = plaintext_bytes.ljust(4, b'\x00')
        else:
            # Trim to exactly 4 bytes if it's longer (adjust according to your needs)
            plaintext_bytes = plaintext_bytes[:4]

        # Randomly split the 4 bytes into two halves
        split_point = randint(1, 3)  # Split between 1st and 3rd byte
        part1 = plaintext_bytes[ : split_point]
        part2 = plaintext_bytes[split_point : ]

        # Convert to two 16-bit integers (if smaller, pad with 0s)
        word1 = int.from_bytes(part1.ljust(2, b'\x00'), byteorder = 'big')
        word2 = int.from_bytes(part2.ljust(2, b'\x00'), byteorder = 'big')

        return word1, word2

'''
# Encrypt a plaintext block (as two 16-bit words)
plaintext = (0x1234, 0x5678)
ciphertext = rc5.encrypt(plaintext)
print("Ciphertext:", ciphertext)

# Decrypt the ciphertext
decrypted = rc5.decrypt(ciphertext)
print("Decrypted:", decrypted)
'''

class RC5EncryptionWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RC5 Encryption")
        self.setFixedSize(700, 800)

        # Plaintext
        plaintext_label = QLabel("Give plaintext:", parent=self)
        plaintext_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        # Key
        key_label = QLabel("Give key: (Generates a random if none given)", parent=self)
        key_label.setGeometry(250, 110, 500, 50)
        self.key_input = DefaultQLineEditStyle(
            parent=self,
            max_length=255,
            placeholder_text="Key must be from 0 to 255 bytes (16 bytes suggested).")
        self.key_input.setGeometry(10, 160, 680, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(300, 210, 120, 50)
        output_format_items = ['Base64', 'Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(300, 260, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_rc5_encryption)
        encrypt_button.setGeometry(300, 330, 100, 50)

        self.encrypted_text_label = QTextEdit(parent=self)
        self.encrypted_text_label.setGeometry(10, 380, 680, 100)
        self.encrypted_text_label.setReadOnly(True)
        self.encrypted_text_label.hide()

        self.key_label = QTextEdit(parent=self)
        self.key_label.setGeometry(10, 530, 680, 50)
        self.key_label.setReadOnly(True)
        self.key_label.hide()

    def call_rc5_encryption(self):
        plaintext = self.plaintext_input.text()
        plaintext_bytes = plaintext.encode('utf-8')
        key = self.key_input.text()
        key_bytes = key.encode('utf-8')
        output_format = self.output_format_options.currentText()

        if key == "":
            key = get_random_bytes(16)
            
            rc5 = RC5_EncryptionImp(key=key)
            word1, word2 = rc5.divide_to_16bit_words(plaintext_bytes)
            plaintext_divided = (word1, word2)
            ciphertext = rc5.encrypt(plaintext=plaintext_divided)

            self.key_label.clear()
            self.key_label.setHtml(f"<b>Random key:</b><br>{str(key)}")
        else:
            rc5 = RC5_EncryptionImp(key=key_bytes)
            word1, word2 = rc5.divide_to_16bit_words(plaintext_bytes)
            plaintext_divided = (word1, word2)
            ciphertext = rc5.encrypt(plaintext=plaintext_divided)

            self.key_label.clear()
            self.key_label.setHtml(f"<b>Key:</b><br>{str(key)}")
        
        ciphertext_bytes = ciphertext[0].to_bytes(2, byteorder='big') + ciphertext[1].to_bytes(2, byteorder='big')
        if output_format == "Base64":
            ciphertext = base64.b64encode(ciphertext_bytes).decode('utf-8')
        elif output_format == "Hex":
            ciphertext = hexlify(ciphertext_bytes).decode('utf-8')

        self.encrypted_text_label.clear()
        self.encrypted_text_label.setHtml(f"<b>Encrypted text:</b><br>{str(ciphertext)}")
        self.encrypted_text_label.show()

        self.key_label.show()





class RC5DecryptionWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RC5 Decryption")
        self.setGeometry(150, 150, 200, 150)

        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Hello from the new window!"))
        self.setLayout(layout)