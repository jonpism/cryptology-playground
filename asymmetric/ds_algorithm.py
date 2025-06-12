from PyQt6.QtWidgets                                import QWidget, QLabel, QTextEdit, QMessageBox
from cryptography.hazmat.primitives.asymmetric      import dsa
from cryptography.hazmat.primitives                 import hashes
from cryptography.hazmat.primitives.serialization   import Encoding, PrivateFormat, PublicFormat, NoEncryption
from cryptography.hazmat.backends                   import default_backend
from DefaultStyles.button_style                     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style                 import DefaultQLineEditStyle
from DefaultStyles.qcombo_box_style                 import DefaultQComboBoxStyle
from binascii                                       import hexlify
from datetime                                       import datetime
from pathlib                                        import Path
import base64, os 

# Implementation
class DSAImp:

    def __init__(self, key_size=2048):
        # Generate a private key for DSA
        self.private_key = dsa.generate_private_key(key_size=key_size, backend=default_backend())
        self.public_key = self.private_key.public_key()
        
    def sign(self, message, hashalgo):
        """
        Signs the message using the private key.
        :param message: The message to be signed (as bytes).
        :return: The signature as bytes.
        """
        if hashalgo == "SHA1":
            signature = self.private_key.sign(
                message,
                hashes.SHA1())
            return signature
        elif hashalgo == "SHA224":
            signature = self.private_key.sign(
                message,
                hashes.SHA224())
            return signature
        elif hashalgo == "SHA256":
            signature = self.private_key.sign(
                message,
                hashes.SHA256())
            return signature
        elif hashalgo == "SHA384":
            signature = self.private_key.sign(
                message,
                hashes.SHA384())
            return signature
        elif hashalgo == "SHA512":
            signature = self.private_key.sign(
                message,
                hashes.SHA512())
            return signature

    def verify(self, message, signature, hashalgo):
        """
        Verifies the signature using the public key.
        :param message: The original message (as bytes).
        :param signature: The signature to be verified (as bytes).
        :return: True if the signature is valid, False otherwise.
        """
        try:
            if hashalgo == "SHA1":
                self.public_key.verify(
                    signature,
                    message,
                    hashes.SHA1())
                return True
            elif hashalgo == "SHA224":
                self.public_key.verify(
                    signature,
                    message,
                    hashes.SHA224())
                return True
            elif hashalgo == "SHA256":
                self.public_key.verify(
                    signature,
                    message,
                    hashes.SHA256())
                return True
            elif hashalgo == "SHA384":
                self.public_key.verify(
                    signature,
                    message,
                    hashes.SHA384())
                return True
            elif hashalgo == "SHA512":
                self.public_key.verify(
                    signature,
                    message,
                    hashes.SHA512())
                return True
        except Exception as e:
            QMessageBox.critical(self, 'An Error occured while verifying', str(e))

    def get_private_key(self):
        """
        Returns the private key in PEM format.
        :return: Private key as PEM-encoded string.
        """
        return self.private_key.private_bytes(
            Encoding.PEM,
            PrivateFormat.PKCS8,
            NoEncryption())

    def get_public_key(self):
        """
        Returns the public key in PEM format.
        :return: Public key as PEM-encoded string.
        """
        return self.public_key.public_bytes(
            Encoding.PEM,
            PublicFormat.SubjectPublicKeyInfo)

class DSAWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About DSA"
        msgbox_txt = (
        "The Digital Signature Algorithm (DSA) is a widely-used standard "
        "for digital signatures, developed by the U.S. National Institute "
        "of Standards and Technology (NIST) in 1991 as part of the Digital "
        "Signature Standard (DSS). DSA is based on modular arithmetic and is  "
        "primarily used for authenticating the integrity and authenticity "
        "of a message, rather than for encryption. DSA’s security is based on "
        "the Discrete Logarithm Problem in finite fields, which is computationally "
        "hard to solve. This problem involves finding a value x such that"
        "g^x ≡ y mod p, where p is a large prime. It's commonly used in digital "
        "certificates and protocols like TLS but has been somewhat supplanted by "
        "Elliptic Curve DSA (ECDSA) due to its better efficiency and "
        "security at shorter key lengths. DSA is retained only for the purposes of verifying existing signatures. <br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Digital_Signature_Algorithm>Wikipedia</a><br>"
        "<a href=https://www.geeksforgeeks.org/digital-signature-algorithm-dsa>Geeks for Geeks</a>")

        self.setWindowTitle("Digital Signature Algorithm")
        self.setFixedSize(700, 700)

        self.downloads_path = str(Path.home() / "Downloads")

        # MESSAGE
        msg_label = QLabel("Give message:", parent=self)
        msg_label.setGeometry(300, 10, 100, 50)

        self.message_input = DefaultQLineEditStyle(parent=self)
        self.message_input.setGeometry(10, 60, 680, 50)

        hashalgo_label = QLabel("Hash Algorithm:", parent=self)
        hashalgo_label.setGeometry(150, 110, 120, 50)
        items = ['SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512']
        self.hashalgo_options = DefaultQComboBoxStyle(parent=self, items=items)
        self.hashalgo_options.setGeometry(150, 160, 120, 50)

        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(450, 110, 120, 50)
        output_format_items = ['Base64', 'Hex', 'Raw']
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=output_format_items)
        self.output_format_options.setGeometry(450, 160, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_dsa)
        submit_button.setGeometry(300, 220, 100, 50)

        self.signature_label = QTextEdit(parent=self)
        self.signature_label.setGeometry(10, 300, 680, 100)
        self.signature_label.setReadOnly(True)
        self.signature_label.hide()

        self.private_key_label = QTextEdit(parent=self)
        self.private_key_label.setGeometry(10, 410, 680, 100)
        self.private_key_label.setReadOnly(True)
        self.private_key_label.hide()

        self.public_key_label = QTextEdit(parent=self)
        self.public_key_label.setGeometry(10, 520, 680, 100)
        self.public_key_label.setReadOnly(True)
        self.public_key_label.hide()

        self.is_valid = QLabel("", parent=self)
        self.is_valid.setGeometry(10, 630, 300, 50)
        self.is_valid.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_dsa(self):
        try:
            if self.message_input.text():
                message = self.message_input.text()
                message_bytes = message.encode('utf-8')
                hashalgo = self.hashalgo_options.currentText()
                output_format = self.output_format_options.currentText()

                dsa_object = DSAImp()
                signature = dsa_object.sign(message=message_bytes, hashalgo=hashalgo)
                is_valid = dsa_object.verify(message=message_bytes, signature=signature, hashalgo=hashalgo)
                public_key = dsa_object.get_public_key()
                private_key = dsa_object.get_private_key()

                if output_format == "Base64":
                    signature = base64.b64encode(signature).decode('utf-8')
                    public_key = base64.b64encode(public_key).decode('utf-8')
                    private_key = base64.b64encode(private_key).decode('utf-8')
                elif output_format == "Hex":
                    signature = hexlify(signature).decode('utf-8')
                    public_key = hexlify(public_key).decode('utf-8')
                    private_key = hexlify(private_key).decode('utf-8')

                # timestamp for filenames
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # save signature
                with open(os.path.join(self.downloads_path, f"signature_{timestamp}.txt"), "w", encoding="utf-8") as f:
                    f.write(signature)

                # save private key
                with open(os.path.join(self.downloads_path, f"private_key_{timestamp}.txt"), "w", encoding="utf-8") as f:
                    f.write(private_key)

                # save public key
                with open(os.path.join(self.downloads_path, f"public_key_{timestamp}.txt"), "w", encoding="utf-8") as f:
                    f.write(public_key)

                QMessageBox.information(
                    self, 
                    'Files Successfully generated',
                    f'Files saved at: {self.downloads_path}')

                self.signature_label.clear()
                self.signature_label.setHtml(f"<b>Signature:</b><br>{str(signature)}")
                self.signature_label.show()

                self.private_key_label.clear()
                self.private_key_label.setHtml(f"<b>Private key:</b><br>{str(private_key)}")
                self.private_key_label.show()

                self.public_key_label.clear()
                self.public_key_label.setHtml(f"<b>Public key:</b><br>{str(public_key)}")
                self.public_key_label.show()

                self.is_valid.clear()
                self.is_valid.setText(f"Is signature valid?: {str(is_valid)}")
                self.is_valid.show()
            else:
                raise ValueError('Please enter a message.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox(self, 'Unexpected Error', str(e))
