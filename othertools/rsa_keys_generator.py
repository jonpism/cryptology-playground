from PyQt6.QtWidgets                            import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style             import DefaultQComboBoxStyle
from cryptography.hazmat.primitives.asymmetric  import rsa
from cryptography.hazmat.primitives             import serialization
from cryptography.hazmat.backends               import default_backend
from binascii                                   import hexlify
from base64                                     import b64encode, b64decode
from pathlib                                    import Path

downloads_path = Path.home() / "Downloads" / "generated_rsa_keys"

class RSA_Key_Generator:

    def __init__(self, key_size=None, encoding=None):
        
        self.key_size = key_size
        self.private_key = None
        self.public_key = None

        if encoding == "PEM":
            self.encoding = serialization.Encoding.PEM
        else:
            self.encoding = serialization.Encoding.DER

    def generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = self.key_size,
            backend = default_backend())
        self.public_key = self.private_key.public_key()

    def get_private_key_pem(self):
        if self.private_key:
            return self.private_key.private_bytes(
                encoding = self.encoding,
                format = serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm = serialization.NoEncryption())
        else:
            raise ValueError("Keys have not been generated yet!")

    def get_public_key_pem(self):
        if self.public_key:
            return self.public_key.public_bytes(
                encoding = self.encoding,
                format = serialization.PublicFormat.SubjectPublicKeyInfo)
        else:
            raise ValueError("Keys have not been generated yet!")
    
    def save_private_key_to_file(self, filepath):
        if not self.private_key:
            raise ValueError("Private key not generated yet!")
        with open(filepath, "wb") as f:
            f.write(self.get_private_key_pem())

    def save_public_key_to_file(self, filepath):
        if not self.public_key:
            raise ValueError("Public key not generated yet!")
        with open(filepath, "wb") as f:
            f.write(self.get_public_key_pem())


class RSAKeyGenWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About RSA Key Generator"
        msgbox_txt = (
            "<p>The RSA Key Generator is a tool that creates a pair of cryptographic keys using the RSA algorithm. RSA, which stands for Rivest-Shamir-Adleman, "
            "is one of the first and most widely used public-key cryptosystems. It is widely used in secure data transmission, especially in establishing secure connections over the internet.</p>"
            "<p><strong>Key Components of RSA:</strong></p>"
            "<ul>"
            "<li><strong>Private Key:</strong> A secret key used for decrypting data that was encrypted with the corresponding public key. The private key should be kept secure and never shared.</li>"
            "<li><strong>Public Key:</strong> A key used for encrypting data that can only be decrypted by the corresponding private key. The public key can be freely shared with anyone.</li>"
            "</ul>"
            "<p>The key size, which is usually 2048 bits or higher, determines the strength of the encryption. Larger key sizes provide higher security but result in slower performance. "
            "For most applications, 2048-bit keys are considered secure, though 4096-bit keys are sometimes used for even greater security.</p>"
            "<p><strong>Security Considerations:</strong></p>"
            "<ul>"
            "<li><strong>Key Size:</strong> The security of RSA depends on the key size. Keys shorter than 2048 bits are considered weak and vulnerable to attacks.</li>"
            "<li><strong>Cryptographic Attacks:</strong> RSA is vulnerable to attacks if improperly implemented, such as timing attacks, padding oracle attacks, and factorization attacks on weak keys.</li>"
            "</ul>"
            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://en.wikipedia.org/wiki/RSA_(cryptosystem)'>RSA (Cryptosystem) - Wikipedia</a></li>"
            "<li><a href='https://cryptography.io/en/latest/'>Python Cryptography Library</a></li>"
            "<li><a href='https://www.openssl.org/'>OpenSSL Project</a></li>"
            "</ul>")

        self.setWindowTitle("RSA Keys Generator")
        self.setFixedSize(700, 500)

        # Key size
        key_size_options_label = QLabel("Select key size:", parent=self)
        key_size_options_label.setGeometry(50, 10, 200, 50)
        self.key_size_options = DefaultQComboBoxStyle(
            parent=self, items=["2048", "3072", "4096"])
        self.key_size_options.setGeometry(50, 60, 130, 50)

        # Encoding options
        encoding_label = QLabel("Select encoding:", parent=self)
        encoding_label.setGeometry(250, 10, 140, 50)
        self.encoding_options = DefaultQComboBoxStyle(
            parent=self,
            items=["PEM", "DER"])
        self.encoding_options.setGeometry(250, 60, 130, 50)

        generate_button = DefaultButtonStyle("Generate", parent=self, bold=True, command=self.generate)
        generate_button.setGeometry(450, 60, 100, 50)

        self.prv_key_label = QTextEdit(parent=self)
        self.prv_key_label.setGeometry(10, 220, 680, 50)
        self.prv_key_label.setReadOnly(True)
        self.prv_key_label.hide()

        self.pbl_key_label = QTextEdit(parent=self)
        self.pbl_key_label.setGeometry(10, 320, 680, 50)
        self.pbl_key_label.setReadOnly(True)
        self.pbl_key_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def generate(self):
        try:
            key_size = int(self.key_size_options.currentText())
            encoding = self.encoding_options.currentText()

            object = RSA_Key_Generator(key_size=key_size, encoding=encoding)
            object.generate_keys()

            private_key_path = downloads_path / "private_key.pem" if encoding == "PEM" else downloads_path / "private_key.der"
            public_key_path = downloads_path / "public_key.pem" if encoding == "PEM" else downloads_path / "public_key.der"

            downloads_path.mkdir(parents=True, exist_ok=True)

            object.save_private_key_to_file(private_key_path)
            object.save_public_key_to_file(public_key_path)
            QMessageBox.information(
                self, 'Success', f'Keys successfully generated and saved at: {downloads_path}')

            if encoding == "PEM":
                    self.prv_key_label.clear()
                    self.prv_key_label.setHtml(f"<b>Private key (PEM) location:</b><br>{private_key_path}")
                    self.prv_key_label.show()
                    self.pbl_key_label.clear()
                    self.pbl_key_label.setHtml(f"<b>Public key (PEM) location:</b><br>{public_key_path}")
                    self.pbl_key_label.show()
            else:  # DER
                    self.prv_key_label.clear()
                    self.prv_key_label.setHtml(f"<b>Private key (DER) location:</b><br>{private_key_path}")
                    self.prv_key_label.show()
                    self.pbl_key_label.clear()
                    self.pbl_key_label.setHtml(f"<b>Public key (DER) location:</b><br>{public_key_path}")
                    self.pbl_key_label.show()

        except ValueError as ve:
            QMessageBox.warning(self , 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def convert_pem_to_hex(self, pem_data):
        # Decode bytes to a string
        pem_str = pem_data.decode('utf-8')
    
        # Remove the PEM headers and footers
        pem_body = pem_str.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "")
        pem_body = pem_body.replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "")
        pem_body = pem_body.strip()
    
        # Ensure correct padding for Base64 decoding
        def add_padding(base64_string):
            return base64_string + '=' * ((4 - len(base64_string) % 4) % 4)
    
        # Add padding if necessary and decode the Base64 content
        pem_body_padded = add_padding(pem_body)
        der_data = b64decode(pem_body_padded)
    
        # Convert the binary DER data to hex
        hex_data = hexlify(der_data).decode('utf-8')
    
        return hex_data
