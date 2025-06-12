from cryptography                               import x509
from cryptography.x509.oid                      import NameOID
from cryptography.hazmat.primitives             import hashes
from cryptography.hazmat.primitives.asymmetric  import rsa
from cryptography.hazmat.primitives             import serialization
from cryptography.hazmat.backends               import default_backend
from PyQt6.QtWidgets                            import QWidget, QLabel, QMessageBox, QTextEdit
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style             import DefaultQComboBoxStyle
from DefaultStyles.qline_edit_style             import DefaultQLineEditStyle
from pathlib                                    import Path

class CSRGenerator:

    def __init__(self, country_name, state_or_province_name, locality_name, organization_name, common_name, key_size=2048):
        self.country_name = country_name
        self.state_or_province_name = state_or_province_name
        self.locality_name = locality_name
        self.organization_name = organization_name
        self.common_name = common_name
        self.key_size = key_size
        self.private_key = None
        self.csr = None

    def generate_private_key(self):
        """
        Generates a private key and stores it in the object.
        """
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend()) # no longer required, can be omitted
        return self.private_key

    def generate_csr(self):
        """
        Generates a CSR using the provided details and the generated private key.
        """
        if not self.private_key:
            self.generate_private_key()

        csr_builder = x509.CertificateSigningRequestBuilder()

        csr_builder = csr_builder.subject_name(x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, self.state_or_province_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, self.locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.organization_name),
            x509.NameAttribute(NameOID.COMMON_NAME, self.common_name)]))

        # extensions: basic constraints, alternative names
        # csr_builder = csr_builder.add_extension(
        #     x509.SubjectAlternativeName([
        #         x509.DNSName("www.example.com"),
        #         x509.DNSName("example.com"),]),
        #     critical=False)

        self.csr = csr_builder.sign(
            private_key=self.private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend())
        return self.csr

    def serialize_private_key(self, passphrase=None):
        """Serializes the private key to PEM format.
        Optionally encrypts it using a passphrase."""
        if passphrase:
            encryption = serialization.BestAvailableEncryption(passphrase.encode())
        else:
            encryption = serialization.NoEncryption()

        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption)

    def serialize_csr(self):
        """Serializes the CSR to PEM format."""
        return self.csr.public_bytes(serialization.Encoding.PEM)

class CSRWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About CSR"
        msgbox_txt = (
        "A Certificate Signing Request (CSR) is a block of encoded text that an individual "
        "or organization submits to a Certificate Authority (CA) when applying for a digital "
        "certificate, like an SSL/TLS certificate. The CSR contains essential information "
        "that helps the CA generate and authenticate the certificate. The CSR includes "
        "the public key that corresponds to the private key generated on the applicant’s server. "
        "This public key will be part of the issued certificate. A CSR is generated and sent "
        "to a CA to apply for an SSL certificate or other types of digital certificates. The CA "
        "verifies the details provided in the CSR to ensure they match the organization "
        "requesting the certificate. Once the verification process is completed, the CA issues "
        "a certificate that the organization can use to secure its communications. "
        "CSRs are encoded in PEM or DER format, with PEM being the more common format in practice.<br><br>"
        "Useful links: <br>"
        "<a href=https://en.wikipedia.org/wiki/Certificate_signing_request>Wikipedia</a><br>"
        "<a href=https://www.sectigo.com/resource-library/what-is-a-certificate-signing-request-csr>Sectigo</a>")

        self.setWindowTitle("Certificate Signing Request")
        self.setFixedSize(700, 800)

        self.downloads_path = str(Path.home() / "Downloads")

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
        country_name_label.setGeometry(50, 230, 120, 50)
        country_names_list = ['US', 'GR', 'RO', 'BR', 'FR', 'DE', 'IT', 'ES', 'RU', 'CN', 
                      'JP', 'IN', 'AU', 'CA', 'MX', 'AR', 'CL', 'CO', 'NL', 'SE', 
                      'CH', 'BE', 'NO', 'DK', 'FI', 'PT', 'PL', 'CZ', 'HU', 'IE', 
                      'AT', 'NZ', 'ZA', 'EG', 'NG', 'KE', 'TZ', 'SA', 'AE', 'TR', 
                      'KR', 'TH', 'MY', 'SG', 'ID', 'VN', 'PH', 'IL', 'UA', 'BY']

        self.country_name_options = DefaultQComboBoxStyle(parent=self, items=country_names_list, visible_items=10)
        self.country_name_options.setGeometry(50, 280, 120, 50)

        passphrase_label = QLabel("Give passphrase:", parent=self)
        passphrase_label.setGeometry(300, 230, 150, 50)
        self.passphrase_input = DefaultQLineEditStyle(parent=self, placeholder_text="Optional - e.g: mysecurepass")
        self.passphrase_input.setGeometry(250, 280, 250, 50)

        generate_button = DefaultButtonStyle("Generate", parent=self, bold=True, command=self.csr)
        generate_button.setGeometry(550, 280, 100, 50)

        self.private_key_textedit = QTextEdit(parent=self)
        self.private_key_textedit.setGeometry(10, 380, 680, 120)
        self.private_key_textedit.setReadOnly(True)
        self.private_key_textedit.hide()

        self.csr_textedit = QTextEdit(parent=self)
        self.csr_textedit.setGeometry(10, 530, 680, 120)
        self.csr_textedit.setReadOnly(True)
        self.csr_textedit.hide()

        self.file_location_textedit = QTextEdit(parent=self)
        self.file_location_textedit.setGeometry(10, 680, 680, 50)
        self.file_location_textedit.setReadOnly(True)
        self.file_location_textedit.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 750, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def csr(self):
        try:
            if not self.state_or_province_input.text():
                raise ValueError('Please enter a state or province.')
            elif not self.locality_input.text():
                raise ValueError('Please enter a locality.')
            elif not self.organization_input.text():
                raise ValueError('Please enter an organization.')
            elif not self.common_name_input.text():
                raise ValueError('Please enter a common name.')

            country = self.country_name_options.currentText()
            state_province = self.state_or_province_input.text()
            locality = self.locality_input.text()
            organization = self.organization_input.text()
            common_name = self.common_name_input.text()
            passphrase = self.passphrase_input.text() # optional

            generator = CSRGenerator(
                country_name = country,
                state_or_province_name = state_province,
                locality_name = locality,
                organization_name = organization,
                common_name = common_name)

            # generate private key and self-signed certificate
            generator.generate_csr()

            try:
                # serialize and save the private key
                private_key_pem = generator.serialize_private_key(passphrase if passphrase else None)
                private_key_path = Path(self.downloads_path) / "private_key.pem"
                with open(private_key_path, "wb") as key_file:
                    key_file.write(private_key_pem)

                # serialize and save the CSR
                csr_pem = generator.serialize_csr()
                csr_path = Path(self.downloads_path) / "csr.pem"
                with open(csr_path, "wb") as csr_file:
                    csr_file.write(csr_pem)

                escaped_key = private_key_pem.decode().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                self.private_key_textedit.clear()
                self.private_key_textedit.setHtml(f"<b>Private Key (PEM Format):</b><br><pre>{escaped_key}</pre>")
                self.private_key_textedit.show()

                escaped_csr = csr_pem.decode().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                self.csr_textedit.clear()
                self.csr_textedit.setHtml(f"<b>Certificate Signing Request (PEM Format):</b><br><pre>{escaped_csr}</pre>")
                self.csr_textedit.show()

                QMessageBox.information(self, 'Success', 'Files generated and saved at downloads folder.')
                self.file_location_textedit.clear()
                self.file_location_textedit.setHtml(f"<b>Files successfully generated and saved at:</b><br> {self.downloads_path}")
                self.file_location_textedit.show()

            except Exception as e:
                QMessageBox.critical(self, 'Unexpected Error', str(e))

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
