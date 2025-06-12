from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from binascii                       import hexlify
from os                             import urandom
import base64, struct

# Implementation
class XXTEAImp:

    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes long.")
        
        # Convert the key (16 bytes) into four 32-bit integers
        self.key = struct.unpack("4I", key)

    def encrypt(self, plaintext: bytes) -> bytes:
        if len(plaintext) == 0:
            return plaintext

        # Pad the plaintext to a multiple of 4 bytes (32 bits)
        padded_plaintext = plaintext.ljust((len(plaintext) + 3) // 4 * 4, b'\0')

        # Convert the plaintext into a list of 32-bit integers
        n = len(padded_plaintext) // 4
        v = list(struct.unpack(f"{n}I", padded_plaintext))  # Using 'I' for 32-bit unsigned int

        # Perform the XXTEA encryption
        self._xxtea_encrypt(v)

        # Convert the result back into bytes
        encrypted = struct.pack(f"{n}I", *v)
        return encrypted

    def decrypt(self, ciphertext: bytes) -> bytes:
        if len(ciphertext) == 0:
            return ciphertext

        # Convert the ciphertext into a list of 32-bit integers
        n = len(ciphertext) // 4
        v = list(struct.unpack(f"{n}L", ciphertext))

        # Perform the XXTEA decryption
        self._xxtea_decrypt(v)

        # Convert the result back into bytes and remove padding
        decrypted = struct.pack(f"{n}L", *v)
        return decrypted.rstrip(b'\0')

    def _xxtea_encrypt(self, v: list):
        n = len(v)
        if n < 2:
            return

        DELTA = 0x9e3779b9
        q = 6 + 52 // n
        sum = 0
        z = v[n - 1]
        while q > 0:
            q -= 1
            sum = (sum + DELTA) & 0xffffffff
            e = (sum >> 2) & 3
            for p in range(n - 1):
                y = v[p + 1]
                v[p] = (v[p] + self._mx(sum, y, z, p, e)) & 0xffffffff
                z = v[p]
            y = v[0]
            v[n - 1] = (v[n - 1] + self._mx(sum, y, z, n - 1, e)) & 0xffffffff
            z = v[n - 1]

    def _xxtea_decrypt(self, v: list):
        n = len(v)
        if n < 2:
            return

        DELTA = 0x9e3779b9
        q = 6 + 52 // n
        sum = (q * DELTA) & 0xffffffff
        y = v[0]
        while q > 0:
            q -= 1
            e = (sum >> 2) & 3
            for p in range(n - 1, 0, -1):
                z = v[p - 1]
                v[p] = (v[p] - self._mx(sum, y, z, p, e)) & 0xffffffff
                y = v[p]
            z = v[n - 1]
            v[0] = (v[0] - self._mx(sum, y, z, 0, e)) & 0xffffffff
            y = v[0]
            sum = (sum - DELTA) & 0xffffffff

    def _mx(self, sum, y, z, p, e):
        return (((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ ((sum ^ y) + (self.key[(p & 3) ^ e] ^ z))

class XXTEAWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About XXTEA"
        msgbox_txt = (
        "XXTEA, or 'Corrected Block TEA', is an improvement over the original"
        "Block TEA cipher. It was designed to provide a more secure and "
        "efficient algorithm for block encryption. Developed by David Wheeler "
        "and Roger Needham of the Computer Laboratory at the University of  "
        "Cambridge, XXTEA aims to fix security vulnerabilities found in the "
        "original Block TEA. XXTEA is a block cipher that operates on variable-sized "
        "data blocks. Unlike traditional block ciphers, which generally work on "
        "fixed-sized blocks (e.g., AES uses 128-bit blocks), XXTEA can encrypt "
        "and decrypt data of any block size larger than 64 bits. XXTEA is known for"
        " its simplicity. It uses simple operations like XOR, addition, and "
        "bitwise shifts. This makes it suitable for constrained environments, such "
        "as embedded systems or devices with limited computational power. XXTEA is "
        "well-suited for scenarios where lightweight encryption is needed: Microcontrollers "
        "IoT devices, and sensors"
        "<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/XXTEA>Wikipedia</a><br>"
        "<a href=https://crypto.stackexchange.com/questions/12993/in-what-way-is-xxtea-really-vulnerable>StackExchange</a><br>"
        "<a href=https://eprint.iacr.org/2010/254.pdf>Cryptology ePrint Archive</a>")

        self.setWindowTitle("XXTEA block cipher (Corrected Block TEA)")
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

        encrypt_button = DefaultButtonStyle("Encrypt", parent=self, command=self.call_xxtea)
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

    def call_xxtea(self):
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
            
        xxtea = XXTEAImp(key=key_bytes)
        ciphertext = xxtea.encrypt(plaintext=plaintext_bytes)

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
