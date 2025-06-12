from PyQt6.QtWidgets                            import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style             import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style             import DefaultQLineEditStyle
from cryptography.hazmat.primitives.asymmetric  import ec
from cryptography.hazmat.primitives             import hashes, serialization
from cryptography.hazmat.backends               import default_backend
from cryptography.hazmat.primitives.kdf.hkdf    import HKDF
from pathlib                                    import Path
import os

class ECDH:
    def __init__(self, curve = None, hashalgo = None, salt = None):
        """
        Initialize the ECDH instance with the specified elliptic curve.
        """
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
            self.hashalgo = hashes.SHA224()
        elif hashalgo == 'SHA256':
            self.hashalgo = hashes.SHA256()
        elif hashalgo == 'SHA384':
            self.hashalgo = hashes.SHA384()
        else:
            self.hashalgo = hashes.SHA512()
        
        self.salt = salt
        self.private_key = ec.generate_private_key(self.curve, default_backend())
        self.public_key = self.private_key.public_key()
    
    def get_public_key_bytes(self):
        """
        Return the public key in PEM format for safe sharing.
        """
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def get_private_key_bytes(self):
        """
        Return the private key in PEM format.
        This should be securely stored and never shared openly.
        """
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())
    
    def load_peer_public_key(self, peer_public_key_bytes):
        """
        Load a peer's public key from PEM bytes, ensuring compatibility.
        """
        peer_public_key = serialization.load_pem_public_key(
            peer_public_key_bytes, 
            backend=default_backend())
        return peer_public_key
    
    def generate_shared_secret(self, peer_public_key):
        """
        Generate the shared ECDH secret using the peer's public key.
        """
        shared_secret = self.private_key.exchange(ec.ECDH(), peer_public_key)
        return shared_secret

    def derive_key(self, peer_public_key_bytes, key_length=32, info=b"handshake data"):
        """
        Derive a symmetric key using HKDF from the ECDH shared secret.
        """
        # load the peer's public key
        peer_public_key = self.load_peer_public_key(peer_public_key_bytes)
        
        # generate the ECDH shared secret
        shared_secret = self.generate_shared_secret(peer_public_key)
        
        # use HKDF to derive a symmetric key from the shared secret
        derived_key = HKDF(
            algorithm=self.hashalgo,
            length=key_length,
            salt=self.salt,
            info=info,
            backend=default_backend()).derive(shared_secret)
        
        return derived_key

    def export_keys(self, name_prefix="key", target_dir="."):
        """
        Exports private and public keys to PEM files in the specified target directory.
        """
        try:
            private_path = Path(target_dir) / f"{name_prefix}_private_key.pem"
            public_path  = Path(target_dir) / f"{name_prefix}_public_key.pem"

            with open(private_path, "wb") as f:
                f.write(self.get_private_key_bytes())

            with open(public_path, "wb") as f:
                f.write(self.get_public_key_bytes())

            return True, True  # indicate success
        except Exception as e:
            print(f"Failed to export keys for {name_prefix}: {e}")
            return False, False

    
    def get_salt(self):
        return self.salt

class ECDHWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About ECDH"
        msgbox_txt = (
        "Elliptic Curve Diffie-Hellman (ECDH) is a key exchange protocol that allows two parties "
        "to securely share a secret key over an insecure channel. It is based on the mathematics "
        " of elliptic curves and provides a high level of security with relatively small key sizes "
        "compared to traditional methods like RSA. ECDH is widely used in secure communications "
        "protocols such as TLS (Transport Layer Security), which underpins secure web traffic (HTTPS)."
        "Many cryptocurrencies use ECDH for securing transactions. ECDH can also be used in secure "
        "messaging applications to establish encrypted channels. ECDH is a powerful and efficient "
        "method for secure key exchange, widely adopted in various security protocols. Its "
        "reliance on elliptic curve mathematics allows for a high level of security while "
        "maintaining efficiency, making it suitable for modern cryptographic applications.<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman>Wikipedia</a><br>"
        "<a href=https://cryptobook.nakov.com/asymmetric-key-ciphers/ecdh-key-exchange>Practical Cryptography for Developers</a>")

        self.setWindowTitle("Elliptic Curve Diffie Hellman Key agreement")
        self.setFixedSize(700, 1000)

        self.downloads_path = str(Path.home() / "Downloads")

        # curve options
        curve_label = QLabel("Select curve:", parent=self)
        curve_label.setGeometry(10, 20, 100, 50)
        self.curve_options = DefaultQComboBoxStyle(
            parent=self,
            items=["SECP192R1", "SECP224R1", "SECP256K1", "SECP384R1", "SECP521R1"])
        self.curve_options.setGeometry(110, 20, 130, 50)

        # hashalgo options
        hashalgo_label = QLabel("Select Hash Algorithm:", parent=self)
        hashalgo_label.setGeometry(320, 20, 250, 50)
        self.hashalgo_options = DefaultQComboBoxStyle(
            parent=self,
            items=["SHA224", "SHA256", "SHA384", "SHA512"])
        self.hashalgo_options.setGeometry(490, 20, 120, 50)

        # salt input
        salt_input_label = QLabel("Give salt (Generates a random if none given):", parent=self)
        salt_input_label.setGeometry(10, 80, 310, 50)
        self.salt_input = DefaultQLineEditStyle(
            parent=self,
            placeholder_text='16 bytes long.',
            max_length=16)
        self.salt_input.setGeometry(100, 120, 150, 50)

        # export keys options
        export_keys_label = QLabel("Export keys?", parent=self)
        export_keys_label.setGeometry(380, 80, 250, 50)
        self.export_keys_options = DefaultQComboBoxStyle(
            parent=self,
            items=["Yes", "No"])
        self.export_keys_options.setGeometry(380, 120, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.call_ecdh)
        submit_button.setGeometry(540, 120, 100, 50)

        self.alice_private_key_label = QTextEdit(parent=self)
        self.alice_private_key_label.setGeometry(10, 190, 680, 100)
        self.alice_private_key_label.setReadOnly(True)
        self.alice_private_key_label.hide()

        self.bob_private_key_label = QTextEdit(parent=self)
        self.bob_private_key_label.setGeometry(10, 300, 680, 100)
        self.bob_private_key_label.setReadOnly(True)
        self.bob_private_key_label.hide()

        self.alice_public_key_label = QTextEdit(parent=self)
        self.alice_public_key_label.setGeometry(10, 410, 680, 100)
        self.alice_public_key_label.setReadOnly(True)
        self.alice_public_key_label.hide()

        self.bob_public_key_label = QTextEdit(parent=self)
        self.bob_public_key_label.setGeometry(10, 520, 680, 100)
        self.bob_public_key_label.setReadOnly(True)
        self.bob_public_key_label.hide()

        self.alice_derived_key_label = QTextEdit(parent=self)
        self.alice_derived_key_label.setGeometry(10, 630, 680, 70)
        self.alice_derived_key_label.setReadOnly(True)
        self.alice_derived_key_label.hide()

        self.bob_derived_key_label = QTextEdit(parent=self)
        self.bob_derived_key_label.setGeometry(10, 720, 680, 70)
        self.bob_derived_key_label.setReadOnly(True)
        self.bob_derived_key_label.hide()

        self.salt_label = QTextEdit(parent=self)
        self.salt_label.setGeometry(10, 800, 680, 50)
        self.salt_label.setReadOnly(True)
        self.salt_label.hide()

        self.keys_match_label = QTextEdit(parent=self)
        self.keys_match_label.setGeometry(10, 860, 680, 50)
        self.keys_match_label.setReadOnly(True)
        self.keys_match_label.hide()

        self.export_keys_label = QTextEdit(parent=self)
        self.export_keys_label.setGeometry(10, 930, 480, 50)
        self.export_keys_label.setReadOnly(True)
        self.export_keys_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 950, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_ecdh(self):
        try:
            curve = self.curve_options.currentText()
            hashalgo = self.hashalgo_options.currentText()
            salt = self.salt_input.text()

            # ensure salt is exactly 16 bytes or use os.urandom if not
            if len(salt) < 16:
                salt = os.urandom(16)  # generate random salt if input is too short
            else:
                salt = salt.encode('utf-8')[:16]  # truncate or pad to 16 bytes

            alice = ECDH(curve=curve, hashalgo=hashalgo, salt=salt)
            bob = ECDH(curve=curve, hashalgo=hashalgo, salt=salt)

            # Alice's private key
            alice_prv_key = alice.get_private_key_bytes()
            self.alice_private_key_label.clear()
            self.alice_private_key_label.setHtml(f"<b>Alice's Private key:</b><br>{str(alice_prv_key.decode('utf-8'))}")
            self.alice_private_key_label.show()

            # Bob's private key
            bob_prv_key = bob.get_private_key_bytes()
            self.bob_private_key_label.clear()
            self.bob_private_key_label.setHtml(f"<b>Bob's Private key:</b><br>{str(bob_prv_key.decode('utf-8'))}")
            self.bob_private_key_label.show()

            # Alice's public key
            alice_pbl_key = alice.get_public_key_bytes()
            self.alice_public_key_label.clear()
            self.alice_public_key_label.setHtml(f"<b>Alice's Public key:</b><br>{str(alice_pbl_key.decode('utf-8'))}")
            self.alice_public_key_label.show()

            # Bob's public key
            bob_pbl_key = bob.get_public_key_bytes()
            self.bob_public_key_label.clear()
            self.bob_public_key_label.setHtml(f"<b>Bob's Public key:</b><br>{str(bob_pbl_key.decode('utf-8'))}")
            self.bob_public_key_label.show()

            # Exchange public keys
            alice_symmetric_key = alice.derive_key(bob_pbl_key)
            self.alice_derived_key_label.clear()
            self.alice_derived_key_label.setHtml(f"<b>Alices's derived symmetric key:</b><br>{str(alice_symmetric_key)}")
            self.alice_derived_key_label.show()
            bob_symmetric_key = bob.derive_key(alice_pbl_key)
            self.bob_derived_key_label.clear()
            self.bob_derived_key_label.setHtml(f"<b>Bob's derived symmetric key:</b><br>{str(bob_symmetric_key)}")
            self.bob_derived_key_label.show()

            # Salt label
            self.salt_label.clear()
            self.salt_label.setHtml(f"<b>Salt:</b>{str(alice.get_salt())}")
            self.salt_label.show()

            # Do the keys match?
            self.keys_match_label.clear()
            self.keys_match_label.setHtml(f"<b>Do the keys match?</b><br>{str(alice_symmetric_key == bob_symmetric_key)}")
            self.keys_match_label.show()

            if self.export_keys_options.currentText() == "Yes":
                alice.export_keys("alice", target_dir=self.downloads_path)
                bob.export_keys("bob", target_dir=self.downloads_path)
                # export keys successfully - label and messagebox
                QMessageBox.information(self, 'Success', 'Keys exported and saved successfully')
                self.export_keys_label.clear()
                self.export_keys_label.setHtml(f"Keys successfully exported and saved at: {self.downloads_path}")
                self.export_keys_label.show()
            else:
                self.export_keys_label.clear()
                self.export_keys_label.hide()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

