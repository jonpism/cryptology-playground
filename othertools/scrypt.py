from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from base64                         import b64encode
import hashlib, os

def scrypt_kdf(password: str, salt: bytes = None, n: int = 2**14, r: int = 8, p: int = 1, dk_len: int = 64) -> bytes:
    """Derives a key from a password using the scrypt key derivation function.

    :param password: The password to derive the key from.
    :param salt: The salt to use. If None, a random salt is generated.
    :param n: CPU/memory cost factor. Must be a power of 2.
    :param r: Block size parameter.
    :param p: Parallelization factor.
    :param dk_len: Length of the derived key in bytes.
    :return: The derived key as bytes."""
    if salt is None:
        salt = os.urandom(16)  # Generate a random 16-byte salt if not provided

    # n, r, and p meet the required constraints
    assert n > 1 and (n & (n - 1)) == 0, "n must be > 1 and a power of 2."
    assert r > 0 and p > 0, "r and p must be greater than 0."
    assert len(salt) > 0, "Salt must be non-empty."

    # hashlib's scrypt function to derive the key
    derived_key = hashlib.scrypt(password.encode(), salt=salt, n=n, r=r, p=p, maxmem=0, dklen=dk_len)

    return salt, derived_key

class ScryptWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About scrypt"
        msgbox_txt = (
            "<p><strong>scrypt</strong> is a key derivation function designed to be computationally expensive and memory-intensive, making it highly resistant "
            "to brute-force attacks and specialized hardware attacks (such as those using GPUs, FPGAs, or ASICs). It was specifically developed to secure "
            "passwords by making it costly for attackers to attempt password guessing, even with substantial computational resources.</p>"

            "<p><strong>How scrypt Works:</strong></p>"
            "<ul>"
            "<li><strong>Password:</strong> The input password that needs to be securely stored or transmitted.</li>"
            "<li><strong>Salt:</strong> A unique, random value added to the password to prevent dictionary attacks and rainbow table attacks.</li>"
            "<li><strong>Cost Parameters:</strong> scrypt uses three main cost parameters:</li>"
            "<ul>"
            "<li><strong>N (CPU/memory cost factor):</strong> Determines the computational cost. It must be a power of 2. Higher values make scrypt more secure but slower.</li>"
            "<li><strong>r (block size):</strong> Controls the memory usage. Increasing <em>r</em> increases memory requirements linearly.</li>"
            "<li><strong>p (parallelization factor):</strong> Controls the parallelism. It allows scrypt to run in parallel and can be adjusted based on the system’s available resources.</li>"
            "</ul>"
            "</ul>"

            "<p><strong>Common Use Cases:</strong></p>"
            "<ul>"
            "<li><strong>Password Hashing:</strong> scrypt is widely used for securely hashing and storing passwords, as it is more resistant to attacks than traditional "
            "hashing algorithms like MD5 or SHA-1.</li>"
            "<li><strong>Key Derivation:</strong> scrypt can be used to derive cryptographic keys from passwords, making it suitable for encrypting sensitive data.</li>"
            "</ul>"

            "<p><strong>Security Considerations:</strong></p>"
            "<ul>"
            "<li><strong>Parameter Selection:</strong> Choosing appropriate values for <em>N</em>, <em>r</em>, and <em>p</em> is crucial for ensuring security. "
            "Higher values make the function more secure but also more resource-intensive.</li>"
            "<li><strong>Implementation:</strong> Use well-tested and reviewed libraries for implementing scrypt to avoid potential vulnerabilities.</li>"
            "</ul>"

            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/Scrypt'>scrypt - Wikipedia</a></li>"
            "<li><a href='https://www.tarsnap.com/scrypt/scrypt.pdf'>Original scrypt Paper</a></li>"
            "<li><a href='https://cryptography.io/en/latest/'>Python Cryptography Library</a></li>"
            "</ul>")

        self.setWindowTitle("Scrypt")
        self.setFixedSize(700, 800)

        # Password input
        pwd_label = QLabel("Enter password:", parent=self)
        pwd_label.setGeometry(300, 10, 120, 50)
        self.pwd_input = DefaultQLineEditStyle(parent=self)
        self.pwd_input.setGeometry(10, 60, 680, 50)

        # Salt input
        salt_label = QLabel("Enter salt:\nGenerates a random if none given.", parent=self)
        salt_label.setGeometry(10, 110, 240, 50)
        self.salt_input = DefaultQLineEditStyle(
            parent=self,
            max_length=16,
            placeholder_text="16 bytes long.")
        self.salt_input.setGeometry(10, 160, 180, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.scrypt_kd)
        submit_button.setGeometry(300, 160, 100, 50)

        self.base64_label = QTextEdit(parent=self)
        self.base64_label.setGeometry(10, 280, 680, 100)
        self.base64_label.setReadOnly(True)
        self.base64_label.hide()

        self.hexdigest_label = QTextEdit(parent=self)
        self.hexdigest_label.setGeometry(10, 400, 680, 100)
        self.hexdigest_label.setReadOnly(True)
        self.hexdigest_label.hide()

        self.rawdigest_label = QTextEdit(parent=self)
        self.rawdigest_label.setGeometry(10, 520, 680, 100)
        self.rawdigest_label.setReadOnly(True)
        self.rawdigest_label.hide()

        self.salt_label = QTextEdit(parent=self)
        self.salt_label.setGeometry(10, 640, 680, 100)
        self.salt_label.setReadOnly(True)
        self.salt_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 750, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def scrypt_kd(self):
        try:
            if self.pwd_input.text():
                password = self.pwd_input.text()

                if self.salt_input.text():
                    salt = self.salt_input.text().encode('utf-8')
                    _, derived_key = scrypt_kdf(password, salt)
                else:
                    salt, derived_key = scrypt_kdf(password)

                self.base64_label.clear()
                self.base64_label.setHtml(f"<b>Result (Base64):</b><br>{str(b64encode(derived_key).decode())}")
                self.base64_label.show()

                self.hexdigest_label.clear()
                self.hexdigest_label.setHtml(f"<b>Result (Hex):</b><br>{str(derived_key.hex())}")
                self.hexdigest_label.show()

                self.rawdigest_label.clear()
                self.rawdigest_label.setHtml(f"<b>Result (Raw):</b><br>{str(derived_key)}")
                self.rawdigest_label.show()

                self.salt_label.clear()
                self.salt_label.setHtml(f"<b>Salt (Raw):</b><br>{str(salt)}")
                self.salt_label.show()
            else:
                raise ValueError('Please enter password.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))