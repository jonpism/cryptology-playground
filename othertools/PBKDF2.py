import hashlib, hmac, os, base64
from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from binascii                       import hexlify

# Implementation
class PBKDF2Imp:
    def __init__(self, password: str, salt: bytes, iterations: int, dklen: int, hash_name: str):
        """Initialize the PBKDF2 key derivation function.

        :param password: The password from which to derive the key.
        :param salt: The salt to use. If None, a random salt will be generated.
        :param iterations: number of iterations to perform (default is 100000).
        :param dklen: desired length of the derived key in bytes (default is 32).
        :param hash_name: hash function to use ('sha256', 'sha1', etc.)."""
        self.password = password.encode('utf-8')  # Convert password to bytes
        self.salt = salt if salt else os.urandom(16)  # Generate random salt if none is provided
        self.iterations = iterations
        self.dklen = dklen
        self.hash_name = hash_name

    def derive_key(self) -> bytes:
        """Derive a cryptographic key from the password using PBKDF2.
            
        :return: The derived key as bytes."""
        return hashlib.pbkdf2_hmac(
            self.hash_name,
            self.password,
            self.salt,
            self.iterations,
            self.dklen)

    def verify_password(self, derived_key: bytes) -> bool:
        """
        Verify if a derived key matches the password.

        :param derived_key: The key that needs to be verified.
        :return: True if the derived key matches the password, False otherwise.
        """
        new_key = self.derive_key()
        return hmac.compare_digest(new_key, derived_key)

    def get_salt(self) -> bytes:
        """Retrieve the salt used for key derivation.

        :return: The salt as bytes."""
        return self.salt


class PBKDF2Window(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About PBKDF2"
        msgbox_txt = (
            "<p>PBKDF2 (Password-Based Key Derivation Function 2) is a cryptographic function used to derive a secure encryption key from a password. "
            "It is designed to make brute-force attacks and dictionary attacks more difficult by introducing computational cost to the process of generating keys. "
            "PBKDF2 is widely used for secure password storage and in key derivation for various encryption protocols.</p>"
            "<p><strong>How PBKDF2 Works:</strong></p>"
            "<ol>"
            "<li>The user provides a password, which is combined with a unique random salt value to protect against rainbow table attacks.</li>"
            "<li>The function repeatedly applies a pseudorandom function (typically HMAC with a cryptographic hash like SHA-256) to the password and salt "
            "for a specified number of iterations. Each iteration increases the computational cost, making it more difficult for an attacker to guess the password.</li>"
            "<li>The final output is a derived key, which can be used for securely encrypting data or for other cryptographic purposes.</li>"
            "</ol>"
            "<p><strong>Applications of PBKDF2:</strong></p>"
            "<ul>"
            "<li><strong>Password Hashing:</strong> PBKDF2 is commonly used to hash and securely store passwords in databases. By using a high iteration count and a unique salt "
            "for each password, it becomes more difficult for attackers to crack hashed passwords.</li>"
            "<li><strong>Key Derivation:</strong> PBKDF2 is used to derive encryption keys from passwords in secure communication protocols and storage encryption systems. "
            "This allows for a password to be transformed into a strong cryptographic key suitable for use in encryption algorithms.</li>"
            "</ul>"
            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/PBKDF2'>PBKDF2 - Wikipedia</a></li>"
            "<li><a href='https://www.rfc-editor.org/info/rfc2898'>RFC 2898 - PKCS #5: Password-Based Cryptography Specification</a></li>"
            "<li><a href='https://cryptography.io/en/latest/hazmat/primitives/kdf/pbkdf2/'>PBKDF2 Implementation Guide - Cryptography.io</a></li>"
            "</ul>")

        self.setWindowTitle("Password Based Key Derivation Function 2")
        self.setFixedSize(700, 800)

        # Password input
        pwd_input_label = QLabel("Give Password:", parent=self)
        pwd_input_label.setGeometry(300, 10, 100, 50)
        self.pwd_input = DefaultQLineEditStyle(parent=self)
        self.pwd_input.setGeometry(10, 60, 680, 50)

        # Salt input
        salt_input_label = QLabel("Give Salt (16 bytes suggested):", parent=self)
        salt_input_label.setGeometry(300, 120, 250, 50)
        self.salt_input = DefaultQLineEditStyle(
            parent=self,
            placeholder_text="Generates a random salt if none is given")
        self.salt_input.setGeometry(10, 180, 680, 50)

        # Hash Algorithm
        hash_algo_label = QLabel("Hash Algorithm:", parent=self)
        hash_algo_label.setGeometry(10, 240, 120, 50)
        hash_aglorithms = ['sha1', 'sha256', 'sha512']
        self.hashalgo_options = DefaultQComboBoxStyle(parent=self, items=hash_aglorithms)
        self.hashalgo_options.setGeometry(10, 290, 120, 50)

        # Iterations
        iterations_input_label = QLabel("Give iterations (rounds):", parent=self)
        iterations_input_label.setGeometry(200, 240, 200, 50)
        self.iterations_input = DefaultQLineEditStyle(
            parent=self,
            placeholder_text="Default=100000",
            int_validator=True)
        self.iterations_input.setGeometry(200, 290, 130, 50)

        # Output format
        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(450, 240, 120, 50)
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=['Base64', 'Hex', 'Raw'])
        self.output_format_options.setGeometry(450, 290, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_pbkdf2)
        submit_button.setGeometry(300, 360, 100, 50)

        self.derived_key_label = QTextEdit(parent=self)
        self.derived_key_label.setGeometry(10, 410, 680, 100)
        self.derived_key_label.setReadOnly(True)
        self.derived_key_label.hide()

        self.salt_label = QTextEdit(parent=self)
        self.salt_label.setGeometry(10, 510, 680, 100)
        self.salt_label.setReadOnly(True)
        self.salt_label.hide()

        self.verified_label = QTextEdit(parent=self)
        self.verified_label.setGeometry(10, 610, 680, 100)
        self.verified_label.setReadOnly(True)
        self.verified_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 750, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_pbkdf2(self):
        try:
            password = self.pwd_input.text()
            if not password:
                raise ValueError("Please give password")
            hashalgo = self.hashalgo_options.currentText()
            salt = self.salt_input.text()
            iterations = self.iterations_input.text()
            output_format = self.output_format_options.currentText()

            salt_bytes = None
            if salt:
                salt_bytes = salt.encode('utf-8')

            iterations = int(iterations) if iterations.isdigit() else 100000

            pbkdf2 = PBKDF2Imp(password=password, salt=salt_bytes, iterations=iterations, dklen=32, hash_name=hashalgo)

            # Derive a key:
            derived_key = pbkdf2.derive_key()
            is_verified = pbkdf2.verify_password(derived_key=derived_key)

            if output_format == "Base64":
                self.derived_key_label.clear()
                self.derived_key_label.setHtml(
                    f"<b>Derived key (Base64):</b><br>{str(base64.b64encode(derived_key).decode('utf-8'))}")
                self.derived_key_label.show()
            elif output_format == "Hex":
                self.derived_key_label.clear()
                self.derived_key_label.setHtml(
                    f"<b>Derived key (Hex):</b><br>{str(hexlify(derived_key).decode('utf-8'))}")
                self.derived_key_label.show()
            else:
                self.derived_key_label.clear()
                self.derived_key_label.setHtml(f"<b>Derived key (Raw):</b><br>{str(derived_key)}")
                self.derived_key_label.show()

            if salt:
                self.salt_label.clear()
                self.salt_label.setHtml(f"<b>Salt:</b><br>{str(salt)}")
                self.salt_label.show()
            else:
                self.salt_label.clear()
                self.salt_label.setHtml(f"<b>Random Salt:</b><br>{str(pbkdf2.get_salt())}")
                self.salt_label.show()

            self.verified_label.clear()
            self.verified_label.setHtml(f"<b>Is verified:</b><br>{str(is_verified)}")
            self.verified_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
