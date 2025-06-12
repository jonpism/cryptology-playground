from PyQt6.QtWidgets                            import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style             import DefaultQComboBoxStyle
from cryptography.hazmat.primitives.asymmetric  import ec
from cryptography.hazmat.backends               import default_backend
from cryptography.hazmat.primitives             import serialization
from base64                                     import b64decode, b64encode
from binascii                                   import hexlify
from pathlib                                    import Path

downloads_path = Path.home() / "Downloads" / "elliptic_curve_keys"

class EllipticCurveKeyPair:
    
    def __init__(self, curve=None, encoding=None):
        if curve == 'SECP192R1':
            self.curve = ec.SECP192R1()
        elif curve == 'SECP224R1':
            self.curve = ec.SECP224R1()
        elif curve == 'SECP256K1':
            self.curve = ec.SECP256K1()
        elif curve == 'SECP384R1':
            self.curve = ec.SECP384R1()
        elif curve == "SECP521R1":
            self.curve = ec.SECP521R1()
        elif curve == "BrainpoolP256R1":
            self.curve = ec.BrainpoolP256R1
        elif curve == "BrainpoolP384R1":
            self.curve = ec.BrainpoolP384R1
        else:
            self.curve = ec.BrainpoolP512R1
        
        if encoding == "PEM":
            self.encoding = serialization.Encoding.PEM
        else:
            self.encoding = serialization.Encoding.DER

        self.format = serialization.PrivateFormat.PKCS8
        # Generate a private key for the given curve
        self.private_key = ec.generate_private_key(self.curve, default_backend())
        self.public_key = self.private_key.public_key()

    def get_private_key_pem(self):
        # Return the private key in PEM format
        return self.private_key.private_bytes(
            encoding=self.encoding,
            format=self.format,
            encryption_algorithm=serialization.NoEncryption())

    def get_public_key_pem(self, format=serialization.PublicFormat.SubjectPublicKeyInfo):
        # Return the public key in PEM format
        return self.public_key.public_bytes(
            encoding=self.encoding,
            format=format)

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

class EllipticCurveKeyPairWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About EC Key Pair Tool"
        msgbox_txt = (
            "<p>This tool enables users to generate secure Elliptic Curve (EC) key pairs for cryptographic purposes. "
            "Elliptic Curve Cryptography (ECC) is widely used in modern security protocols due to its efficiency "
            "and high level of security relative to key size.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Supports a variety of curves, including SECP and Brainpool families (e.g., SECP256K1, SECP384R1).</li>"
            "<li>Options for PEM or DER encoding formats.</li>"
            "<li>Export keys in Base64, Hex, or Raw formats.</li>"
            "<li>Generates both private and public keys with a simple interface.</li>"
            "</ul>"
            "<p>This tool is designed for developers and security professionals, making EC key management straightforward and reliable.</p>")

        self.setWindowTitle("Generate Elliptic Curve Key Pairs")
        self.setFixedSize(700, 700)

        # Curve options
        curve_label = QLabel("Select curve:", parent=self)
        curve_label.setGeometry(10, 20, 100, 50)
        self.curve_options = DefaultQComboBoxStyle(
            parent=self,
            items=[
                "SECP192R1", "SECP224R1", "SECP256K1", 
                "SECP384R1", "SECP521R1", "BrainpoolP256R1",
                "BrainpoolP384R1", "BrainpoolP512R1"])
        self.curve_options.setGeometry(110, 20, 130, 50)

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
        self.saved_keys_label.setGeometry(10, 540, 680, 50)
        self.saved_keys_label.setReadOnly(True)
        self.saved_keys_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def generate(self):
        try:
            curve = self.curve_options.currentText()
            encoding = self.encoding_options.currentText()
            output_format = self.output_format_options.currentText()

            key_pair = EllipticCurveKeyPair(curve=curve, encoding=encoding)
            private_key = key_pair.get_private_key_pem()
            public_key = key_pair.get_public_key_pem()

            private_key_path = downloads_path / "private_key.pem" if encoding == "PEM" else downloads_path / "private_key.der"
            public_key_path = downloads_path / "public_key.pem" if encoding == "PEM" else downloads_path / "public_key.der"
            downloads_path.mkdir(parents=True, exist_ok=True)

            if encoding == "PEM":
                key_pair.save_private_key_to_file(private_key_path)
                key_pair.save_public_key_to_file(public_key_path)
                QMessageBox.information(self, 'Success', f'Keys successfully generated and saved at {downloads_path} ')
                self.saved_keys_label.clear()
                self.saved_keys_label.setHtml(f"<b>Private and public key generated and saved at:</b><br> {downloads_path}")
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
