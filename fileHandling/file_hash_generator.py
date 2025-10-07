from PyQt6.QtWidgets            import QWidget, QTextEdit, QMessageBox, QFileDialog
from DefaultStyles.button_style import DefaultButtonStyle, DefaultAboutButtonStyle
from pathlib                    import Path
import os, hashlib, time, platform

class HashFilesWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About File Hash Generator"
        msgbox_txt = """<p>
        The <b>File Hash Generator</b> calculates cryptographic hash values 
        for any file. Hashes are unique digital fingerprints used to verify 
        file integrity and detect tampering.
        </p>
        <h3>Supported Algorithms:</h3>
        <ul>
          <li><b>MD5</b> – Fast, legacy checksum</li>
          <li><b>SHA-1</b> – Commonly used for file verification</li>
          <li><b>SHA-256</b> – Modern secure hash standard</li>
          <li><b>SHA-512</b> – High-strength variant for sensitive data</li>
        </ul>
        <p>Use this tool to confirm that files are identical or unaltered after download, transfer, or modification.</p>"""

        self.setWindowTitle("File Hash Generator")
        self.setFixedSize(700, 600)

        select_file_button = DefaultButtonStyle(
            'Select File for Hashing',
            parent=self,
            bold=True,
            command=self.select_file)
        select_file_button.setGeometry(50, 30, 250, 50)

        generate_hash_button = DefaultButtonStyle(
            'Generate Hashes',
            parent=self,
            bold=True,
            command=self.generate_hashes)
        generate_hash_button.setGeometry(340, 30, 200, 50)

        save_button = DefaultButtonStyle(
            'Save Hash Report',
            parent=self,
            bold=True,
            command=self.save_hash_report)
        save_button.setGeometry(260, 500, 180, 40)

        self.hash_display = QTextEdit(parent=self)
        self.hash_display.setGeometry(10, 100, 680, 380)
        self.hash_display.setReadOnly(True)
        self.hash_display.hide()

        # About Button
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select a File to Hash')
        if file_path:
            self.selected_file = file_path
            QMessageBox.information(self, 'File Selected', f'Selected file: {file_path}')

    def generate_hashes(self):
        try:
            if not hasattr(self, 'selected_file'):
                raise ValueError("Please select a file first.")

            file_path = self.selected_file
            start_time = time.time()

            hashes = {
                'MD5': self.compute_hash(file_path, 'md5'),
                'SHA-1': self.compute_hash(file_path, 'sha1'),
                'SHA-256': self.compute_hash(file_path, 'sha256'),
                'SHA-512': self.compute_hash(file_path, 'sha512'),}

            elapsed = time.time() - start_time
            file_size = os.path.getsize(file_path)

            result_html = f"""
            <h2>File Hash Report</h2>
            <b>File:</b> {os.path.basename(file_path)}<br>
            <b>Path:</b> {file_path}<br>
            <b>Size:</b> {file_size:,} bytes<br>
            <b>Platform:</b> {platform.system()} {platform.release()}<br>
            <b>Time Taken:</b> {elapsed:.2f} seconds<br><br>
            <b>MD5:</b> {hashes['MD5']}<br>
            <b>SHA-1:</b> {hashes['SHA-1']}<br>
            <b>SHA-256:</b> {hashes['SHA-256']}<br>
            <b>SHA-512:</b> {hashes['SHA-512']}<br>"""
            self.hash_display.setHtml(result_html)
            self.hash_display.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', f'An unexpected error occurred:\n{e}')

    def compute_hash(self, file_path, algo):
        """Compute file hash using the specified algorithm."""
        h = hashlib.new(algo)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def save_hash_report(self):
        try:
            if not self.hash_display.toPlainText():
                raise ValueError("No hashes to save. Please generate them first.")
            
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                'Save Hash Report',
                str(Path.home() / "Downloads" / "hash_report.txt"))
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(self.hash_display.toPlainText())
                QMessageBox.information(self, 'Saved', f'Hash report saved to:\n{save_path}')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Save Error', str(e))
