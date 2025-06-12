from PyQt6.QtWidgets                            import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style             import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style             import DefaultQLineEditStyle
from pgpy.constants                             import (PubKeyAlgorithm, KeyFlags, HashAlgorithm, 
                                                        SymmetricKeyAlgorithm, CompressionAlgorithm)
from pathlib                                    import Path
from PyQt6.QtCore                               import QProcess
from os                                         import makedirs, path
from datetime                                   import datetime
import pgpy, sys

class PGPKeyGenerate:
    def __init__(
            self, name, email, key_size, compression_algorithm, 
            sk_algorithm, pb_key_algorithm, hashalgo, curve):
        """Initialize the PGP Key Manager with user details.

        :param name: Name of the user for the key.
        :param email: Email of the user for the key."""
        self.name = name
        self.email = email
        self.compression_algorithm = compression_algorithm
        self.symmetric_key_algorithm = sk_algorithm
        self.pubkey_algorithm = pb_key_algorithm
        self.curve = curve
        self.key_size = key_size
        self.hashalgo = hashalgo
        self.key = None
        self.private_key = None
        self.public_key = None

    def generate_key_pair(self):
        """Generate a PGP key pair."""
        # Create a new PGPKeyPair
        if self.pubkey_algorithm in [PubKeyAlgorithm.DSA, PubKeyAlgorithm.RSAEncryptOrSign]:
            key = pgpy.PGPKey.new(self.pubkey_algorithm, self.key_size)
        else:
            key = pgpy.PGPKey.new(self.pubkey_algorithm, self.curve)
        
        # Create a User ID
        uid = pgpy.PGPUID.new(self.name, comment="PGP Key", email=self.email)
        
        # Add the user ID to the key with capabilities
        key.add_uid(
            uid,
            usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            ciphers=[self.symmetric_key_algorithm],
            compression=[self.compression_algorithm])
        self.key = key
        self.private_key = key
        self.public_key = key.pubkey
        return self.public_key, self.private_key

    def export_keys(self, public_key_file='public_key.asc', private_key_file='private_key.asc'):
        """Export the keys to files.

        :param public_key_file: File name for the public key (default 'public_key.asc').
        :param private_key_file: File name for the private key (default 'private_key.asc')."""
        if not self.key:
            raise ValueError("No keys generated to export.")

        # Export the public key
        with open(public_key_file, 'w') as pub_file:
            pub_file.write(str(self.public_key))
        
        # Export the private key
        with open(private_key_file, 'w') as priv_file:
            priv_file.write(str(self.private_key))

    def load_private_key(self, private_key_file):
        """Load a private key from a file.
        
        :param private_key_file: File containing the private key."""
        with open(private_key_file, 'r') as priv_file:
            self.private_key, _ = pgpy.PGPKey.from_blob(priv_file.read())

    def load_public_key(self, public_key_file):
        """Load a public key from a file.
        
        :param public_key_file: File containing the public key."""
        with open(public_key_file, 'r') as pub_file:
            self.public_key, _ = pgpy.PGPKey.from_blob(pub_file.read())

class PGPKeyPairGenerateWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Generate PGP Key Pair Tool"
        msgbox_txt = """
            This tool allows you to create secure 
            <b>PGP public</b> and <b>private keys</b> with ease. Customize your key pairs with a wide 
            range of algorithms, curves, and compression options to suit your needs.<br><br>
            <b>Features:</b>
            <ul>
                <li>Support for <i>RSA</i>, <i>DSA</i>, <i>ECDSA</i>, and <i>EdDSA</i> key algorithms.</li>
                <li>Customizable symmetric, hashing, and compression algorithms.</li>
                <li>Dynamic UI tailored to your key algorithm selections.</li>
                <li>Easy export of keys to files.</li>
            </ul>
            <b>Instructions:</b><br>
            Enter your name and email, select your preferred configurations, 
            and click <b>Generate</b> to create your keys.<br><br>
            <i>Note:</i> Ensure you save your private keys securely!"""

        self.setWindowTitle("Generate PGP Key Pairs")
        self.setFixedSize(700, 800)

        self.downloads_path = Path.home() / "Downloads" / "pgp_keys"
        makedirs(self.downloads_path, exist_ok=True)

        # Name input
        name_label = QLabel("Enter name:", parent=self)
        name_label.setGeometry(120, 10, 100, 50)
        self.name_input = DefaultQLineEditStyle(parent=self)
        self.name_input.setGeometry(10, 50, 280, 50)

        # Email input
        email_label = QLabel("Enter email:", parent=self)
        email_label.setGeometry(450, 10, 100, 50)
        self.email_input = DefaultQLineEditStyle(parent=self)
        self.email_input.setGeometry(340, 50, 280, 50)

        # Symmetric key algorithm options
        symmetric_key_algorithm_label = QLabel("Symmetric Key Algorithm:", parent=self)
        symmetric_key_algorithm_label.setGeometry(10, 120, 180, 50)
        self.symmetric_key_algorithm_options = DefaultQComboBoxStyle(
            parent=self,
            items=["AES128", "AES192", "AES256"])
        self.symmetric_key_algorithm_options.setGeometry(200, 120, 130, 50)
        
        # Public key algorithm options
        pb_key_label = QLabel("Public Key Algorithm:", parent=self)
        pb_key_label.setGeometry(360, 120, 150, 50)
        self.pb_key_options = DefaultQComboBoxStyle(
            parent=self,
            items=["RSA"])
        self.pb_key_options.setGeometry(510, 120, 130, 50)

        # Bits options
        self.bits_label = QLabel("Select bits:", parent=self)
        self.bits_label.setGeometry(10, 200, 100, 50)
        self.bits_options = DefaultQComboBoxStyle(
            parent=self,
            items=["2048", "3072", "4096"])
        self.bits_options.setGeometry(110, 200, 130, 50)
        self.pb_key_options.currentTextChanged.connect(self.toggle_bits_curve_label)

        # Compression algorithm options
        compression_algorithm_label = QLabel("Compression Algorithm:", parent=self)
        compression_algorithm_label.setGeometry(320, 200, 180, 50)
        self.compression_algorithm_options = DefaultQComboBoxStyle(
            parent=self,
            items=["ZIP", "Uncompressed"])
        self.compression_algorithm_options.setGeometry(500, 200, 130, 50)

        # Hashing algorithm options
        hashalgo_label = QLabel("Hashing Algorithm:", parent=self)
        hashalgo_label.setGeometry(10, 300, 180, 50)
        self.hashalgo_options = DefaultQComboBoxStyle(
            parent=self,
            items=["SHA1", "SHA224", "SHA256", "SHA384", "SHA512"])
        self.hashalgo_options.setGeometry(160, 300, 130, 50)

        # Save keys yes or no
        save_keys_label = QLabel("Save keys?", parent=self)
        save_keys_label.setGeometry(370, 260, 180, 50)
        self.save_keys_options = DefaultQComboBoxStyle(
            parent=self,
            items=["Yes", "No"])
        self.save_keys_options.setGeometry(350, 300, 130, 50)
        
        generate_button = DefaultButtonStyle("Generate", parent=self, bold=True, command=self.generate)
        generate_button.setGeometry(530, 300, 100, 50)

        self.private_key_label = QTextEdit(parent=self)
        self.private_key_label.setGeometry(10, 380, 680, 150)
        self.private_key_label.setReadOnly(True)
        self.private_key_label.hide()

        self.public_key_label = QTextEdit(parent=self)
        self.public_key_label.setGeometry(10, 540, 680, 150)
        self.public_key_label.setReadOnly(True)
        self.public_key_label.hide()

        self.saved_keys_label = QTextEdit(parent=self)
        self.saved_keys_label.setGeometry(10, 700, 680, 50)
        self.saved_keys_label.setReadOnly(True)
        self.saved_keys_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 750, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def generate(self):
        try:
            if self.name_input.text():
                if self.email_input.text():
                    name = self.name_input.text()
                    email = self.email_input.text()
                    key_size = int(self.bits_options.currentText())
                    compression_algorithm = self.compression_algorithm_options.currentText()
                    sk_algorithm = self.symmetric_key_algorithm_options.currentText()
                    pb_key_algorithm = self.pb_key_options.currentText()
                    hashalgo = self.hashalgo_options.currentText()
                    save_keys = self.save_keys_options.currentText()

                    if compression_algorithm == "ZIP":
                        compression_algorithm = CompressionAlgorithm.ZIP
                    else:
                        compression_algorithm = CompressionAlgorithm.Uncompressed

                    if sk_algorithm == "AES128":
                        sk_algorithm = SymmetricKeyAlgorithm.AES128
                    elif sk_algorithm == "AES192":
                        sk_algorithm = SymmetricKeyAlgorithm.AES192
                    elif sk_algorithm == "AES256":
                        sk_algorithm = SymmetricKeyAlgorithm.AES256

                    if pb_key_algorithm == "RSA":
                        pb_key_algorithm = PubKeyAlgorithm.RSAEncryptOrSign

                    if hashalgo == "SHA1":
                        hashalgo = HashAlgorithm.SHA1
                    if hashalgo == "SHA224":
                        hashalgo = HashAlgorithm.SHA224
                    if hashalgo == "SHA256":
                        hashalgo = HashAlgorithm.SHA256
                    if hashalgo == "SHA384":
                        hashalgo = HashAlgorithm.SHA384
                    if hashalgo == "SHA512":
                        hashalgo = HashAlgorithm.SHA512

                    if '@' not in email:
                        raise ValueError('Please enter a valid email')
                    else:
                        if pb_key_algorithm in [PubKeyAlgorithm.RSAEncryptOrSign]:
                            pgp_manager = PGPKeyGenerate(
                                name, 
                                email, 
                                key_size, 
                                compression_algorithm,
                                sk_algorithm,
                                pb_key_algorithm,
                                hashalgo,
                                curve = None)

                            public_key, private_key = pgp_manager.generate_key_pair()

                            self.private_key_label.clear()
                            self.private_key_label.setHtml(f"<b>Private key:</b><br>{private_key}")
                            self.private_key_label.show()
                            self.public_key_label.clear()
                            self.public_key_label.setHtml(f"<b>Public key:</b><br>{public_key}")
                            self.public_key_label.show()

                            if save_keys == "No":
                                QMessageBox.information(self, 'Successfull Key generation', 'Keys successfully generated')
                                self.saved_keys_label.clear()
                                self.saved_keys_label.hide()
                            else:
                                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                                key_folder = self.downloads_path / f'pgp_keys_{timestamp}'
                                makedirs(key_folder, exist_ok=True)
                                
                                private_key_path = key_folder / "private_key.asc"
                                public_key_path = key_folder / "public_key.asc"


                                # Export the keys to the Downloads folder
                                pgp_manager.export_keys(
                                    private_key_file=str(private_key_path),
                                    public_key_file=str(public_key_path))

                                # Show a custom message box with a button to open the Downloads folder
                                msg_box = QMessageBox(self)
                                msg_box.setWindowTitle('Generation successfull')
                                msg_box.setText(f'Keys successfully generated and saved at: {key_folder}')
                                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

                                # Add a custom button for opening the Downloads folder
                                open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                                msg_box.exec()

                                # If the user clicks "Open Downloads", open the Downloads folder
                                if msg_box.clickedButton() == open_folder_btn:
                                    self.open_downloads_folder()

                                self.saved_keys_label.clear()
                                self.saved_keys_label.setHtml(
                                    f'<b>Private Key and Public Key generated successfully and saved at:</b><br>'
                                    f'{private_key_path}<br>{public_key_path}')
                                self.saved_keys_label.show()
                else:
                    raise ValueError('Please enter an email')
            else:
                raise ValueError('Please enter a name')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def toggle_bits_curve_label(self, pubkey_algorithm):
        if pubkey_algorithm in ["RSA"]:
            self.bits_label.show()
            self.bits_options.show()
    
    def open_downloads_folder(self):
        # Open the Downloads folder using the appropriate command for the OS
        if sys.platform == 'win32':
            os.startfile(self.downloads_path)
        elif sys.platform == 'darwin':  # macOS
            QProcess.execute('open', [self.downloads_path])
        else:  # Linux and other Unix-like systems
            QProcess.execute('xdg-open', [str(self.downloads_path)])
