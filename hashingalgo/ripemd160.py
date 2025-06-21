from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from base64                         import b64encode
import struct

class RIPEMD160Hash:

    def __init__(self):
        self.h0 = 0x67452301
        self.h1 = 0xefcdab89
        self.h2 = 0x98badcfe
        self.h3 = 0x10325476
        self.h4 = 0xc3d2e1f0
        self.bytes_processed = 0
        self.buffer = b''

    def rotate_left(self, x, n):
        """Rotate x left by n bits."""
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    def f(self, j, x, y, z):
        """Non-linear functions F, G, H, I, J"""
        if 0 <= j <= 15:
            return x ^ y ^ z
        elif 16 <= j <= 31:
            return (x & y) | (~x & z)
        elif 32 <= j <= 47:
            return (x | ~y) ^ z
        elif 48 <= j <= 63:
            return (x & z) | (y & ~z)
        elif 64 <= j <= 79:
            return x ^ (y | ~z)

    def K(self, j):
        """Constants K"""
        if 0 <= j <= 15:
            return 0x00000000
        elif 16 <= j <= 31:
            return 0x5a827999
        elif 32 <= j <= 47:
            return 0x6ed9eba1
        elif 48 <= j <= 63:
            return 0x8f1bbcdc
        elif 64 <= j <= 79:
            return 0xa953fd4e

    def Kprime(self, j):
        """Constants K' (prime)"""
        if 0 <= j <= 15:
            return 0x50a28be6
        elif 16 <= j <= 31:
            return 0x5c4dd124
        elif 32 <= j <= 47:
            return 0x6d703ef3
        elif 48 <= j <= 63:
            return 0x7a6d76e9
        elif 64 <= j <= 79:
            return 0x00000000

    def R(self, j):
        """Left-rotation amounts"""
        r = [
            11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
            7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
            11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
            11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
            9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
        return r[j]

    def Rprime(self, j):
        """Left-rotation amounts for the prime variant"""
        rp = [
            8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
            9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
            9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
            15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
            8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
        return rp[j]

    def X(self, block, j):
        """Access the j-th word of the 512-bit message block"""
        return struct.unpack('<L', block[j * 4 : (j + 1) * 4])[0]

    def process_block(self, block):
        """Process one 512-bit block."""
        X = [self.X(block, i) for i in range(16)]
        
        # Initialize the 5 working variables
        A1, B1, C1, D1, E1 = self.h0, self.h1, self.h2, self.h3, self.h4
        A2, B2, C2, D2, E2 = self.h0, self.h1, self.h2, self.h3, self.h4

        # Main loop
        for j in range(80):
            T = (self.rotate_left(A1 + self.f(j, B1, C1, D1) + X[j % 16] + self.K(j), self.R(j)) + E1) & 0xFFFFFFFF
            A1, E1, D1, C1, B1 = T, A1, self.rotate_left(C1, 10), D1, C1

            T = (self.rotate_left(A2 + self.f(79 - j, B2, C2, D2) + X[j % 16] + self.Kprime(j), self.Rprime(j)) + E2) & 0xFFFFFFFF
            A2, E2, D2, C2, B2 = T, A2, self.rotate_left(C2, 10), D2, C2

        # Combine the two parallel chains
        T = (self.h1 + C1 + D2) & 0xFFFFFFFF
        self.h1 = (self.h2 + D1 + E2) & 0xFFFFFFFF
        self.h2 = (self.h3 + E1 + A2) & 0xFFFFFFFF
        self.h3 = (self.h4 + A1 + B2) & 0xFFFFFFFF
        self.h4 = (self.h0 + B1 + C2) & 0xFFFFFFFF
        self.h0 = T

    def update(self, data):
        """Add data to the buffer and process blocks."""
        self.bytes_processed += len(data)
        self.buffer += data

        while len(self.buffer) >= 64:
            self.process_block(self.buffer[ : 64])
            self.buffer = self.buffer[64 : ]

    def digest(self):
        """Return the final hash."""
        # Pad the data
        padding = b'\x80' + b'\x00' * ((55 - self.bytes_processed % 64) % 64)
        padded_data = self.buffer + padding + struct.pack('<Q', self.bytes_processed * 8)
        
        # Process any remaining blocks
        self.update(padded_data)

        # Return the final hash
        return struct.pack('<5L', self.h0, self.h1, self.h2, self.h3, self.h4)

    def hexdigest(self):
        """Return the final hash as a hex string."""
        return ''.join(f'{x:08x}' for x in struct.unpack('<5L', self.digest()))

class RIPEMD160Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About RIPEMD-160"
        msgbox_txt = (
            "<h2>About RIPEMD-160</h2>"
            "<p>RIPEMD-160 (RACE Integrity Primitives Evaluation Message Digest) is a cryptographic hash function "
            "developed in 1996 by Hans Dobbertin, Antoon Bosselaers, and Bart Preneel. It was designed as a stronger "
            "alternative to the original RIPEMD, which was based on the MD4 family of hash functions. RIPEMD-160 generates "
            "a 160-bit hash value and is known for its strong resistance to collision and pre-image attacks.</p>"
            "<p><strong>Characteristics of RIPEMD-160:</strong></p>"
            "<ul>"
            "<li>Produces a 160-bit hash value, typically represented as a 40-character hexadecimal string.</li>"
            "<li>Based on a design principle similar to MD4 and MD5 but with more robustness.</li>"
            "<li>Performs two parallel lines of computation to ensure enhanced security.</li>"
            "<li>RIPEMD-160 is slower compared to MD5 and SHA-1 but provides better security.</li>"
            "</ul>"
            "<p>RIPEMD-160 is primarily used in cryptographic applications where higher security is needed. While it has not "
            "been as widely adopted as SHA-256 or SHA-3, it remains a reliable option for applications that require a secure "
            "hash function. RIPEMD-160 has been successfully used in cryptocurrency protocols, such as Bitcoin, to generate "
            "public key hashes.</p>"
            "<p>Despite being secure, newer hash functions like SHA-256 are generally preferred today due to better overall "
            "support and integration in modern security systems.</p>"
            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/RIPEMD'>RIPEMD - Wikipedia</a></li>"
            "<li><a href='https://homes.esat.kuleuven.be/~bosselae/ripemd160/'>RIPEMD-160 Specification and Analysis</a></li>"
            "<li><a href='https://www.cryptographyworld.com/ripemd.htm'>Understanding RIPEMD-160 - Cryptography World</a></li>"
            "</ul>")

        self.setWindowTitle("RIPEMD-160")
        self.setFixedSize(700, 400)

        # Text
        message_input_label = QLabel("Give message:", parent=self)
        message_input_label.setGeometry(300, 10, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_ripemd)
        submit_button.setGeometry(300, 160, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 220, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_ripemd(self):
        try:
            message = self.message_input.text()
            if not message:
                raise ValueError("Please enter a message")
            else:
                message_bytes = message.encode('utf-8')
                ripemd = RIPEMD160Hash()
                ripemd.update(message_bytes)

                self.result_label.clear()
                self.result_label.setHtml(f"<b>Result (Base64):</b><br>{str(b64encode(ripemd.digest()).decode())}")
                self.result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))