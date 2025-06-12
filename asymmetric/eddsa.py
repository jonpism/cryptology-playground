from PyQt6.QtWidgets                            import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style             import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style             import DefaultQLineEditStyle
from cryptography.hazmat.primitives             import serialization
from cryptography.exceptions                    import InvalidSignature
from base64                                     import b64encode
from binascii                                   import hexlify
from cryptography.hazmat.primitives.asymmetric  import ed25519

class EdDSA:

    def __init__(self):
        # Generate a private key for Ed25519
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        # Derive the corresponding public key
        self.public_key = self.private_key.public_key()

    def sign(self, message: bytes) -> bytes:
        """
        Sign a message with the Ed25519 private key.
        
        :param message: The message to sign as bytes.
        :return: The signature as bytes.
        """
        return self.private_key.sign(message)

    def verify(self, message: bytes, signature: bytes) -> bool:
        """
        Verify a signature for a given message using the Ed25519 public key.
        
        :param message: The original message as bytes.
        :param signature: The signature to verify as bytes.
        :return: True if the signature is valid, False otherwise.
        """
        try:
            self.public_key.verify(signature, message)
            return True
        except InvalidSignature:
            return False
        
    def get_private_key(self, password: bytes = None) -> bytes:
        """
        Get the private key in PEM format, optionally encrypted with a password.
        
        :param password: Password to encrypt the private key (optional).
        :return: The private key in PEM format as bytes.
        """
        encryption = (serialization.BestAvailableEncryption(password) if password else serialization.NoEncryption())
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption,)

    def get_public_key(self) -> bytes:
        """
        Get the public key in PEM format.
        
        :return: The public key in PEM format as bytes.
        """
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,)

    def save_private_key(self, filepath: str, password: bytes = None):
        """
        Save the private key to a file, optionally encrypted with a password.
        
        :param filepath: Path to save the private key.
        :param password: Password to encrypt the key file (optional).
        """
        encryption = (serialization.BestAvailableEncryption(password) if password else serialization.NoEncryption())
        with open(filepath, "wb") as key_file:
            key_file.write(
                self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=encryption,))

    def load_private_key(self, filepath: str, password: bytes = None):
        """
        Load the private key from a file.
        
        :param filepath: Path to the private key file.
        :param password: Password to decrypt the key file if it is encrypted (optional).
        """
        with open(filepath, "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(), password=password)
        # Derive the corresponding public key after loading the private key
        self.public_key = self.private_key.public_key()

    def save_public_key(self, filepath: str):
        """
        Save the public key to a file.
        :param filepath: Path to save the public key.
        """
        with open(filepath, "wb") as key_file:
            key_file.write(
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,))

    def load_public_key(self, filepath: str):
        """
        Load the public key from a file.
        :param filepath: Path to the public key file.
        """
        with open(filepath, "rb") as key_file:
            self.public_key = serialization.load_pem_public_key(key_file.read())


class EdDSAWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Edwards-curve Digital Signature Algorithm"
        msgbox_txt = (
        "EdDSA is a modern, efficient digital signature algorithm that's usually implemented "
        "over the Ed25519 curve, which is a specific case of an Edwards curve. This curve "
        "is known for its security and speed, particularly in applications requiring "
        "high-performance cryptography. EdDSA is especially popular in secure communication "
        "applications, such as SSH and TLS, and is often used in blockchain technology "
        "due to its speed and reduced complexity. Ed25519 has become a popular key type for SSH, "
        "offering a faster, more secure alternative to traditional RSA and ECDSA keys.<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/EdDSA>Wikipedia</a><br>"
        "<a href=https://cryptobook.nakov.com/digital-signatures/eddsa-and-ed25519>Practical Cryptography for Developers</a>")

        self.setWindowTitle("Edwards-curve Digital Signature Algorithm (EdDSA)")
        self.setFixedSize(700, 680)

        # Message input
        msg_label = QLabel("Enter message:", parent=self)
        msg_label.setGeometry(300, 10, 100, 50)
        self.msg_input = DefaultQLineEditStyle(parent=self)
        self.msg_input.setGeometry(10, 60, 680, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(10, 130, 120, 50)
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=['Base64', 'Hex', 'Raw'])
        self.output_format_options.setGeometry(130, 130, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_eddsa)
        submit_button.setGeometry(330, 130, 100, 50)

        self.private_key_label = QTextEdit(parent=self)
        self.private_key_label.setGeometry(10, 240, 680, 100)
        self.private_key_label.setReadOnly(True)
        self.private_key_label.hide()

        self.public_key_label = QTextEdit(parent=self)
        self.public_key_label.setGeometry(10, 350, 680, 100)
        self.public_key_label.setReadOnly(True)
        self.public_key_label.hide()

        self.signature_label = QTextEdit(parent=self)
        self.signature_label.setGeometry(10, 460, 680, 100)
        self.signature_label.setReadOnly(True)
        self.signature_label.hide()

        self.is_valid_label = QTextEdit(parent=self)
        self.is_valid_label.setGeometry(10, 570, 680, 50)
        self.is_valid_label.setReadOnly(True)
        self.is_valid_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 630, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        
    def call_eddsa(self):
        try:
            msg = self.msg_input.text()
            if not msg:
                raise ValueError('Please enter a message.')
            msg_bytes = msg.encode('utf-8')
            output_format = self.output_format_options.currentText()

            eddsa = EdDSA()
            signature = eddsa.sign(msg_bytes)
            is_valid = eddsa.verify(msg_bytes, signature)

            if output_format == 'Base64':
                private_key = eddsa.get_private_key().decode('utf-8')
                self.private_key_label.clear()
                self.private_key_label.setHtml(f"<b>Private key (Base64):</b><br>{str(private_key)}")
                self.private_key_label.show()

                public_key = eddsa.get_public_key().decode('utf-8')
                self.public_key_label.clear()
                self.public_key_label.setHtml(f"<b>Public key (Base64):</b><br>{str(public_key)}")
                self.public_key_label.show()

                signature_label = b64encode(signature).decode('utf-8')
                self.signature_label.clear()
                self.signature_label.setHtml(f"<b>Signature (Base64):</b><br>{str(signature_label)}")
                self.signature_label.show()
            elif output_format == 'Hex':
                private_key = hexlify(eddsa.get_private_key()).decode('utf-8')
                self.private_key_label.clear()
                self.private_key_label.setHtml(f"<b>Private key (Hex):</b><br>{str(private_key)}")
                self.private_key_label.show()

                public_key = hexlify(eddsa.get_public_key()).decode('utf-8')
                self.public_key_label.clear()
                self.public_key_label.setHtml(f"<b>Public key (Hex):</b><br>{str(public_key)}")
                self.public_key_label.show()

                signature_label = hexlify(signature).decode('utf-8')
                self.signature_label.clear()
                self.signature_label.setHtml(f"<b>Signature (Hex):</b><br>{str(signature_label)}")
                self.signature_label.show()
            else:
                self.private_key_label.clear()
                self.private_key_label.setHtml(f"<b>Private key (Raw):</b><br>{eddsa.get_private_key().decode()}")
                self.private_key_label.show()

                self.public_key_label.clear()
                self.public_key_label.setHtml(f"<b>Public key (Raw):</b><br>{eddsa.get_public_key().decode()}")
                self.public_key_label.show()

                self.signature_label.clear()
                self.signature_label.setHtml(f"<b>Signature (Raw):</b><br>{str(signature)}")
                self.signature_label.show()

            # Verify the signature
            is_valid = eddsa.verify(msg_bytes, signature)
            self.is_valid_label.clear()
            self.is_valid_label.setHtml(f"<b>Is signature valid?</b><br>{str(is_valid)}")
            self.is_valid_label.show()
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
