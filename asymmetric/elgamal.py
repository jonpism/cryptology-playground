from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from binascii                       import hexlify
import base64, secrets, hashlib

# Implementation
class ElGamalImp:
    def __init__(self, bit_length=2048):
        """Initialize ElGamal instance, generate prime and generator."""
        self.bit_length = bit_length
        self.p = self.generate_large_prime()
        self.g = secrets.randbelow(self.p - 2) + 2  # Generator in range [2, p-2]

    def generate_large_prime(self):
        """Generate a large prime number of a specific bit length."""
        while True:
            prime_candidate = secrets.randbits(self.bit_length) | (1 << self.bit_length - 1) | 1
            if self.is_prime(prime_candidate):
                return prime_candidate

    def is_prime(self, num, k=128):
        """Miller-Rabin primality test for checking if a number is prime."""
        if num <= 1:
            return False
        if num == 2 or num == 3:
            return True
        if num % 2 == 0:
            return False
        
        r, d = 0, num - 1
        while d % 2 == 0:
            d //= 2
            r += 1

        for _ in range(k):
            a = secrets.randbelow(num - 3) + 2  # Random integer in [2, num-2]
            x = pow(a, d, num)
            if x == 1 or x == num - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, num)
                if x == num - 1:
                    break
            else:
                return False
        return True

    def generate_keys(self):
        """Generate public and private keys for the user."""
        x = secrets.randbelow(self.p - 2) + 1  # Private key
        y = pow(self.g, x, self.p)  # Public key y = g^x mod p
        return {'private_key': x, 'public_key': (self.p, self.g, y)}
    
    def encrypt(self, plaintext, public_key):
        """Encrypt the plaintext message using the receiver's public key."""
        p, g, y = public_key

        # Convert plaintext to integer
        plaintext_int = self.text_to_int(plaintext)
        if plaintext_int >= p:
            raise ValueError("Plaintext too large to encrypt. Use a larger key size or split message.")

        # Generate random session key k
        k = secrets.randbelow(p - 2) + 1

        # ElGamal encryption steps
        c1 = pow(g, k, p)
        s = pow(y, k, p)
        c2 = (plaintext_int * s) % p
        return c1, c2

    def decrypt(self, ciphertext, private_key):
        """Decrypt the ciphertext and return the plaintext string."""
        c1, c2 = ciphertext
        p = self.p
        x = private_key

        s = pow(c1, x, p)
        s_inv = pow(s, p - 2, p)  # modular inverse of s mod p
        plaintext_int = (c2 * s_inv) % p

        try:
            plaintext = self.int_to_text(plaintext_int)
        except UnicodeDecodeError:
            raise ValueError("Decryption failed: result is not valid UTF-8 text.")
        return plaintext

    def hash_message(self, message):
        """Hash the plaintext message using SHA-256."""
        sha256 = hashlib.sha256()
        sha256.update(message.encode('utf-8'))
        return sha256.hexdigest()

    def text_to_int(self, text):
        """Convert text (string) to an integer."""
        return int.from_bytes(text.encode('utf-8'), 'big')

    def int_to_text(self, number):
        """Convert an integer back to the original text (string)."""
        byte_length = (number.bit_length() + 7) // 8
        return number.to_bytes(byte_length, 'big').decode('utf-8')

# UI/WINDOW
class ElGamalWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About El Gamal"
        msgbox_txt = (
        "The El Gamal encryption algorithm is a public-key cryptosystem "
        "based on the Diffie-Hellman key exchange and is commonly used in  "
        "cryptographic applications that require asymmetric encryption. It "
        "offers both encryption and digital signature capabilities and is "
        "valued for its simplicity and efficiency, especially in contexts "
        "where key exchange security is critical. El Gamal relies on the "
        "difficulty of solving the Discrete Logarithm Problem (DLP), which "
        "makes it hard to determine the exponent in modular exponentiation. "
        "El Gamal’s security is rooted in the hardness of the discrete "
        "logarithm problem. Each message encrypted with a new random key "
        "results in a unique ciphertext, even for the same message, improving "
        "security against replay attacks. El Gamal is commonly used in cryptographic "
        "applications requiring digital signatures and is foundational to "
        "certain cryptosystems, including the Digital Signature Algorithm.<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/ElGamal_encryption>Wikipedia</a><br>"
        "<a href=https://www.geeksforgeeks.org/elgamal-encryption-algorithm>Geeks for Geeks</a>")

        self.setWindowTitle("El Gamal Encryption - Decryption")
        self.setFixedSize(1100, 700)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(170, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 480, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(70, 110, 120, 50)
        output_format_items = ['Base64', 'Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(70, 160, 120, 50)

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_elgamal_encryption)
        encrypt_button.setGeometry(250, 160, 100, 50)

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 270, 480, 100)
        self.ciphertext_label.setReadOnly(True)
        self.ciphertext_label.hide()

        self.private_key_label = QTextEdit(parent=self)
        self.private_key_label.setGeometry(10, 400, 480, 100)
        self.private_key_label.setReadOnly(True)
        self.private_key_label.hide()

        self.public_key_label = QTextEdit(parent=self)
        self.public_key_label.setGeometry(10, 510, 480, 100)
        self.public_key_label.setReadOnly(True)
        self.public_key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(1050, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        _label = QLabel(
            '|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n'
            '|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n', 
            parent=self)
        _label.setGeometry(550, 5, 20, 1000)

        # ciphertext
        ciphertext_label = QLabel("Enter ciphertext:", parent=self)
        ciphertext_label.setGeometry(750, 10, 100, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(600, 60, 480, 50)

        decrypt_button = DefaultButtonStyle("Decrypt", parent=self, command=self.call_elgamal_decryption)
        decrypt_button.setGeometry(750, 160, 100, 50)

        self.original_msg_label = QTextEdit(parent=self)
        self.original_msg_label.setGeometry(600, 270, 480, 100)
        self.original_msg_label.setReadOnly(True)
        self.original_msg_label.hide()
    
    def call_elgamal_decryption(self):
        try:
            ciphertext_str = self.ciphertext_input.text().strip()
            if not ciphertext_str:
                raise ValueError("Please enter the ciphertext.")

            output_format = self.output_format_options.currentText()

            if output_format == "Base64":
                c1_b64, c2_b64 = ciphertext_str.split(",")
                c1 = int.from_bytes(base64.b64decode(c1_b64), 'big')
                c2 = int.from_bytes(base64.b64decode(c2_b64), 'big')

            elif output_format == "Hex":
                c1_hex, c2_hex = ciphertext_str.split(",")
                c1 = int(c1_hex, 16)
                c2 = int(c2_hex, 16)

            else:  # Raw format expects direct int tuple string like "(123, 456)"
                if not ciphertext_str.startswith("(") or not ciphertext_str.endswith(")"):
                    raise ValueError("Invalid raw format. Expected tuple like (123, 456)")
                c1, c2 = eval(ciphertext_str)  # Unsafe in real apps! Acceptable only in trusted testing.

            decrypted_message = self.elgamal.decrypt((c1, c2), self.keys['private_key'])

            self.original_msg_label.setPlainText(f"Decrypted Message:\n{decrypted_message}")
            self.original_msg_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Decryption Error", str(e))
        
    def call_elgamal_encryption(self):
        try:
            plaintext = self.plaintext_input.text()
            if not plaintext:
                raise ValueError('Please enter a plaintext.')
            output_format = self.output_format_options.currentText()

            self.elgamal = ElGamalImp(bit_length=2048)
            self.keys = self.elgamal.generate_keys()
            public_key = self.keys['public_key']
            private_key = self.keys['private_key']
            ciphertext = self.elgamal.encrypt(plaintext=plaintext, public_key=self.keys['public_key'])

            c1, c2 = ciphertext

            if output_format == "Base64":
                c1_b64 = base64.b64encode(c1.to_bytes((c1.bit_length() + 7) // 8, byteorder='big')).decode('utf-8')
                c2_b64 = base64.b64encode(c2.to_bytes((c2.bit_length() + 7) // 8, byteorder='big')).decode('utf-8')
                ciphertext_b64 = f"{c1_b64},{c2_b64}"
                public_key_b64 = base64.b64encode(str(public_key).encode('utf-8')).decode('utf-8')
                private_key_b64 = base64.b64encode(str(private_key).encode('utf-8')).decode('utf-8')

            elif output_format == "Hex":
                c1_hex = hex(c1)[2:]
                c2_hex = hex(c2)[2:]
                ciphertext_hex = f"{c1_hex},{c2_hex}"
                public_key_hex = hexlify(str(public_key).encode('utf-8')).decode('utf-8')
                private_key_hex = hexlify(str(private_key).encode('utf-8')).decode('utf-8')

            self.ciphertext_label.clear()
            if output_format == "Base64":
                self.ciphertext_label.setHtml(f"<b>Ciphertext (Base64):</b><br>{ciphertext_b64}")
                self.private_key_label.setHtml(f"<b>Private key (Base64):</b><br>{private_key_b64}")
                self.public_key_label.setHtml(f"<b>Public key (Base64):</b><br>{public_key_b64}")
            elif output_format == "Hex":
                self.ciphertext_label.setHtml(f"<b>Ciphertext (Hex):</b><br>{ciphertext_hex}")
                self.private_key_label.setHtml(f"<b>Private key (Hex):</b><br>{private_key_hex}")
                self.public_key_label.setHtml(f"<b>Public key (Hex):</b><br>{public_key_hex}")
            else:
                self.ciphertext_label.setHtml(f"<b>Ciphertext (Raw):</b><br>{ciphertext}")
                self.private_key_label.setHtml(f"<b>Private key (Raw):</b><br>{private_key}")
                self.public_key_label.setHtml(f"<b>Public key (Raw):</b><br>{public_key}")

            self.ciphertext_label.show()
            self.private_key_label.show()
            self.public_key_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
