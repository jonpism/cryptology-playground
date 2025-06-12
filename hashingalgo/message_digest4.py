from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
import struct

class MD4:

    # MD4 Constants
    S = [3, 7, 11, 19, 3, 5, 9, 13, 3, 9, 11, 15]
    K = [0, 0x5A827999, 0x6ED9EBA1]

    def __init__(self, message):
        self.message = message

    def left_rotate(self, x, n):
        """Left rotate a 32-bit integer x by n bits."""
        return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

    def F(self, x, y, z):
        return (x & y) | (~x & z)

    def G(self, x, y, z):
        return (x & y) | (x & z) | (y & z)

    def H(self, x, y, z):
        return x ^ y ^ z

    def reset(self):
        """Reset the MD4 state variables."""
        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        self.buffer = b""
        self.count = 0

    def update(self, input_bytes):
        """Update the hash object with the bytes-like object."""
        input_len = len(input_bytes)
        self.count += input_len * 8
        self.buffer += input_bytes

        # Process each 64-byte (512-bit) block
        while len(self.buffer) >= 64:
            self._process_block(self.buffer[ : 64])
            self.buffer = self.buffer[64 : ]

    def _process_block(self, block):
        """Process a 64-byte (512-bit) block."""
        # Break block into sixteen 32-bit little-endian words
        X = list(struct.unpack("<16I", block))

        # Save state variables
        A, B, C, D = self.A, self.B, self.C, self.D

        # Round 1
        for i in range(16):
            if i % 4 == 0:
                A = self.left_rotate(A + self.F(B, C, D) + X[i], self.S[i % 4])
            elif i % 4 == 1:
                D = self.left_rotate(D + self.F(A, B, C) + X[i], self.S[i % 4])
            elif i % 4 == 2:
                C = self.left_rotate(C + self.F(D, A, B) + X[i], self.S[i % 4])
            else:
                B = self.left_rotate(B + self.F(C, D, A) + X[i], self.S[i % 4])

        # Round 2
        for i in range(16):
            if i % 4 == 0:
                A = self.left_rotate(A + self.G(B, C, D) + X[(i * 4) % 16] + self.K[1], self.S[4 + (i % 4)])
            elif i % 4 == 1:
                D = self.left_rotate(D + self.G(A, B, C) + X[(i * 4) % 16] + self.K[1], self.S[4 + (i % 4)])
            elif i % 4 == 2:
                C = self.left_rotate(C + self.G(D, A, B) + X[(i * 4) % 16] + self.K[1], self.S[4 + (i % 4)])
            else:
                B = self.left_rotate(B + self.G(C, D, A) + X[(i * 4) % 16] + self.K[1], self.S[4 + (i % 4)])

        # Round 3
        for i in range(16):
            if i % 4 == 0:
                A = self.left_rotate(A + self.H(B, C, D) + X[(i * 4) % 16] + self.K[2], self.S[8 + (i % 4)])
            elif i % 4 == 1:
                D = self.left_rotate(D + self.H(A, B, C) + X[(i * 4) % 16] + self.K[2], self.S[8 + (i % 4)])
            elif i % 4 == 2:
                C = self.left_rotate(C + self.H(D, A, B) + X[(i * 4) % 16] + self.K[2], self.S[8 + (i % 4)])
            else:
                B = self.left_rotate(B + self.H(C, D, A) + X[(i * 4) % 16] + self.K[2], self.S[8 + (i % 4)])

        # Update state variables
        self.A = (self.A + A) & 0xFFFFFFFF
        self.B = (self.B + B) & 0xFFFFFFFF
        self.C = (self.C + C) & 0xFFFFFFFF
        self.D = (self.D + D) & 0xFFFFFFFF

    def digest(self):
        """Return the digest of the data passed to the update method so far."""
        # Save the current state
        original_buffer = self.buffer
        original_count = self.count
        original_A = self.A
        original_B = self.B
        original_C = self.C
        original_D = self.D

        # Padding
        padding_length = (56 - (self.count // 8) % 64) % 64
        padding = b"\x80" + b"\x00" * (padding_length - 1)
        length = struct.pack("<Q", self.count)
        self.update(padding + length)

        # Produce the final hash
        digest = struct.pack("<4I", self.A, self.B, self.C, self.D)

        # Restore the original state
        self.buffer = original_buffer
        self.count = original_count
        self.A = original_A
        self.B = original_B
        self.C = original_C
        self.D = original_D

        return digest

    def hexdigest(self):
        """Return the digest as a string of hexadecimal digits."""
        return ''.join(f'{x:02x}' for x in self.digest())

class MD4Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About MD4"
        msgbox_txt = (
        "<p>MD4 (Message Digest Algorithm 4) is a cryptographic hash function developed by "
        "Ronald Rivest in 1990. It is designed to produce a 128-bit hash value and was one of the earliest "
        "widely adopted hash algorithms. MD4 laid the foundation for other hash functions such as MD5 and "
        "SHA algorithms.</p>"
        "<p><strong>Characteristics of MD4:</strong></p>"
        "<ul>"
        "<li>Produces a 128-bit hash value.</li>"
        "<li>Utilizes three rounds of computation for generating the hash value.</li>"
        "<li>Considered highly efficient but no longer secure for modern cryptographic needs.</li>"
        "<li>MD4 is vulnerable to collision attacks, meaning different input data can produce the same hash.</li>"
        "</ul>"
        "<p>MD4 was commonly used in applications such as digital signatures and password hashing, "
        "but due to its vulnerabilities, it is now considered obsolete for most security purposes. "
        "Modern systems have moved to more secure algorithms like SHA-256 or SHA-3.</p>"
        "<h3>Useful Links:</h3>"
        "<ul>"
        "<li><a href='https://en.wikipedia.org/wiki/MD4'>MD4 - Wikipedia</a></li>"
        "<li><a href='https://tools.ietf.org/html/rfc1320'>MD4 Specification (RFC 1320)</a></li>"
        "<li><a href='https://www.schneier.com/academic/archives/1993/04/the_md4_message_dige.html'>The MD4 Message Digest Algorithm - Analysis by Bruce Schneier</a></li>"
        "</ul>")

        self.setWindowTitle("Message Digest 4")
        self.setFixedSize(700, 400)

        # Text
        message_input_label = QLabel("Give message:", parent=self)
        message_input_label.setGeometry(300, 10, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_md4)
        submit_button.setGeometry(300, 160, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 220, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_md4(self):
        try:
            message = self.message_input.text()

            if not message:
                raise ValueError("Please enter a message")
            else:
                message_bytes = message.encode('utf-8')
                md4 = MD4(message=message)
                md4.reset()
                md4.update(message_bytes)
                hash_result = md4.hexdigest()

                self.result_label.clear()
                self.result_label.setHtml(f"<b>Result (Hex):</b><br>{str(hash_result)}")
                self.result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))