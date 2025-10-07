from PyQt6.QtWidgets            import QWidget, QTextEdit, QMessageBox, QFileDialog
from DefaultStyles.button_style import DefaultButtonStyle, DefaultAboutButtonStyle
from PIL                        import Image
from pathlib                    import Path

class FileStegToolWindow(QWidget):
    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About File Steganography Tool"
        msgbox_txt = """<p>
        The <b>File Steganography Tool</b> hides secret data within image files using 
        <b>Least Significant Bit (LSB)</b> steganography.  
        You can embed text or small files inside a PNG or BMP without visible changes.</p>
        <h3>Key Features:</h3>
        <ul>
          <li>Embed messages or files within images</li>
          <li>Extract hidden data from stego images</li>
          <li>Supports PNG and BMP formats</li>
          <li>Optional password protection</li>
        </ul>
        <p>
        <b>Note:</b> Use responsibly. This tool is for educational and security research purposes only.</p>"""

        self.setWindowTitle("File Steganography Tool")
        self.setFixedSize(700, 500)

        select_cover_button = DefaultButtonStyle(
            'Select Cover Image', parent=self, bold=True, command=self.select_cover_image)
        select_cover_button.setGeometry(50, 30, 200, 50)

        select_secret_button = DefaultButtonStyle(
            'Select File to Hide', parent=self, bold=True, command=self.select_secret_file)
        select_secret_button.setGeometry(270, 30, 200, 50)

        encode_button = DefaultButtonStyle(
            'Encode/Save Image', parent=self, bold=True, command=self.encode_steg)
        encode_button.setGeometry(490, 30, 150, 50)

        self.status_display = QTextEdit(parent=self)
        self.status_display.setGeometry(10, 120, 680, 80)
        self.status_display.setReadOnly(True)
        self.status_display.hide()

        decode_button = DefaultButtonStyle(
            'Decode Hidden Data', parent=self, bold=True, command=self.decode_steg)
        decode_button.setGeometry(250, 250, 200, 50)

        self.decoding_status_display = QTextEdit(parent=self)
        self.decoding_status_display.setGeometry(10, 330, 680, 80)
        self.decoding_status_display.setReadOnly(True)
        self.decoding_status_display.hide()

        # About Button
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def select_cover_image(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Select Cover Image', filter="Images (*.png *.bmp)")
        if path:
            self.cover_image = path
            QMessageBox.information(self, 'Image Selected', f'Cover image: {path}')

    def select_secret_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Select File to Hide')
        if path:
            self.secret_file = path
            QMessageBox.information(self, 'File Selected', f'Secret file: {path}')

    def encode_steg(self):
        try:
            if not hasattr(self, 'cover_image') or not hasattr(self, 'secret_file'):
                raise ValueError("Please select both a cover image and a file to hide.")

            img = Image.open(self.cover_image)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            data = open(self.secret_file, 'rb').read()
            bin_data = ''.join(format(byte, '08b') for byte in data)
            data_len = len(bin_data)
            pixels = img.load()

            width, height = img.size
            total_pixels = width * height * 3
            if data_len + 32 > total_pixels:
                raise ValueError("File too large to hide in this image.")

            # Store message length in first 32 bits
            len_bin = format(data_len, '032b')
            full_data = len_bin + bin_data
            data_index = 0

            for y in range(height):
                for x in range(width):
                    if data_index >= len(full_data):
                        break
                    r, g, b = pixels[x, y]
                    r = (r & ~1) | int(full_data[data_index]) if data_index < len(full_data) else r; data_index += 1
                    g = (g & ~1) | int(full_data[data_index]) if data_index < len(full_data) else g; data_index += 1
                    b = (b & ~1) | int(full_data[data_index]) if data_index < len(full_data) else b; data_index += 1
                    pixels[x, y] = (r, g, b)
                if data_index >= len(full_data):
                    break

            save_path = str(Path.home() / "Downloads" / "steg_image.png")
            img.save(save_path)

            self.status_display.setHtml(
                f"<h3>File successfully hidden inside image!</h3><b>Saved as:</b> {save_path}")
            self.status_display.show()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Encoding failed: {str(e)}")

    def decode_steg(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, 'Select Steg Image', filter="Images (*.png *.bmp)")
            if not path:
                return

            img = Image.open(path).convert('RGB')
            pixels = list(img.getdata())

            # collect LSBs
            lsb_bits = []
            for r, g, b in pixels:
                lsb_bits.append(str(r & 1))
                lsb_bits.append(str(g & 1))
                lsb_bits.append(str(b & 1))

            if len(lsb_bits) < 32:
                raise ValueError("Image too small or contains no hidden data.")

            # first 32 bits is payload length in bits
            header_bits = ''.join(lsb_bits[:32])
            payload_len_bits = int(header_bits, 2)
            total_needed = 32 + payload_len_bits
            if len(lsb_bits) < total_needed:
                raise ValueError(f"Image does not contain the full payload. "
                                 f"Expected {payload_len_bits} payload bits but only {len(lsb_bits)-32} are present.")

            payload_bits = lsb_bits[32:32 + payload_len_bits]

            # convert bits to bytes
            payload_bytes = bytearray()
            for i in range(0, len(payload_bits), 8):
                byte = int(''.join(payload_bits[i:i+8]), 2)
                payload_bytes.append(byte)

            save_path, _ = QFileDialog.getSaveFileName(
                self, 'Save Extracted Payload', str(Path.home() / "Downloads" / "extracted_secret.bin"))
            if not save_path:
                return
            with open(save_path, 'wb') as f:
                f.write(payload_bytes)

            result_html = (f"<h3>Hidden file extracted!</h3>"
                           f"<b>Saved as:</b> {save_path}<br>"
                           f"<b>Extracted size:</b> {len(payload_bytes)} bytes<br>")

            # if we encoded in same session, compare hashes
            try:
                extracted_hash = self._file_sha256(save_path)
                result_html += f"<b>Extracted SHA256:</b> {extracted_hash}<br>"
                if self.secret_file:
                    original_hash = self._file_sha256(self.secret_file)
                    match = (original_hash == extracted_hash)
                    result_html += f"<b>Original SHA256:</b> {original_hash}<br>"
                    result_html += f"<b>Match with original:</b> {'Yes' if match else 'No'}<br>"
            except Exception:
                pass
            
            self.decoding_status_display.clear()
            self.decoding_status_display.setHtml(result_html)
            self.decoding_status_display.show()

        except Exception as e:
            QMessageBox.critical(self, 'Decoding Error', str(e))


