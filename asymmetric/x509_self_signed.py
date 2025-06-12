from PyQt6.QtWidgets                            import QWidget, QLabel, QMessageBox, QTextEdit
from PyQt6.QtCore                               import QProcess
from cryptography                               import x509
from cryptography.x509.oid                      import NameOID
from cryptography.hazmat.primitives             import hashes
from cryptography.hazmat.primitives.asymmetric  import rsa
from cryptography.hazmat.primitives             import serialization
from cryptography.hazmat.backends               import default_backend
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style             import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style             import DefaultQLineEditStyle
from pathlib                                    import Path
import datetime, sys, os

class X509SelfSignedCertGenerator:
    def __init__(
            self, country_name, state_or_province_name, locality_name, organization_name, common_name, 
            key_size=2048, san_names=None, valid_days=365):
        """
        Initialize with common certificate attributes and options for SAN and validity period.
        :param san_names: List of SAN names (domain names or IPs), default is None.
        :param valid_days: Number of days the certificate will be valid, default is 365.
        """
        self.country_name = country_name
        self.state_or_province_name = state_or_province_name
        self.locality_name = locality_name
        self.organization_name = organization_name
        self.common_name = common_name
        self.key_size = key_size
        self.san_names = san_names if san_names else []
        self.valid_days = valid_days
        self.private_key = None
        self.cert = None

    def generate_private_key(self):
        """
        Generates a private key for signing the certificate.
        """
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend())
        return self.private_key

    def generate_self_signed_cert(self):
        """
        Generates a self-signed X.509 certificate with SAN, keyUsage and customizable validity period.
        """
        if not self.private_key:
            self.generate_private_key()

        # Define subject and issuer (for self-signed, they are the same)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, self.state_or_province_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, self.locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.organization_name),
            x509.NameAttribute(NameOID.COMMON_NAME, self.common_name),])

        # Certificate validity period
        valid_from = datetime.datetime.utcnow()
        valid_to = valid_from + datetime.timedelta(days=int(self.valid_days))  # Set by user

        # Build certificate
        cert_builder = x509.CertificateBuilder()
        cert_builder = cert_builder.subject_name(subject)
        cert_builder = cert_builder.issuer_name(issuer)
        cert_builder = cert_builder.public_key(self.private_key.public_key())
        cert_builder = cert_builder.serial_number(x509.random_serial_number())
        cert_builder = cert_builder.not_valid_before(valid_from)
        cert_builder = cert_builder.not_valid_after(valid_to)

        # Add SAN (Subject Alternative Names) if any
        if self.san_names:
            san_list = [x509.DNSName(name) for name in self.san_names]
            cert_builder = cert_builder.add_extension(
                x509.SubjectAlternativeName(san_list),
                critical=False)

        # Add basic constraints (self-signed certificate is a CA certificate)
        cert_builder = cert_builder.add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True)

         # Add KeyUsage
        cert_builder = cert_builder.add_extension(x509.KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=True,
            crl_sign=True,
            encipher_only=False,
            decipher_only=False),critical=True)

        # Self-sign the certificate with its own private key
        self.cert = cert_builder.sign(
            private_key=self.private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend())
        return self.cert

    def serialize_private_key(self, passphrase=None):
        """Serializes the private key to PEM format. Optionally encrypts it using a passphrase."""
        if passphrase:
            encryption = serialization.BestAvailableEncryption(passphrase.encode())
        else:
            encryption = serialization.NoEncryption()

        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=encryption)

    def serialize_public_key(self):
        """Serializes the public key to PEM format"""
        return self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def serialize_certificate(self):
        """Serializes the certificate to PEM format."""
        return self.cert.public_bytes(serialization.Encoding.PEM)

class X509SelfSignedWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About X509 Self Signed Certificate"
        msgbox_txt = (
        "A self-signed X.509 certificate is a digital certificate that is signed "
        "by the same entity it certifies, rather than by a third-party certificate "
        "authority (CA). Self-signed certificates are often used in testing, "
        "local development, or internal applications where trusted CA validation "
        "isn’t necessary. X.509 is a standard for public key infrastructure (PKI) "
        "and defines the format of public key certificates. Each certificate contains "
        "a subject, a public key, issuer information, validity dates, and a "
        "digital signature. In a self-signed certificate, the entity (user or organization) "
        "that issues the certificate is also the one that signs it. This means the Issuer "
        "and Subject fields are identical. This approach eliminates the need for a CA, "
        "making it quick and free to generate but less secure outside of trusted environments. <br>"
        "While self-signed certificates provide encryption, they don’t verify "
        "the identity of the server. Thus, they should be used only when there’s an implicit "
        "trust in the certificate holder, like in private or controlled environments."
        "<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/X.509>Wikipedia</a><br>"
        "<a href=https://workos.com/blog/x509-certificate>WorkOs</a>")

        self.setWindowTitle("X509 Self Signed Certificate")
        self.setFixedSize(700, 700)

        state_or_province_label = QLabel("State/Province:", parent=self)
        state_or_province_label.setGeometry(150, 10, 110, 50)
        self.state_or_province_input = DefaultQLineEditStyle(parent=self, placeholder_text="e.g: California")
        self.state_or_province_input.setGeometry(10, 60, 325, 50)

        locality_label = QLabel("Locality:", parent=self)
        locality_label.setGeometry(450, 10, 100, 50)
        self.locality_input = DefaultQLineEditStyle(parent=self, placeholder_text="e.g: San Fransisco")
        self.locality_input.setGeometry(350, 60, 340, 50)

        organization_label = QLabel("Organization:", parent=self)
        organization_label.setGeometry(150, 130, 100, 50)
        self.organization_input = DefaultQLineEditStyle(parent=self, placeholder_text="e.g: My Organization")
        self.organization_input.setGeometry(10, 180, 325, 50)

        common_name_label = QLabel("Common name:", parent=self)
        common_name_label.setGeometry(450, 130, 110, 50)
        self.common_name_input = DefaultQLineEditStyle(parent=self, placeholder_text="e.g: www.example.com")
        self.common_name_input.setGeometry(350, 180, 340, 50)

        country_name_label = QLabel("Country name:", parent=self)
        country_name_label.setGeometry(10, 230, 120, 50)
        country_names_list = ['US', 'GR', 'RO', 'BR', 'FR', 'DE', 'IT', 'ES', 'RU', 'CN', 
                      'JP', 'IN', 'AU', 'CA', 'MX', 'AR', 'CL', 'CO', 'NL', 'SE', 
                      'CH', 'BE', 'NO', 'DK', 'FI', 'PT', 'PL', 'CZ', 'HU', 'IE', 
                      'AT', 'NZ', 'ZA', 'EG', 'NG', 'KE', 'TZ', 'SA', 'AE', 'TR', 
                      'KR', 'TH', 'MY', 'SG', 'ID', 'VN', 'PH', 'IL', 'UA', 'BY']

        self.country_name_options = DefaultQComboBoxStyle(parent=self, items=country_names_list, visible_items=10)
        self.country_name_options.setGeometry(10, 280, 120, 50)

        valid_days_label = QLabel("Valid days:", parent=self)
        valid_days_label.setGeometry(200, 230, 120, 50)
        self.valid_days_input = DefaultQLineEditStyle(parent=self, placeholder_text="Default: 730", int_validator=True)
        self.valid_days_input.setGeometry(200, 280, 100, 50)

        san_names_label = QLabel("SAN (subject alternative names):", parent=self)
        san_names_label.setGeometry(450, 230, 240, 50)
        self.san_names_input = DefaultQLineEditStyle(parent=self, placeholder_text="Optional field (separate names with comma)")
        self.san_names_input.setGeometry(350, 280, 340, 50)

        passphrase_label = QLabel("Give passphrase:", parent=self)
        passphrase_label.setGeometry(150, 350, 150, 50)
        self.passphrase_input = DefaultQLineEditStyle(parent=self, placeholder_text="Optional - e.g: mysecurepass")
        self.passphrase_input.setGeometry(100, 400, 250, 50)

        generate_button = DefaultButtonStyle("Generate", parent=self, bold=True, command=self.call_x509)
        generate_button.setGeometry(400, 400, 100, 50)

        self.saved_files_path = QTextEdit(parent=self)
        self.saved_files_path.setGeometry(100, 540, 500, 100)
        self.saved_files_path.setReadOnly(True)

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(theme_mode)
        
    def call_x509(self):
        try:
            downloads_path = Path.home() / "Downloads" / "x509_self_signed"
            downloads_path.mkdir(parents=True, exist_ok=True)

            if not self.state_or_province_input.text():
                raise ValueError('No state or province entered.')
            elif not self.locality_input.text():
                raise ValueError('No locality entered.')
            elif not self.organization_input.text():
                raise ValueError('No organization entered.')
            elif not self.common_name_input.text():
                raise ValueError('No common name entered.')

            country = self.country_name_options.currentText()
            state_province = self.state_or_province_input.text()
            locality = self.locality_input.text()
            organization = self.organization_input.text()
            common_name = self.common_name_input.text()
            san_names = [name.strip() for name in self.san_names_input.text().split(',')] if self.san_names_input.text() else []
            valid_days = self.valid_days_input.text()
            passphrase = self.passphrase_input.text()

            generator = X509SelfSignedCertGenerator(
                country_name = country,
                state_or_province_name = state_province,
                locality_name = locality,
                organization_name = organization,
                common_name = common_name,
                san_names = san_names if san_names else [],
                valid_days = int(valid_days) if valid_days else 730)

            # Generate private key and self-signed certificate
            generator.generate_self_signed_cert()

            # Serialize and save private key, public key and certificate to files
            with open(downloads_path / "private_key.pem", "wb") as key_file:
                key_file.write(generator.serialize_private_key(passphrase=passphrase))

            with open(downloads_path / "certificate.pem", "wb") as cert_file:
                cert_file.write(generator.serialize_certificate())
            
            with open(downloads_path / "public_key.pem", "wb") as pub_file:
                pub_file.write(generator.serialize_public_key())
            
            # Show a message box with option to open Downloads folder
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Success')
            msg_box.setText(f'Certificate and keys successfully generated and saved at:\n{downloads_path}')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            open_folder_btn = msg_box.addButton('Open Folder', QMessageBox.ButtonRole.ActionRole)
            msg_box.exec()
            if msg_box.clickedButton() == open_folder_btn:
                self.open_downloads_folder(downloads_path)
            
            self.saved_files_path.clear()
            self.saved_files_path.setHtml(f"<b>Private key, Public key and Certificate path:</b><br>{downloads_path}")
            self.saved_files_path.show()    

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def open_downloads_folder(self, downloads_path):
        # Open the Downloads folder using the appropriate command for the OS
        if sys.platform == 'win32':
            os.startfile(downloads_path)
        elif sys.platform == 'darwin':  # macOS
            QProcess.execute('open', [str(downloads_path)])
        else:  # Linux and other Unix-like systems
            QProcess.execute('xdg-open', [str(downloads_path)])
