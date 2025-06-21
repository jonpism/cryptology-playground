from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from base64                         import b64encode
import hashlib

class AboutSHA(QWidget):

    def __init__(self, about_title, about_text, ax, ay, aw, ah, theme_mode):
        super().__init__()

        self.about_title = about_title
        self.about_text = about_text
        self.theme_mode = theme_mode

        self.setup_about_button(ax, ay, aw, ah)

    def setup_about_button(self, ax, ay, aw, ah):
        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=self.about_text, title=self.about_title, geometry=(ax, ay, aw, ah))
        self.aboutButton.update_theme(self.theme_mode)

# ================================================================================================================

class SHA1:
    def __init__(self):
        # Initialize a new SHA1 hash object using hashlib
        self.hasher = hashlib.sha1()

    def update(self, message):
        """Update the hash object with the bytes-like object."""
        if not isinstance(message, (bytes, bytearray)):
            raise TypeError("Input must be bytes or bytearray")
        self.hasher.update(message)

    def digest(self):
        """Return the digest of the data passed to the update method so far."""
        return self.hasher.digest()

    def hexdigest(self):
        """Return the hex digest of the data."""
        return self.hasher.hexdigest()

    def copy(self):
        """Return a copy of the hash object."""
        new_sha1 = SHA1()
        new_sha1.hasher = self.hasher.copy()
        return new_sha1

    @classmethod
    def sha1(cls, message):
        """Convenience method for one-time SHA1 computation."""
        try:
            if not isinstance(message, (bytes, bytearray)):
                raise TypeError("Input must be bytes or bytearray")
            return hashlib.sha1(message).hexdigest()
        except TypeError as te:
            QMessageBox.warning('Error', str(te))

class SHA1Window(AboutSHA):

    def __init__(self, theme_mode):
        about_title = "About SHA-1"
        about_text = (
        "<p>SHA-1 (Secure Hash Algorithm 1) is a cryptographic hash function developed by the National Security Agency (NSA) "
        "and published by the National Institute of Standards and Technology (NIST) in 1995. It was designed to produce a "
        "160-bit hash value, which is often represented as a 40-character hexadecimal number. SHA-1 was widely used in security "
        "protocols, such as SSL/TLS and digital signatures, for ensuring data integrity.</p>"
        "<p><strong>Characteristics of SHA-1:</strong></p>"
        "<ul>"
        "<li>Generates a 160-bit hash value.</li>"
        "<li>Uses a series of bitwise operations, modular additions, and compression functions to process input data.</li>"
        "<li>Designed as part of the Digital Signature Algorithm (DSA) suite in the Digital Signature Standard (DSS).</li>"
        "<li>Faster than many older hash functions but compromised in terms of security.</li>"
        "</ul>"
        "<p><strong>Security Concerns:</strong></p>"
        "<p>SHA-1 has significant security weaknesses and is susceptible to collision attacks, where two different inputs "
        "produce the same hash value. In 2017, a successful collision attack on SHA-1 was demonstrated by Google and CWI "
        "Amsterdam, further emphasizing the algorithm's vulnerability. Because of this, SHA-1 is considered deprecated and "
        "unsuitable for secure cryptographic applications.</p>"
        "<p>SHA-1 has been replaced by more secure hash functions, such as SHA-256 and SHA-3, in most security-related applications. "
        "Despite its vulnerabilities, SHA-1 may still be used for legacy systems or applications where security is not a primary concern.</p>"
        "<h3>Useful Links:</h3>"
        "<ul>"
        "<li><a href='https://en.wikipedia.org/wiki/SHA-1'>SHA-1 - Wikipedia</a></li>"
        "<li><a href='https://www.schneier.com/blog/archives/2017/02/sha-1_collision.html'>SHA-1 Collision Attack - Schneier on Security</a></li>"
        "<li><a href='https://shattered.io/'>SHAttered: SHA-1 Collision Attack Details</a></li>"
        "</ul>")
        
        ax, ay, aw, ah = 650, 650, 50, 50
        super().__init__(about_title, about_text, ax, ay, aw, ah, theme_mode)

        self.setWindowTitle("SHA-1")
        self.setFixedSize(700, 700)

        # Text
        message_input_label = QLabel("Give message:", parent=self)
        message_input_label.setGeometry(300, 10, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_sha1)
        submit_button.setGeometry(300, 160, 100, 50)

        self.b64_result_label = QTextEdit(parent=self)
        self.b64_result_label.setGeometry(10, 230, 680, 100)
        self.b64_result_label.setReadOnly(True)
        self.b64_result_label.hide()

        self.hexdigest_label = QTextEdit(parent=self)
        self.hexdigest_label.setGeometry(10, 380, 680, 100)
        self.hexdigest_label.setReadOnly(True)
        self.hexdigest_label.hide()

        self.rawdigest_label = QTextEdit(parent=self)
        self.rawdigest_label.setGeometry(10, 500, 680, 100)
        self.rawdigest_label.setReadOnly(True)
        self.rawdigest_label.hide()

    def call_sha1(self):
        try:
            message = self.message_input.text()
            if not message:
                raise ValueError("Please enter a message")
            else:
                message_bytes = message.encode('utf-8')
                h = SHA1()
                h.update(message=message_bytes)

                # Hexadecimal digest
                hexdigest = h.hexdigest()

                # Raw digest
                rawdigest = h.digest()

                self.b64_result_label.clear()
                self.b64_result_label.setHtml(f"<b>Base64 digest:</b><br>{str(b64encode(rawdigest).decode())}")
                self.b64_result_label.show()

                self.hexdigest_label.clear()
                self.hexdigest_label.setHtml(f"<b>Hex digest:</b><br>{str(hexdigest)}")
                self.hexdigest_label.show()

                self.rawdigest_label.clear()
                self.rawdigest_label.setHtml(f"<b>Raw digest:</b><br>{str(rawdigest)}")
                self.rawdigest_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

# ==========================================================================================================================

# https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf

class SHA256:
    def __init__(self):
        # Initialize a new SHA256 hash object using hashlib
        self._hasher = hashlib.sha256()

    def update(self, message):
        """Update the hash object with the bytes-like object."""
        if not isinstance(message, (bytes, bytearray)):
            raise TypeError("Input must be bytes or bytearray")
        self._hasher.update(message)

    def digest(self):
        """Return the digest of the data passed to the update method so far."""
        return self._hasher.digest()

    def hexdigest(self):
        """Return the hex digest of the data."""
        return self._hasher.hexdigest()

    def copy(self):
        """Return a copy of the hash object."""
        new_sha256 = SHA256()
        new_sha256._hasher = self._hasher.copy()
        return new_sha256

    @classmethod
    def sha256(cls, message):
        """Convenience method for one-time SHA256 computation."""
        if not isinstance(message, (bytes, bytearray)):
            raise TypeError("Input must be bytes or bytearray")
        return hashlib.sha256(message).hexdigest()


class SHA256Window(AboutSHA):

    def __init__(self, theme_mode):
        about_title = "About SHA-256"
        about_text = (
        "<p>SHA-256 (Secure Hash Algorithm 256-bit) is part of the SHA-2 family of cryptographic hash functions, "
        "which were designed by the National Security Agency (NSA) and published by the National Institute of Standards "
        "and Technology (NIST) in 2001. SHA-256 generates a 256-bit (32-byte) hash value, commonly represented as a "
        "64-character hexadecimal string. It is widely used in a variety of security applications and protocols, including "
        "TLS/SSL, digital certificates, and cryptocurrency mining.</p>"
        "<p><strong>Characteristics of SHA-256:</strong></p>"
        "<ul>"
        "<li>Produces a 256-bit hash value, offering a higher level of security compared to earlier algorithms like SHA-1.</li>"
        "<li>Uses 64 rounds of computation, involving bitwise operations, modular additions, and compression functions.</li>"
        "<li>Highly resistant to collision and pre-image attacks, making it suitable for secure data hashing.</li>"
        "<li>Efficient in terms of performance while providing strong cryptographic security.</li>"
        "</ul>"
        "<p>SHA-256 is a crucial component of many modern security protocols. It is used extensively in blockchain technology, "
        "where it provides the cryptographic foundation for data integrity and the mining process in cryptocurrencies like Bitcoin. "
        "It is also used in password hashing (with added salts for security) and digital signatures.</p>"
        "<p>Despite the robustness of SHA-256, cryptographic researchers continue to advance the development of hash functions, "
        "and more secure algorithms like SHA-3 have been introduced. Nevertheless, SHA-256 remains one of the most trusted and "
        "commonly used cryptographic hash functions in the world today.</p>"
        "<h3>Useful Links:</h3>"
        "<ul>"
        "<li><a href='https://en.wikipedia.org/wiki/SHA-2'>SHA-2 - Wikipedia</a></li>"
        "<li><a href='https://csrc.nist.gov/publications/detail/fips/180/4/final'>SHA-256 Specification (NIST FIPS 180-4)</a></li>"
        "<li><a href='https://bitcoin.org/en/how-it-works#hash-functions'>How SHA-256 Works in Bitcoin - Bitcoin.org</a></li>"
        "</ul>")
        
        ax, ay, aw, ah = 650, 650, 50, 50
        super().__init__(about_title, about_text, ax, ay, aw, ah, theme_mode)

        self.setWindowTitle("SHA-256")
        self.setFixedSize(700, 700)

        # Text
        message_input_label = QLabel("Give message:", parent=self)
        message_input_label.setGeometry(300, 10, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_sha256)
        submit_button.setGeometry(300, 160, 100, 50)

        self.b64_result_label = QTextEdit(parent=self)
        self.b64_result_label.setGeometry(10, 230, 680, 100)
        self.b64_result_label.setReadOnly(True)
        self.b64_result_label.hide()

        self.hexdigest_label = QTextEdit(parent=self)
        self.hexdigest_label.setGeometry(10, 380, 680, 100)
        self.hexdigest_label.setReadOnly(True)
        self.hexdigest_label.hide()

        self.rawdigest_label = QTextEdit(parent=self)
        self.rawdigest_label.setGeometry(10, 500, 680, 100)
        self.rawdigest_label.setReadOnly(True)
        self.rawdigest_label.hide()

    def call_sha256(self):
        try:
            message = self.message_input.text()
            if not message:
                raise ValueError("Please enter a message")
            else:
                message_bytes = message.encode('utf-8')
                h = SHA256()
                h.update(message=message_bytes)

                # Hexadecimal digest
                hexdigest = h.hexdigest()

                # Raw digest
                rawdigest = h.digest()

                self.b64_result_label.clear()
                self.b64_result_label.setHtml(f"<b>Base64 digest:</b><br>{str(b64encode(rawdigest).decode())}")
                self.b64_result_label.show()

                self.hexdigest_label.clear()
                self.hexdigest_label.setHtml(f"<b>Hex digest:</b><br>{str(hexdigest)}")
                self.hexdigest_label.show()

                self.rawdigest_label.clear()
                self.rawdigest_label.setHtml(f"<b>Raw digest:</b><br>{str(rawdigest)}")
                self.rawdigest_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
# ==========================================================================================================================

class SHA384:
    def __init__(self):
        # Initialize a new SHA384 hash object using hashlib
        self._hasher = hashlib.sha384()

    def update(self, message):
        """Update the hash object with the bytes-like object."""
        if not isinstance(message, (bytes, bytearray)):
            raise TypeError("Input must be bytes or bytearray")
        self._hasher.update(message)

    def digest(self):
        """Return the digest of the data passed to the update method so far."""
        return self._hasher.digest()

    def hexdigest(self):
        """Return the hex digest of the data."""
        return self._hasher.hexdigest()

    def copy(self):
        """Return a copy of the hash object."""
        new_sha384 = SHA384()
        new_sha384._hasher = self._hasher.copy()
        return new_sha384

    @classmethod
    def sha384(cls, message):
        """Convenience method for one-time SHA384 computation."""
        if not isinstance(message, (bytes, bytearray)):
            raise TypeError("Input must be bytes or bytearray")
        return hashlib.sha384(message).hexdigest()

    
class SHA384Window(AboutSHA):

    def __init__(self, theme_mode):
        about_title = "About SHA-384"
        about_text = (
        "<p>SHA-384 (Secure Hash Algorithm 384-bit) is part of the SHA-2 family of cryptographic hash functions, "
        "which were developed by the National Security Agency (NSA) and published by the National Institute of Standards "
        "and Technology (NIST). SHA-384 generates a 384-bit (48-byte) hash value, typically represented as a 96-character "
        "hexadecimal string. It offers a higher level of security than SHA-256 and is used in various applications where "
        "strong cryptographic security is required.</p>"
        "<p><strong>Characteristics of SHA-384:</strong></p>"
        "<ul>"
        "<li>Produces a 384-bit hash value, making it more secure against collision and brute-force attacks compared to SHA-256.</li>"
        "<li>Based on the SHA-512 algorithm, but with a truncated output and a different initial hash value.</li>"
        "<li>Uses 80 rounds of computation, involving bitwise operations, modular additions, and message scheduling.</li>"
        "<li>Efficient for use in applications that require robust security without significantly impacting performance.</li>"
        "</ul>"
        "<p>SHA-384 is commonly used in digital certificates, SSL/TLS protocols, and in environments where stronger security is "
        "needed compared to SHA-256. It is suitable for applications that demand high levels of integrity and resistance to attacks.</p>"
        "<p>While SHA-384 is considered very secure, it is important to follow best practices in cryptography and ensure that it "
        "is implemented correctly in any security-sensitive application. For the highest level of future-proofing, some systems are "
        "beginning to explore newer hash functions, like those in the SHA-3 family.</p>"
        "<h3>Useful Links:</h3>"
        "<ul>"
        "<li><a href='https://en.wikipedia.org/wiki/SHA-2'>SHA-2 - Wikipedia</a></li>"
        "</ul>")
        
        ax, ay, aw, ah = 650, 650, 50, 50
        super().__init__(about_title, about_text, ax, ay, aw, ah, theme_mode)

        self.setWindowTitle("SHA-384")
        self.setFixedSize(700, 700)

        # Text
        message_input_label = QLabel("Give message:", parent=self)
        message_input_label.setGeometry(300, 10, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_sha384)
        submit_button.setGeometry(300, 160, 100, 50)

        self.b64_result_label = QTextEdit(parent=self)
        self.b64_result_label.setGeometry(10, 230, 680, 100)
        self.b64_result_label.setReadOnly(True)
        self.b64_result_label.hide()

        self.hexdigest_label = QTextEdit(parent=self)
        self.hexdigest_label.setGeometry(10, 380, 680, 100)
        self.hexdigest_label.setReadOnly(True)
        self.hexdigest_label.hide()

        self.rawdigest_label = QTextEdit(parent=self)
        self.rawdigest_label.setGeometry(10, 500, 680, 100)
        self.rawdigest_label.setReadOnly(True)
        self.rawdigest_label.hide()

    def call_sha384(self):
        try:
            message = self.message_input.text()
            if not message:
                raise ValueError("Please enter a message")
            else:
                message_bytes = message.encode('utf-8')
                h = SHA384()
                h.update(message=message_bytes)

                # Hexadecimal digest
                hexdigest = h.hexdigest()

                # Raw digest
                rawdigest = h.digest()

                self.b64_result_label.clear()
                self.b64_result_label.setHtml(f"<b>Base64 digest:</b><br>{str(b64encode(rawdigest).decode())}")
                self.b64_result_label.show()

                self.hexdigest_label.clear()
                self.hexdigest_label.setHtml(f"<b>Hex digest:</b><br>{str(hexdigest)}")
                self.hexdigest_label.show()

                self.rawdigest_label.clear()
                self.rawdigest_label.setHtml(f"<b>Raw digest:</b><br>{str(rawdigest)}")
                self.rawdigest_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

# ==========================================================================================================================

class SHA512:
    def __init__(self):
        # Initialize a new SHA512 hash object using hashlib
        self._hasher = hashlib.sha512()

    def update(self, message):
        """Update the hash object with the bytes-like object."""
        if not isinstance(message, (bytes, bytearray)):
            raise TypeError("Input must be bytes or bytearray")
        self._hasher.update(message)

    def digest(self):
        """Return the digest of the data passed to the update method so far."""
        return self._hasher.digest()

    def hexdigest(self):
        """Return the hex digest of the data."""
        return self._hasher.hexdigest()

    def copy(self):
        """Return a copy of the hash object."""
        new_sha512 = SHA512()
        new_sha512._hasher = self._hasher.copy()
        return new_sha512

    @classmethod
    def sha512(cls, message):
        """Convenience method for one-time SHA512 computation."""
        if not isinstance(message, (bytes, bytearray)):
            raise TypeError("Input must be bytes or bytearray")
        return hashlib.sha512(message).hexdigest()


class SHA512Window(AboutSHA):

    def __init__(self, theme_mode):
        about_title = "About SHA-512"
        about_text = (
        "<p>SHA-512 (Secure Hash Algorithm 512-bit) is part of the SHA-2 family of cryptographic hash functions, "
        "developed by the National Security Agency (NSA) and published by the National Institute of Standards and Technology "
        "(NIST). SHA-512 generates a 512-bit (64-byte) hash value, typically represented as a 128-character hexadecimal string. "
        "It is widely used in various cryptographic applications requiring high levels of security.</p>"
        "<p><strong>Characteristics of SHA-512:</strong></p>"
        "<ul>"
        "<li>Produces a 512-bit hash value, offering a higher level of security than SHA-256 and SHA-384.</li>"
        "<li>Uses 80 rounds of computation and a 1024-bit message block size, providing a robust defense against collision and pre-image attacks.</li>"
        "<li>SHA-512 is based on the same design principles as SHA-256 and SHA-384 but processes data in larger chunks, resulting in a larger output.</li>"
        "<li>Because of its larger output, it is more computationally intensive than SHA-256, but it provides stronger cryptographic guarantees.</li>"
        "</ul>"
        "<p>SHA-512 is typically used in situations where a higher level of security is required. It is commonly employed in digital signatures, "
        "certificate generation, blockchain applications, and cryptographic protocols like SSL/TLS. The large hash output also makes it "
        "useful for applications that require very low risk of collision or vulnerability to brute-force attacks.</p>"
        "<p>While SHA-512 provides robust security, it is often more computationally expensive than other hash functions like SHA-256. "
        "However, with the increasing computational power of modern systems, SHA-512 continues to be a secure and trusted choice for high-security applications.</p>"
        "<h3>Useful Links:</h3>"
        "<ul>"
        "<li><a href='https://en.wikipedia.org/wiki/SHA-2'>SHA-2 - Wikipedia</a></li>"
        "</ul>")
        
        ax, ay, aw, ah = 650, 650, 50, 50
        super().__init__(about_title, about_text, ax, ay, aw, ah, theme_mode)

        self.setWindowTitle("SHA-512")
        self.setFixedSize(700, 700)

        # Text
        message_input_label = QLabel("Give message:", parent=self)
        message_input_label.setGeometry(300, 10, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_sha512)
        submit_button.setGeometry(300, 160, 100, 50)

        self.b64_result_label = QTextEdit(parent=self)
        self.b64_result_label.setGeometry(10, 230, 680, 100)
        self.b64_result_label.setReadOnly(True)
        self.b64_result_label.hide()

        self.hexdigest_label = QTextEdit(parent=self)
        self.hexdigest_label.setGeometry(10, 380, 680, 100)
        self.hexdigest_label.setReadOnly(True)
        self.hexdigest_label.hide()

        self.rawdigest_label = QTextEdit(parent=self)
        self.rawdigest_label.setGeometry(10, 500, 680, 100)
        self.rawdigest_label.setReadOnly(True)
        self.rawdigest_label.hide()

    def call_sha512(self):
        try:
            message = self.message_input.text()
            if not message:
                raise ValueError("Please enter a message")
            else:
                message_bytes = message.encode('utf-8')
                h = SHA512()
                h.update(message=message_bytes)
    
                # Hexadecimal digest
                hexdigest = h.hexdigest()
    
                # Raw digest
                rawdigest = h.digest()
    
                self.b64_result_label.clear()
                self.b64_result_label.setHtml(f"<b>Base64 digest:</b><br>{str(b64encode(rawdigest).decode())}")
                self.b64_result_label.show()
    
                self.hexdigest_label.clear()
                self.hexdigest_label.setHtml(f"<b>Hex digest:</b><br>{str(hexdigest)}")
                self.hexdigest_label.show()
    
                self.rawdigest_label.clear()
                self.rawdigest_label.setHtml(f"<b>Raw digest:</b><br>{str(rawdigest)}")
                self.rawdigest_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
            
# =====================================================================================================================
