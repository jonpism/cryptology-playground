from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from base64                         import b64encode
import hashlib
import hmac

class HMAC:
    def __init__(self, key: bytes, message: bytes, hash_func):
        """Initialize HMAC with a key, message, and a hash function."""
        self.key = key
        self.message = message
        self.hash_func = hash_func

    def compute(self) -> bytes:
        """Compute the HMAC value using the built-in hmac library."""
        hmac_obj = hmac.new(self.key, self.message, self.hash_func)
        return hmac_obj.digest()

    def hexdigest(self) -> str:
        """Return the HMAC result as a hexadecimal string."""
        hmac_obj = hmac.new(self.key, self.message, self.hash_func)
        return hmac_obj.hexdigest()

class HMACWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About HMAC"
        msgbox_txt = (
            "<p>HMAC (Hash-based Message Authentication Code) is a widely used cryptographic technique that provides message integrity and authenticity. "
            "It combines a cryptographic hash function (such as SHA-256 or MD5) with a secret key to generate a unique message authentication code. This "
            "code ensures that the message has not been tampered with and verifies the identity of the sender.</p>"
            "<p>HMAC is commonly used in network security protocols, such as TLS, IPsec, and in API authentication mechanisms, where it helps protect against "
            "man-in-the-middle attacks and message alteration.</p>"
            "<p><strong>How HMAC Works:</strong></p>"
            "<ol>"
            "<li>The message to be authenticated is combined with a secret key using a hashing algorithm (like SHA-256 or SHA-512).</li>"
            "<li>HMAC applies the hashing function twice: once to a modified version of the message combined with the key (inner hash), and then again "
            "to another modified version of the key combined with the result of the inner hash (outer hash).</li>"
            "<li>The final output is the HMAC value, which is used as a signature to authenticate the message.</li>"
            "</ol>"
            "<p><strong>Characteristics of HMAC:</strong></p>"
            "<ul>"
            "<li><strong>Message Integrity:</strong> HMAC ensures that the message has not been modified during transmission. If any part of the message changes, "
            "the HMAC value will also change, allowing the recipient to detect tampering.</li>"
            "<li><strong>Message Authenticity:</strong> Because HMAC uses a secret key, only those who have the key can generate a valid HMAC. This provides assurance "
            "of the sender's authenticity.</li>"
            "<li><strong>Resilience to Cryptographic Attacks:</strong> HMAC is designed to be secure even when the underlying hash function has some vulnerabilities. "
            "The use of a secret key adds an additional layer of protection.</li>"
            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/HMAC'>HMAC - Wikipedia</a></li>"
            "<li><a href='https://tools.ietf.org/html/rfc2104'>RFC 2104 - HMAC: Keyed-Hashing for Message Authentication</a></li>"
            "<li><a href='https://cryptography.io/en/latest/hazmat/primitives/mac/hmac/'>Cryptography.io - HMAC Implementation Guide</a></li>"
            "</ul>")

        self.setWindowTitle("HMAC (Hash-based Message Authentication Code)")
        self.setFixedSize(700, 800)

        # Message input
        message_label = QLabel("Give message:", parent=self)
        message_label.setGeometry(300, 10, 100, 50)
        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        # Key input
        key_input_label = QLabel("Give key:", parent=self)
        key_input_label.setGeometry(300, 130, 250, 50)
        self.key_input = DefaultQLineEditStyle(parent=self)
        self.key_input.setGeometry(10, 180, 680, 50)

        # Hash Algorithm
        hashalgo_label = QLabel("Hash Algorithm:", parent=self)
        hashalgo_label.setGeometry(10, 280, 120, 50)
        self.hashalgo_options = DefaultQComboBoxStyle(parent=self, items=['sha1', 'sha224', 'sha384', 'sha512'])
        self.hashalgo_options.setGeometry(130, 280, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_hmac)
        submit_button.setGeometry(400, 280, 100, 50)

        self.digest_label = QTextEdit(parent=self)
        self.digest_label.setGeometry(10, 380, 680, 100)
        self.digest_label.setReadOnly(True)
        self.digest_label.hide()

        self.hex_digest_label = QTextEdit(parent=self)
        self.hex_digest_label.setGeometry(10, 490, 680, 100)
        self.hex_digest_label.setReadOnly(True)
        self.hex_digest_label.hide()

        self.b64_digest_label = QTextEdit(parent=self)
        self.b64_digest_label.setGeometry(10, 600, 680, 100)
        self.b64_digest_label.setReadOnly(True)
        self.b64_digest_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 750, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_hmac(self):
        try:
            if self.message_input.text():
                msg = self.message_input.text()
                if self.key_input.text():
                    key = self.key_input.text()
                    hashalgo = self.hashalgo_options.currentText()

                    msg_bytes = msg.encode('utf-8')
                    key_bytes = key.encode('utf-8')

                    if hashalgo == 'sha1':
                        hmac_instance = HMAC(key=key_bytes, message=msg_bytes, hash_func=hashlib.sha1)
                    elif hashalgo == 'sha224':
                        hmac_instance = HMAC(key=key_bytes, message=msg_bytes, hash_func=hashlib.sha224)
                    elif hashalgo == 'sha384':
                        hmac_instance = HMAC(key=key_bytes, message=msg_bytes, hash_func=hashlib.sha384)
                    else:
                        hmac_instance = HMAC(key=key_bytes, message=msg_bytes, hash_func=hashlib.sha512)

                    digest = hmac_instance.compute()
                    self.digest_label.clear()
                    self.digest_label.setHtml(f"<b>Digest (Raw):</b><br>{str(digest)}")
                    self.digest_label.show()

                    hex_digest = hmac_instance.hexdigest()
                    self.hex_digest_label.clear()
                    self.hex_digest_label.setHtml(f"<b>Digest (Hex):</b><br>{str(hex_digest)}")
                    self.hex_digest_label.show()

                    b64_digest = b64encode(digest).decode('utf-8')
                    self.b64_digest_label.clear()
                    self.b64_digest_label.setHtml(f"<b>Digest (Base64):</b><br>{str(b64_digest)}")
                    self.b64_digest_label.show()
                else:
                    raise ValueError('Please enter a key.')
            else:
                raise ValueError('Please enter a message.')
        
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
