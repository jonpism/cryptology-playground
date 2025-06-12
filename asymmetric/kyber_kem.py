from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox, QFileDialog
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qcombo_box_style import DefaultQComboBoxStyle
from kyber_py.kyber                 import Kyber1024, Kyber768, Kyber512
from pathlib                        import Path
import base64, os, binascii

downloads_path = Path.home() / "Downloads" / "kyber_keys"

class KyberKEM:

    def save_files(self, public_key, private_key, ciphertext):
        os.makedirs(downloads_path, exist_ok=True)

        with open(downloads_path / "public_key.bin", "wb") as f:
            f.write(public_key)
        with open(downloads_path / "private_key.bin", "wb") as f:
            f.write(private_key)
        with open(downloads_path / "ciphertext.bin", "wb") as f:
            f.write(ciphertext)

    def load_keys(self, dir_path="kyber_keys"):
        with open(os.path.join(dir_path, "public_key.bin"), "rb") as f:
            public_key = f.read()
        with open(os.path.join(dir_path, "private_key.bin"), "rb") as f:
            private_key = f.read()
        return public_key, private_key

class KyberKEMWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Kyber Key Encapsulation Mechanism"
        msgbox_txt = ""

        self.setWindowTitle("Kyber Key Encapsulation Mechanism (KEM) - Encapsulation")
        self.setFixedSize(700, 700)

        # Kyber variant
        variant_label = QLabel("Kyber Variant:", parent=self)
        variant_label.setGeometry(30, 20, 120, 50)
        self.variant_options = DefaultQComboBoxStyle(parent=self, items=['Kyber512', 'Kyber768', 'Kyber1024'])
        self.variant_options.setGeometry(20, 70, 120, 50)

        # Output format
        output_format_label = QLabel("Output format:", parent=self)
        output_format_label.setGeometry(200, 20, 120, 50)
        self.output_format_options = DefaultQComboBoxStyle(parent=self, items=['Base64', 'Hex', 'Raw'])
        self.output_format_options.setGeometry(200, 70, 120, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.kem_encapsulate)
        submit_button.setGeometry(400, 70, 100, 50)

        self.private_key_label = QTextEdit(parent=self)
        self.private_key_label.setGeometry(10, 150, 680, 100)
        self.private_key_label.setReadOnly(True)
        self.private_key_label.hide()

        self.public_key_label = QTextEdit(parent=self)
        self.public_key_label.setGeometry(10, 280, 680, 100)
        self.public_key_label.setReadOnly(True)
        self.public_key_label.hide()

        self.ciphertext_label = QTextEdit(parent=self)
        self.ciphertext_label.setGeometry(10, 400, 680, 100)
        self.ciphertext_label.setReadOnly(True)
        self.ciphertext_label.hide()

        self.shared_secret_label = QTextEdit(parent=self)
        self.shared_secret_label.setGeometry(10, 520, 680, 100)
        self.shared_secret_label.setReadOnly(True)
        self.shared_secret_label.hide()

        self.saved_keys_label = QTextEdit(parent=self)
        self.saved_keys_label.setGeometry(10, 640, 480, 50)
        self.saved_keys_label.setReadOnly(True)
        self.saved_keys_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def kem_encapsulate(self):
        try:
            variant = self.variant_options.currentText()
            output_format = self.output_format_options.currentText()
            kyber_kem = KyberKEM()

            if variant == 'Kyber512':    
                public_key, private_key = Kyber512.keygen()
                shared_secret, ciphertext = Kyber512.encaps(public_key)
            elif variant == 'Kyber768':
                public_key, private_key = Kyber512.keygen()
                shared_secret, ciphertext = Kyber768.encaps(public_key)
            else:
                public_key, private_key = Kyber1024.keygen()
                shared_secret, ciphertext = Kyber1024.encaps(public_key)

            print(f"Ciphertext Length when encapsulating: {len(ciphertext)}")
            print(f"Private key when encapsulating: {len(private_key)}")

            kyber_kem.save_files(public_key, private_key, ciphertext)
            QMessageBox.information(self, 'Success', f'Keys successfully generated and saved at: {downloads_path}')
            QMessageBox.information(self, 'Success', f'Ciphertext successfully generated and saved at: {downloads_path}')

            def format_options(data):
                if output_format == "Base64":
                    return base64.b64encode(data).decode()
                elif output_format == "Hex":
                    return binascii.hexlify(data).decode()
                else: # raw
                    return data

            self.private_key_label.setHtml(f"<b>Private key ({output_format}):</b><br>{format_options(private_key)}")
            self.public_key_label.setHtml(f"<b>Public key ({output_format}):</b><br>{format_options(public_key)}")
            self.ciphertext_label.setHtml(f"<b>Ciphertext ({output_format}):</b><br>{format_options(ciphertext)}")
            self.shared_secret_label.setHtml(f"<b>Encapsulated Shared Secret ({output_format}):</b><br>{format_options(shared_secret)}")
            self.saved_keys_label.setHtml(f"<b>Keys and ciphertext saved at:</b> {downloads_path}")

            # show all fields
            for widget in [
                self.private_key_label,
                self.public_key_label,
                self.ciphertext_label,
                self.shared_secret_label,
                self.saved_keys_label]:widget.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

# =========================================================================================================================================================

class KyberKEMDecWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Kyber Key Encapsulation Mechanism - Decapsulation"
        msgbox_txt = ""

        self.setWindowTitle("Kyber Key Encapsulation Mechanism (KEM) - Decapsulation")
        self.setFixedSize(700, 700)

        select_ciphertext_button = DefaultButtonStyle(
            'Select ciphertext file',
            parent=self,
            command=self.select_ciphertext_file)
        select_ciphertext_button.setGeometry(30, 50, 200, 50)

        select_prv_key_button = DefaultButtonStyle(
            'Select private key file',
            parent=self,
            command=self.select_prv_key_file)
        select_prv_key_button.setGeometry(250, 50, 200, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.kem_decapsulate)
        submit_button.setGeometry(500, 50, 100, 50)

        self.selected_key_label = QTextEdit(parent=self)
        self.selected_key_label.setGeometry(10, 150, 270, 70)
        self.selected_key_label.setReadOnly(True)
        self.selected_key_label.setHtml(f"<b>Currently selected private key file:</b><br>None")

        self.selected_ciphertext_label = QTextEdit(parent=self)
        self.selected_ciphertext_label.setGeometry(350, 150, 270, 70)
        self.selected_ciphertext_label.setReadOnly(True)
        self.selected_ciphertext_label.setHtml(f"<b>Currently selected ciphertext file:</b><br>None")

        self.shared_secret_b64_label = QTextEdit(parent=self)
        self.shared_secret_b64_label.setGeometry(10, 250, 680, 100)
        self.shared_secret_b64_label.setReadOnly(True)
        self.shared_secret_b64_label.hide

        self.shared_secret_hex_label = QTextEdit(parent=self)
        self.shared_secret_hex_label.setGeometry(10, 360, 680, 100)
        self.shared_secret_hex_label.setReadOnly(True)
        self.shared_secret_hex_label.hide()

        self.shared_secret_raw_label = QTextEdit(parent=self)
        self.shared_secret_raw_label.setGeometry(10, 470, 680, 100)
        self.shared_secret_raw_label.setReadOnly(True)
        self.shared_secret_raw_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def select_prv_key_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Select a file', '', 'Binary Files (*.bin);;All Files (*)')
            if not file_path:
                raise ValueError("No file selected.")
            
            self.private_key_file = file_path
            self.selected_key_label.setHtml(f"<b>Currently selected private key file:</b><br>{file_path}")
            QMessageBox.information(self, 'Private key selected', f'Selected prv key: {file_path}')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
        
    def select_ciphertext_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Select a ciphertext file', '', 'Binary Files (*.bin);;All Files (*)')
            if not file_path:
                raise ValueError("No file selected.")
            
            self.ciphertext_file = file_path
            self.selected_ciphertext_label.setHtml(f"<b>Currently selected ciphertext file:</b><br>{file_path}")
            self.selected_ciphertext_label.show()
            QMessageBox.information(self, 'Ciphertext selected', f'Selected ciphertext: {file_path}')

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def kem_decapsulate(self):
            try:
                if self.ciphertext_file and self.private_key_file:
                    
                    # load ciphertext
                    with open(self.ciphertext_file, "rb") as f:
                        ciphertext = f.read()
                    if len(ciphertext) < 732:
                        raise ValueError(f"Ciphertext file appears invalid (length bytes: {len(ciphertext)}).")

                    # load private key from selected file
                    with open(self.private_key_file, "rb") as f:
                        private_key = f.read()

                    if len(ciphertext) == 1568:
                        shared_secret = Kyber1024.decaps(private_key, ciphertext)
                    elif len(ciphertext) == 768:
                        shared_secret = Kyber512.decaps(private_key, ciphertext)
                    else:
                        shared_secret = Kyber768.decaps(private_key, ciphertext)

                    self.shared_secret_b64_label.clear()
                    self.shared_secret_b64_label.setHtml(f"<b>Shared Secret (Base64):</b>\n{str(base64.b64encode(shared_secret).decode())}")
                    self.shared_secret_b64_label.show()

                    self.shared_secret_hex_label.clear()
                    self.shared_secret_hex_label.setHtml(f"<b>Shared Secret (Hex):</b>\n{str(binascii.hexlify(shared_secret).decode())}")
                    self.shared_secret_hex_label.show()

                    self.shared_secret_raw_label.clear()
                    self.shared_secret_raw_label.setHtml(f"<b>Shared Secret (Raw):</b>\n{str(shared_secret)}")
                    self.shared_secret_raw_label.show()
                
                else:
                    QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')
            except ValueError as ve:
                QMessageBox.warning(self, 'Error', str(ve))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to decapsulate: {str(e)}")
