from PyQt6.QtWidgets                            import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style             import DefaultQComboBoxStyle
from cryptography.hazmat.primitives             import serialization
from base64                                     import b64decode, b64encode
from binascii                                   import hexlify
from cryptography.hazmat.primitives.asymmetric  import dsa
from cryptography.hazmat.primitives             import serialization
from pathlib                                    import Path
from os                                         import makedirs

downloads_path = Path.home() / "Downloads" / "dsa_keys"

class DSAKeyPair:
    def __init__(self, key_size, encoding):
        """Initializes the DSAKeyPair class and generates the key pair.

            :param key_size: Size of the DSA key"""
        if encoding == "PEM":
            self.encoding = serialization.Encoding.PEM
        else:
            self.encoding = serialization.Encoding.DER
        self.key_size = key_size
        self.private_key = dsa.generate_private_key(key_size=self.key_size)
        self.public_key = self.private_key.public_key()

    def get_private_key(self, password=None):
        """Returns the private key in PEM format.

            :param password: Optional password to encrypt the private key.
            :return: Private key as a PEM-encoded string."""
        encryption = serialization.BestAvailableEncryption(password.encode()) if password else serialization.NoEncryption()
        return self.private_key.private_bytes(
            encoding=self.encoding,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption)

    def get_public_key(self):
        """Returns the public key in PEM format.

        :return: Public key as a PEM-encoded string."""
        return self.public_key.public_bytes(
            encoding=self.encoding,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def save_keys_to_files(self, private_key_file="dsa_private_key.pem", public_key_file="dsa_public_key.pem", password=None):
        """Saves the private and public keys to files.

        :param private_key_file: File name for the private key.
        :param public_key_file: File name for the public key.
        :param password: Optional password to encrypt the private key."""
        makedirs(downloads_path, exist_ok=True)
        with open(downloads_path / "private_key.pem", "wb") as priv_file:
            priv_file.write(self.get_private_key(password))

        with open(downloads_path / "public_key.pem", "wb") as pub_file:
            pub_file.write(self.get_public_key())

class DSAKeyPairGenerateWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Generate DSA Key Pairs Tool"
        msgbox_txt = (
            "<p>This tool allows users to generate secure DSA (Digital Signature Algorithm) key pairs "
            "for cryptographic operations. Users can configure key sizes, encoding formats (PEM or DER), "
            "and output formats (Base64, Hex, or Raw) to suit various security and interoperability needs.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Support for key sizes: 2048, 3072, and 4096 bits.</li>"
            "<li>Choose between PEM and DER encoding formats.</li>"
            "<li>Save keys in Base64, Hex, or Raw representations.</li>"
            "<li>Securely store keys with optional password protection.</li>"
            "</ul>"
            "<p>Designed to make cryptographic key management simple and effective.</p>")

        self.setWindowTitle("Generate DSA Key Pairs")
        self.setFixedSize(700, 700)

        # Key size (bits) options
        bits_label = QLabel("Select bits:", parent=self)
        bits_label.setGeometry(10, 20, 100, 50)
        self.bits_options = DefaultQComboBoxStyle(
            parent=self,
            items=["2048", "3072", "4096"])
        self.bits_options.setGeometry(110, 20, 130, 50)

        # Encoding options
        encoding_label = QLabel("Select encoding:", parent=self)
        encoding_label.setGeometry(320, 20, 140, 50)
        self.encoding_options = DefaultQComboBoxStyle(
            parent=self,
            items=["PEM", "DER"])
        self.encoding_options.setGeometry(440, 20, 130, 50)

        # Output format options
        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(10, 100, 140, 50)
        self.output_format_options = DefaultQComboBoxStyle(
            parent=self,
            items=["Base64", "Hex", "Raw"])
        self.output_format_options.setGeometry(130, 100, 130, 50)

        generate_button = DefaultButtonStyle("Generate", parent=self, bold=True, command=self.generate)
        generate_button.setGeometry(300, 100, 100, 50)

        self.private_key_label = QTextEdit(parent=self)
        self.private_key_label.setGeometry(10, 220, 680, 150)
        self.private_key_label.setReadOnly(True)
        self.private_key_label.hide()

        self.public_key_label = QTextEdit(parent=self)
        self.public_key_label.setGeometry(10, 380, 680, 150)
        self.public_key_label.setReadOnly(True)
        self.public_key_label.hide()

        self.saved_keys_label = QTextEdit(parent=self)
        self.saved_keys_label.setGeometry(10, 550, 680, 50)
        self.saved_keys_label.setReadOnly(True)
        self.saved_keys_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def generate(self):
        try:
            key_size = int(self.bits_options.currentText())
            encoding = self.encoding_options.currentText()
            output_format = self.output_format_options.currentText()

            key_pair = DSAKeyPair(key_size, encoding)
            private_key = key_pair.get_private_key()
            public_key = key_pair.get_public_key()
            key_pair.save_keys_to_files(password=None)
            QMessageBox.information(self, 'Success', f'Key files generated and saved at {downloads_path}')
            self.saved_keys_label.clear()
            self.saved_keys_label.setHtml(f"<b>Files are located at:</b><br>{downloads_path}")
            self.saved_keys_label.show()

            if output_format == "Base64":
                if encoding == "PEM":
                    self.private_key_label.clear()
                    self.private_key_label.setHtml(f"<b>Private key (PEM - Base64):</b><br>{str(private_key.decode())}")
                    self.private_key_label.show()
                    self.public_key_label.clear()
                    self.public_key_label.setHtml(f"<b>Public key (PEM - Base64):</b><br>{str(public_key.decode())}")
                    self.public_key_label.show()
                else:  # DER
                    self.private_key_label.clear()
                    self.private_key_label.setHtml(f"<b>Private key (DER - Base64):</b><br>{str(b64encode(private_key).decode('utf-8'))}")
                    self.private_key_label.show()
                    self.public_key_label.clear()
                    self.public_key_label.setHtml(f"<b>Public key (DER - Base64):</b><br>{str(b64encode(public_key).decode('utf-8'))}")
                    self.public_key_label.show()
            elif output_format == "Hex":
                if encoding == "PEM":
                    private_key_hex = self.convert_pem_to_hex(private_key)
                    public_key_hex = self.convert_pem_to_hex(public_key)
                    self.private_key_label.clear()
                    self.private_key_label.setHtml(f"<b>Private key (PEM - Hex):</b><br>{str(private_key_hex)}")
                    self.private_key_label.show()
                    self.public_key_label.clear()
                    self.public_key_label.setHtml(f"<b>Public key (PEM - Hex):</b><br>{str(public_key_hex)}")
                    self.public_key_label.show()
                else:  # DER
                    self.private_key_label.clear()
                    self.private_key_label.setHtml(f"<b>Private key (DER - Hex):</b><br>{str(hexlify(private_key).decode('utf-8'))}")
                    self.private_key_label.show()
                    self.public_key_label.clear()
                    self.public_key_label.setHtml(f"<b>Public key (DER - Hex):</b><br>{str(hexlify(public_key).decode('utf-8'))}")
                    self.public_key_label.show()
            else: # Raw
                if encoding == "PEM":
                    self.private_key_label.clear()
                    self.private_key_label.setHtml(f"<b>Private key (PEM - Raw):</b><br>{str(private_key)}")
                    self.private_key_label.show()
                    self.public_key_label.clear()
                    self.public_key_label.setHtml(f"<b>Public key (PEM - Raw):</b><br>{str(public_key)}")
                    self.public_key_label.show()
                else:  # DER
                    self.private_key_label.clear()
                    self.private_key_label.setHtml(f"<b>Private key (DER - Raw):</b><br>{str(private_key)}")
                    self.private_key_label.show()
                    self.public_key_label.clear()
                    self.public_key_label.setHtml(f"<b>Public key (DER - Raw):</b><br>{str(public_key)}")
                    self.public_key_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve)) 
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
            
    def convert_pem_to_hex(self, pem_data):
        # Decode bytes to a string
        pem_str = pem_data.decode('utf-8')
    
        # Remove the PEM headers and footers
        pem_body = pem_str.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "")
        pem_body = pem_body.replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "")
        pem_body = pem_body.replace("-----BEGIN EC PRIVATE KEY-----", "").replace("-----END EC PRIVATE KEY-----", "")
        pem_body = pem_body.strip()
    
        # Decode the Base64 content
        der_data = b64decode(pem_body)
    
        # Convert the binary DER data to hex
        hex_data = hexlify(der_data).decode('utf-8')
    
        return hex_data
