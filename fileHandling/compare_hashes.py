from PyQt6.QtWidgets import QWidget, QTextEdit, QMessageBox, QFileDialog
from DefaultStyles.button_style import DefaultButtonStyle, DefaultAboutButtonStyle
import os, hashlib, platform, time

class CompareFileHashesWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About File Hash Comparator"
        msgbox_txt = """<p>
        The <b>File Hash Comparator</b> verifies whether two files are identical 
        by computing and comparing their cryptographic hash values.
        </p>
        <h3>Supported Algorithms:</h3>
        <ul>
          <li><b>MD5</b> – Fast checksum comparison</li>
          <li><b>SHA-1</b> – Common integrity verification hash</li>
          <li><b>SHA-256</b> – Modern secure standard for binary equality</li>
        </ul>
        <p>
        If all hashes match, the files are guaranteed to be identical.  
        This is useful for checking if backups, transfers, or downloads are unmodified.</p>"""

        self.setWindowTitle("Compare File Hashes")
        self.setFixedSize(700, 600)

        select_file1_button = DefaultButtonStyle(
            'Select First File',
            parent=self,
            bold=True,
            command=self.select_first_file)
        select_file1_button.setGeometry(50, 30, 200, 50)

        select_file2_button = DefaultButtonStyle(
            'Select Second File',
            parent=self,
            bold=True,
            command=self.select_second_file)
        select_file2_button.setGeometry(270, 30, 200, 50)

        compare_button = DefaultButtonStyle(
            'Compare Files',
            parent=self,
            bold=True,
            command=self.compare_files)
        compare_button.setGeometry(490, 30, 150, 50)

        self.result_display = QTextEdit(parent=self)
        self.result_display.setGeometry(10, 100, 680, 380)
        self.result_display.setReadOnly(True)
        self.result_display.hide()

        # About Button
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def select_first_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select First File')
        if file_path:
            self.file1 = file_path
            QMessageBox.information(self, 'File Selected', f'First file: {file_path}')

    def select_second_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Second File')
        if file_path:
            self.file2 = file_path
            QMessageBox.information(self, 'File Selected', f'Second file: {file_path}')

    def compute_hash(self, file_path, algo='sha256'):
        h = hashlib.new(algo)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def compare_files(self):
        try:
            if not hasattr(self, 'file1') or not hasattr(self, 'file2'):
                raise ValueError("Please select both files before comparing.")

            start_time = time.time()
            hashes = {}

            for algo in ['md5', 'sha1', 'sha256']:
                hashes[algo] = {
                    'file1': self.compute_hash(self.file1, algo),
                    'file2': self.compute_hash(self.file2, algo)}

            identical = all(
                hashes[a]['file1'] == hashes[a]['file2']
                for a in hashes)

            elapsed = time.time() - start_time
            result_color = "green" if identical else "red"
            verdict = "Files are identical!" if identical else "Files differ!"

            result_html = f"""
            <h2>File Hash Comparison Report</h2>
            <b>File 1:</b> {os.path.basename(self.file1)}<br>
            <b>Path 1:</b> {self.file1}<br><br>
            <b>File 2:</b> {os.path.basename(self.file2)}<br>
            <b>Path 2:</b> {self.file2}<br>
            <hr>
            <b>Platform:</b> {platform.system()} {platform.release()}<br>
            <b>Comparison Time:</b> {elapsed:.2f} seconds<br>
            <hr>
            <b>MD5:</b><br>
            File 1: {hashes['md5']['file1']}<br>
            File 2: {hashes['md5']['file2']}<br><br>
            <b>SHA-1:</b><br>
            File 1: {hashes['sha1']['file1']}<br>
            File 2: {hashes['sha1']['file2']}<br><br>
            <b>SHA-256:</b><br>
            File 1: {hashes['sha256']['file1']}<br>
            File 2: {hashes['sha256']['file2']}<br>
            <hr>
            <h3 style='color:{result_color}'>{verdict}</h3>"""

            self.result_display.setHtml(result_html)
            self.result_display.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', f'An unexpected error occurred:\n{e}')
