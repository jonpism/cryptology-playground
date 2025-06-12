from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox, QFileDialog
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from Crypto.PublicKey               import RSA
from Crypto.Cipher                  import PKCS1_OAEP
from Crypto.Signature               import pkcs1_15
from Crypto.Hash                    import SHA256
from base64                         import b64encode, b64decode
 
# Implementation
class RSAImp:
    def __init__(self, public_key=None, private_key=None):
        self.public_key = None
        self.private_key = None

        if public_key:
            if isinstance(public_key, str) and public_key.endswith(".pem"):
                with open(public_key, "rb") as f:
                    self.public_key = RSA.import_key(f.read())
            elif isinstance(public_key, bytes):
                self.public_key = RSA.import_key(public_key)

        if private_key:
            if isinstance(private_key, str) and private_key.endswith(".pem"):
                with open(private_key, "rb") as f:
                    self.private_key = RSA.import_key(f.read())
            elif isinstance(private_key, bytes):
                self.private_key = RSA.import_key(private_key)

    def encrypt(self, message):
        """Encrypt a message using the public key with PKCS#1 OAEP."""
        if not self.public_key:
            raise ValueError("Public key not loaded.")
        
        cipher = PKCS1_OAEP.new(self.public_key)
        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        return b64encode(encrypted_message).decode('utf-8')

    def decrypt(self, encrypted_message):
        """Decrypt a message using the private key with PKCS#1 OAEP."""
        if not self.private_key:
            raise ValueError("Private key not loaded.")
        cipher = PKCS1_OAEP.new(self.private_key)
        decrypted_message = cipher.decrypt(b64decode(encrypted_message))
        
        return decrypted_message.decode('utf-8')
    
    def sign(self, message):
        """Sign a message using the private key and SHA-256."""
        if not self.private_key:
            raise ValueError("Private key not loaded.")
        
        message_hash = SHA256.new(message.encode('utf-8'))
        signature = pkcs1_15.new(self.private_key).sign(message_hash)
        return b64encode(signature).decode('utf-8')

    def verify(self, message, signature):
        """Verify a message's signature using the public key."""
        if not self.public_key:
            raise ValueError("Public key not loaded.")

        message_hash = SHA256.new(message.encode('utf-8'))
        try:
            pkcs1_15.new(self.public_key).verify(message_hash, b64decode(signature))
            return True
        except (ValueError, TypeError):
            return False

class RSAWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About RSA Implementation"
        msgbox_txt = (
            "This application implements RSA encryption and signing using the PyCryptodome library. RSA "
            "(Rivest–Shamir–Adleman) is a widely used public-key cryptosystem for secure data transmission.<br><br>"
            "<b>Features:</b><br>"
            "<ul>"
            "<li><b>Import keys:</b> Supports ONLY generated keys in PEM format from RSA Key Generator TOOL in Other Tools section.</li>"
            "<li><b>Encryption:</b> Secure plaintext with the recipient’s public key using PKCS#1 OAEP padding.</li>"
            "<li><b>Decryption:</b> Restore the original message with the recipient’s private key.</li>"
            "<li><b>Signing:</b> Generate a SHA-256 signature with the sender’s private key to ensure authenticity.</li>"
            "<li><b>Verification:</b> Validate the signature using the sender’s public key to confirm integrity.</li>"
            "</ul>"
            "<br><b>Useful links:</b><br>"
            "<a href=https://en.wikipedia.org/wiki/RSA_(cryptosystem)>Wikipedia on RSA</a><br>"
            "<a href=https://www.pycryptodome.org/src/examples>PyCryptodome Documentation</a>")

        self.setWindowTitle("RSA")
        self.setFixedSize(1100, 800)

        # Plaintext
        plaintext_label = QLabel("Enter plaintext:", parent=self)
        plaintext_label.setGeometry(200, 10, 120, 50)
        self.plaintext_input = DefaultQLineEditStyle(parent=self)
        self.plaintext_input.setGeometry(10, 60, 500, 50)

        load_receivers_pubkey_button = DefaultButtonStyle(
            'Load receiver`s public key for encryption',
            parent=self,
            command=self.load_receivers_pubkey_file)
        load_receivers_pubkey_button.setGeometry(10, 130, 300, 50)

        load_senders_prvkey_button = DefaultButtonStyle(
            'Load sender`s private key for signing',
            parent=self,
            command=self.load_senders_prvkey_file)
        load_senders_prvkey_button.setGeometry(10, 200, 300, 50)

        encrypt_button = DefaultButtonStyle("Encrypt\nand\nSign", parent=self, bold=True, command=self.call_rsa_encrypt_and_sign)
        encrypt_button.setGeometry(370, 140, 100, 90)

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 310, 500, 100)
        self.ciphertext_label.setReadOnly(True)

        self.receivers_public_key_label = QTextEdit(parent=self)
        self.receivers_public_key_label.setGeometry(10, 420, 500, 100)
        self.receivers_public_key_label.setReadOnly(True)

        self.senders_private_key_label = QTextEdit(parent=self)
        self.senders_private_key_label.setGeometry(10, 530, 500, 100)
        self.senders_private_key_label.setReadOnly(True)

        self.signature_label = QTextEdit(parent=self)
        self.signature_label.setGeometry(10, 640, 500, 100)
        self.signature_label.setReadOnly(True)

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(1050, 750, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
        _label = QLabel(
            '|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n'
            '|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n', 
            parent=self)
        _label.setGeometry(550, 5, 20, 1000)

        # ciphertext
        ciphertext_label = QLabel("Paste Ciphertext:", parent=self)
        ciphertext_label.setGeometry(800, 10, 120, 50)
        self.ciphertext_input = DefaultQLineEditStyle(parent=self)
        self.ciphertext_input.setGeometry(580, 60, 500, 50)

        # signature
        signature_label = QLabel("Paste Signature:", parent=self)
        signature_label.setGeometry(800, 130, 120, 50)
        self.signature_input = DefaultQLineEditStyle(parent=self)
        self.signature_input.setGeometry(580, 180, 500, 50)

        load_receivers_prvkey_button = DefaultButtonStyle(
            'Load receiver`s private key for decryption',
            parent=self,
            command=self.load_receivers_prvkey_file)
        load_receivers_prvkey_button.setGeometry(580, 260, 330, 50)

        load_senders_pblkey_button = DefaultButtonStyle(
            'Load sender`s public key for verification',
            parent=self,
            command=self.load_senders_pblkey_file)
        load_senders_pblkey_button.setGeometry(580, 330, 330, 50)

        decrypt_button = DefaultButtonStyle("Decrypt\nand\nVerify", parent=self, bold=True, command=self.call_rsa_decrypt_and_verify)
        decrypt_button.setGeometry(950, 270, 100, 90)

        self.decrypted_text_label = QTextEdit(parent=self)
        self.decrypted_text_label.setGeometry(580, 410, 500, 100)
        self.decrypted_text_label.setReadOnly(True)
        
        self.verified_signature_label = QTextEdit(parent=self)
        self.verified_signature_label.setGeometry(580, 530, 500, 100)
        self.verified_signature_label.setReadOnly(True)

        self.receiver_prv_key_label = QTextEdit(parent=self)
        self.receiver_prv_key_label.setGeometry(580, 640, 450, 70)
        self.receiver_prv_key_label.setReadOnly(True)
        
        self.sender_public_key_label = QTextEdit(parent=self)
        self.sender_public_key_label.setGeometry(580, 720, 450, 70)
        self.sender_public_key_label.setReadOnly(True)

    # for decryption
    def load_receivers_prvkey_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Select Receiver`s private key file', '', '(*.pem);;All Files (*)')
            if not file_path:
                raise ValueError("No private key file selected.")

            self.receiver_private_key_file = file_path
            QMessageBox.information(self, 'Receiver`s Private key selected', f'Selected private key: {file_path}')
            self.receiver_prv_key_label.setHtml(f"<b>Currently selected Receiver`s private key:</b><br>{file_path}")
            self.receiver_prv_key_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    # for verification
    def load_senders_pblkey_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Select Sender`s public key file', '', '(*.pem);;All Files (*)')
            if not file_path:
                raise ValueError("No public key file selected.")

            self.sender_public_key_file = file_path
            QMessageBox.information(self, 'Sender`s Public key selected', f'Selected public key: {file_path}')
            self.sender_public_key_label.setHtml(f"<b>Currently selected Sender`s public key:</b><br>{file_path}")
            self.sender_public_key_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def call_rsa_decrypt_and_verify(self):
        try:
            ciphertext = self.ciphertext_input.text()
            signature = self.signature_input.text()
            if not ciphertext:
                raise ValueError("Please paste the ciphertext.")
            if not signature:
                raise ValueError("Please paste the signature.")
            if not hasattr(self, 'receiver_private_key_file'):
                raise ValueError("Receiver's private key not loaded.")
            if not hasattr(self, 'sender_public_key_file'):
                raise ValueError("Sender's public key not loaded.")

            rsa = RSAImp(self.sender_public_key_file, self.receiver_private_key_file)
            decrypted_message = rsa.decrypt(ciphertext)
            verified = rsa.verify(decrypted_message, signature)

            QMessageBox.information(self, "Original plaintext/message:", str(decrypted_message))
            self.decrypted_text_label.clear()
            self.decrypted_text_label.setHtml(f"<b>Encrypted Text:</b><br>{str(decrypted_message)}")
            self.decrypted_text_label.show()

            QMessageBox.information(self, "Signature verification:", str(verified))
            self.verified_signature_label.clear()
            self.verified_signature_label.setHtml(f"<b>Is Signature VALID?:</b><br>{str(verified)}")
            self.verified_signature_label.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    # for encrypting
    def load_receivers_pubkey_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Select Receiver`s public key file', '', '(*.pem);;All Files (*)')
            if not file_path:
                raise ValueError("No public key file selected.")
            
            self.public_key_file = file_path
            self.receivers_public_key_label.setHtml(f"<b>Currently selected Receiver`s public key file:</b><br>{file_path}")
            self.receivers_public_key_label.show()
            QMessageBox.information(self, 'Receiver`s Public key selected', f'Selected public key: {file_path}')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    # for signing
    def load_senders_prvkey_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Select sender`s private key file', '', '(*.pem);;All Files (*)')
            if not file_path:
                raise ValueError("No private key file selected.")
            
            self.private_key_file = file_path
            self.senders_private_key_label.setHtml(f"<b>Currently selected Sender`s private key file:</b><br>{file_path}")
            self.senders_private_key_label.show()
            QMessageBox.information(self, 'Sender`s Private key selected', f'Selected private key: {file_path}')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def call_rsa_encrypt_and_sign(self):
        try:
            if self.plaintext_input.text():
                if self.public_key_file:
                    if self.private_key_file:
                        plaintext = self.plaintext_input.text()

                        rsa = RSAImp(self.public_key_file, self.private_key_file)

                        ciphertext = rsa.encrypt(plaintext)
                        self.ciphertext_label.clear()
                        self.ciphertext_label.setHtml(f"<b>Ciphertext (Base64):</b><br>{str(ciphertext)}")
                        self.ciphertext_label.show()

                        signature = rsa.sign(plaintext)
                        self.signature_label.clear()
                        self.signature_label.setHtml(f"<b>Signature (Base64):</b><br>{str(signature)}")
                        self.signature_label.show()

                    else:
                        raise ValueError('No private key loaded.')
                else:
                    raise ValueError('No public key loaded.')
            else:
                raise ValueError('Please enter a plaintext.')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
