from PyQt6.QtWidgets                            import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style             import DefaultQComboBoxStyle
from cryptography.hazmat.primitives             import serialization
from base64                                     import b64decode, b64encode
from binascii                                   import hexlify
from cryptography.hazmat.primitives             import serialization
from cryptography.hazmat.primitives.asymmetric  import ed25519, ed448
from cryptography.hazmat.primitives             import serialization
from pathlib                                    import Path

downloads_path = Path.home() / "Downloads" / "eddsa_keys"

class EdDSAKeyPair:

    def __init__(self, algorithm, encoding):
        """Initializes the EdDSAKeyPair class and generates the key pair.

        :param algorithm: Algorithm to use ("ed25519" or "ed448")."""
        if encoding == "PEM":
            self.encoding = serialization.Encoding.PEM
        else:
            self.encoding = serialization.Encoding.DER
            
        self.algorithm = algorithm
        if self.algorithm == "ed25519":
            self.private_key = ed25519.Ed25519PrivateKey.generate()
        elif self.algorithm == "ed448":
            self.private_key = ed448.Ed448PrivateKey.generate()

        self.public_key = self.private_key.public_key()

    def get_private_key_pem(self, password=None):
        """Returns the private key in PEM format.

        :param password: Optional password to encrypt the private key.
        :return: Private key as a PEM-encoded string."""
        encryption = serialization.BestAvailableEncryption(password.encode()) if password else serialization.NoEncryption()
        return self.private_key.private_bytes(
            encoding=self.encoding,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption)

    def get_public_key_pem(self):
        """Returns the public key in PEM format.

        :return: Public key as a PEM-encoded string."""
        return self.public_key.public_bytes(
            encoding=self.encoding,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def save_keys_to_files(
            self, private_key_file="private_key.pem", 
            public_key_file="public_key.pem",
            password=None):
        """Saves the private and public keys to files.

        :param private_key_file: File name for the private key.
        :param public_key_file: File name for the public key.
        :param password: Optional password to encrypt the private key."""
        with open(private_key_file, "wb") as priv_file:
            priv_file.write(self.get_private_key_pem(password))

        with open(public_key_file, "wb") as pub_file:
            pub_file.write(self.get_public_key_pem())

class EdDSAKeyPairWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Generate EdDSA Key Pair Tool"
        msgbox_txt = (
            "<p>This tool allows you to generate cryptographic key pairs using the <b>Ed25519</b> or <b>Ed448</b> algorithms. "
            "It provides customizable options for key <b>encoding formats</b> (PEM or DER) and <b>output formats</b> (Base64, Hex, or Raw).</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "  <li>Generate secure EdDSA private and public key pairs.</li>"
            "  <li>Save keys to files in various formats for future use.</li>"
            "  <li>View keys in Base64, Hexadecimal, or Raw encoding directly in the interface.</li>"
            "</ul>"
            "<p>Use this tool to explore cryptographic concepts or integrate key pairs into your security applications.</p>"
            "<p style='color:gray; font-size:12px;'>Note: Always handle private keys securely and avoid sharing them with unauthorized parties.</p>")

        self.setWindowTitle("Generate EdDSA Key Pairs")
        self.setFixedSize(700, 700)

        # Algorithm options
        algorithm_label = QLabel("Select algorithm:", parent=self)
        algorithm_label.setGeometry(10, 20, 130, 50)
        self.algorithm_options = DefaultQComboBoxStyle(
            parent=self,
            items=["ed25519", "ed448"])
        self.algorithm_options.setGeometry(140, 20, 130, 50)

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
            algorithm = self.algorithm_options.currentText()
            encoding = self.encoding_options.currentText()
            output_format = self.output_format_options.currentText()

            if algorithm == "ed25519":
                ed25519_keys = EdDSAKeyPair(algorithm, encoding)
                private_key = ed25519_keys.get_private_key_pem()
                public_key = ed25519_keys.get_public_key_pem()
            else:
                ed448_keys = EdDSAKeyPair(algorithm, encoding)
                private_key = ed448_keys.get_private_key_pem()
                public_key = ed448_keys.get_public_key_pem()
            
            if encoding == "PEM":
                # Save keys to files
                downloads_path.mkdir(parents=True, exist_ok=True)
                
                prv_filename = f"{algorithm}_private_key.pem"
                pbl_filename = f"{algorithm}_public_key.pem"
                
                prv_path = downloads_path / prv_filename
                pbl_path = downloads_path / pbl_filename
                if algorithm == "ed25519":
                    ed25519_keys.save_keys_to_files(
                    private_key_file=str(prv_path), public_key_file=str(pbl_path), password=None)
                else:
                    ed448_keys.save_keys_to_files(
                    private_key_file=str(prv_path), public_key_file=str(pbl_path))
                QMessageBox.information(self, 'Success', f'Keys successfully generated and saved at: {downloads_path}')
                self.saved_keys_label.clear()
                self.saved_keys_label.setHtml(f"<b>Keys generated and saved at: </b><br> {downloads_path}")
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
