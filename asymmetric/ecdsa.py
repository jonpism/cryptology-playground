from PyQt6.QtWidgets                            import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style             import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style             import DefaultQLineEditStyle
from cryptography.hazmat.primitives.asymmetric  import ec
from cryptography.hazmat.primitives             import hashes, serialization
from cryptography.hazmat.backends               import default_backend
from cryptography.exceptions                    import InvalidSignature
from base64                                     import b64encode
from binascii                                   import hexlify

class ECDSA:

    def __init__(self, curve=None, hashalgo = None):
        """Initialize the ECC class with the selected curve."""
        if curve == 'SECP192R1':
            self.curve = ec.SECP192R1()
        elif curve == 'SECP224R1':
            self.curve = ec.SECP224R1()
        elif curve == 'SECP256K1':
            self.curve = ec.SECP256K1()
        elif curve == 'SECP384R1':
            self.curve = ec.SECP384R1()
        else:
            self.curve = ec.SECP521R1()
        
        if hashalgo == 'SHA224':
            self.hashalgo = ec.ECDSA(hashes.SHA224())
        elif hashalgo == 'SHA256':
            self.hashalgo = ec.ECDSA(hashes.SHA256())
        elif hashalgo == 'SHA384':
            self.hashalgo = ec.ECDSA(hashes.SHA384())
        else:
            self.hashalgo = ec.ECDSA(hashes.SHA512())
            
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        """Generate a new private and public key pair."""
        self.private_key = ec.generate_private_key(self.curve, default_backend())
        self.public_key = self.private_key.public_key()
        return self.private_key, self.public_key

    def get_private_key_bytes(self):
        """Get the private key in PEM format."""
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())

    def get_public_key_bytes(self):
        """Get the public key in PEM format."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def sign_message(self, message: bytes):
        """Sign a message using the private key."""
        if not self.private_key:
            raise ValueError("Private key not generated.")
        signature = self.private_key.sign(message, self.hashalgo)
        return signature

    def verify_signature(self, message: bytes, signature: bytes):
        """Verify a message signature using the public key."""
        if not self.public_key:
            raise ValueError("Public key not generated.")
        try:
            self.public_key.verify(signature, message, self.hashalgo)
            return True
        except InvalidSignature:
            return False

class ECDSAWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About ECDSA"
        msgbox_txt = (
        "The Elliptic Curve Digital Signature Algorithm (ECDSA) is a cryptographic algorithm "
        "used to create and verify digital signatures. It's based on elliptic curve cryptography "
        "(ECC), which offers a high level of security with smaller key sizes compared to "
        "traditional algorithms like RSA. ECDSA’s compact and secure design has made it a "
        "fundamental part of modern cryptography, particularly where performance, security "
        "and small data size are essential. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm>Wikipedia</a><br>"
        "<a href=https://www.geeksforgeeks.org/blockchain-elliptic-curve-digital-signature-algorithm-ecdsa>Geeks for Geeks</a>")

        self.setWindowTitle("Elliptic Curve Digital Signature Algorithm")
        self.setFixedSize(700, 740)

        # Message input
        msg_label = QLabel("Enter message:", parent=self)
        msg_label.setGeometry(300, 10, 100, 50)
        self.msg_input = DefaultQLineEditStyle(parent=self)
        self.msg_input.setGeometry(10, 60, 680, 50)

        # Curve options
        curve_label = QLabel("Select curve:", parent=self)
        curve_label.setGeometry(10, 130, 100, 50)
        self.curve_options = DefaultQComboBoxStyle(
            parent=self,
            items=["SECP192R1", "SECP224R1", "SECP256K1", "SECP384R1", "SECP521R1"])
        self.curve_options.setGeometry(110, 130, 130, 50)

        # Hashalgo options
        hashalgo_label = QLabel("Select Hash Algorithm:", parent=self)
        hashalgo_label.setGeometry(320, 130, 250, 50)
        self.hashalgo_options = DefaultQComboBoxStyle(
            parent=self,
            items=["SHA224", "SHA256", "SHA384", "SHA512"])
        self.hashalgo_options.setGeometry(490, 130, 120, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(10, 220, 120, 50)
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=['Base64', 'Hex', 'Raw'])
        self.output_format_options.setGeometry(130, 220, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_ecc)
        submit_button.setGeometry(330, 220, 100, 50)

        self.private_key_label = QTextEdit(parent=self)
        self.private_key_label.setGeometry(10, 300, 680, 100)
        self.private_key_label.setReadOnly(True)
        self.private_key_label.hide()

        self.public_key_label = QTextEdit(parent=self)
        self.public_key_label.setGeometry(10, 410, 680, 100)
        self.public_key_label.setReadOnly(True)
        self.public_key_label.hide()

        self.signature_label = QTextEdit(parent=self)
        self.signature_label.setGeometry(10, 520, 680, 100)
        self.signature_label.setReadOnly(True)
        self.signature_label.hide()

        self.is_valid_label = QTextEdit(parent=self)
        self.is_valid_label.setGeometry(10, 630, 680, 50)
        self.is_valid_label.setReadOnly(True)
        self.is_valid_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 690, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_ecc(self):
        try:
            msg = self.msg_input.text()
            if not msg:
                raise ValueError('Please enter a message.')
            else:
                msg_bytes = msg.encode('utf-8')
                curve = self.curve_options.currentText()
                hashalgo = self.hashalgo_options.currentText()
                output_format = self.output_format_options.currentText()

                obj = ECDSA(curve=curve, hashalgo=hashalgo)
                obj.generate_keys()
                signature = obj.sign_message(msg_bytes)
                is_valid = obj.verify_signature(msg_bytes, signature)

                if output_format == 'Base64':
                    private_key = b64encode(obj.get_private_key_bytes()).decode('utf-8')
                    self.private_key_label.clear()
                    self.private_key_label.setHtml(f"<b>Private key (Base64):</b><br>{str(private_key)}")
                    self.private_key_label.show()

                    public_key = b64encode(obj.get_public_key_bytes()).decode('utf-8')
                    self.public_key_label.clear()
                    self.public_key_label.setHtml(f"<b>Public key (Base64):</b><br>{str(public_key)}")
                    self.public_key_label.show()

                    signature_label = b64encode(signature).decode('utf-8')
                    self.signature_label.clear()
                    self.signature_label.setHtml(f"<b>Signature (Base64):</b><br>{str(signature_label)}")
                    self.signature_label.show()

                elif output_format == 'Hex':
                    private_key = hexlify(obj.get_private_key_bytes()).decode('utf-8')
                    self.private_key_label.clear()
                    self.private_key_label.setHtml(f"<b>Private key (Hex):</b><br>{str(private_key)}")
                    self.private_key_label.show()

                    public_key = hexlify(obj.get_public_key_bytes()).decode('utf-8')
                    self.public_key_label.clear()
                    self.public_key_label.setHtml(f"<b>Public key (Hex):</b><br>{str(public_key)}")
                    self.public_key_label.show()

                    signature_label = hexlify(signature).decode('utf-8')
                    self.signature_label.clear()
                    self.signature_label.setHtml(f"<b>Signature (Hex):</b><br>{str(signature_label)}")
                    self.signature_label.show()
                else:
                    self.private_key_label.clear()
                    self.private_key_label.setHtml(f"<b>Private key (Raw):</b><br>{str(obj.get_private_key_bytes().decode('utf-8'))}")
                    self.private_key_label.show()

                    self.public_key_label.clear()
                    self.public_key_label.setHtml(f"<b>Public key (Raw):</b><br>{str(obj.get_public_key_bytes().decode('utf-8'))}")
                    self.public_key_label.show()

                    self.signature_label.clear()
                    self.signature_label.setHtml(f"<b>Signature (Raw):</b><br>{str(signature)}")
                    self.signature_label.show()

                self.is_valid_label.clear()
                self.is_valid_label.setHtml(f"<b>Is signature valid:</b><br>{str(is_valid)}")
                self.is_valid_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
