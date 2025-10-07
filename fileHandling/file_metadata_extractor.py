from PyQt6.QtWidgets            import QWidget, QTextEdit, QMessageBox, QFileDialog
from DefaultStyles.button_style import DefaultButtonStyle, DefaultAboutButtonStyle
from pathlib                    import Path
import os, mimetypes, hashlib, time, platform, stat, math, zipfile, tarfile

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    Image = None

class FileMetadataExtractorWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About File Metadata Extractor"
        msgbox_txt = """<p>
        The <b>File Metadata Extractor</b> provides an in-depth view of a file's internal and system-level attributes.
        It identifies key information such as file hashes, EXIF data, compression details, and more.</p>
        <h3>Key Features:</h3>
        <ul>
          <li><b>File System Info:</b> Size, timestamps, permissions, owner, inode</li>
          <li><b>Security Info:</b> SHA256, MD5 hashes, entropy estimation</li>
          <li><b>Content Info:</b> MIME type, file type detection</li>
          <li><b>Media Metadata:</b> EXIF, audio/video duration, codecs</li>
          <li><b>Document Metadata:</b> PDF or DOCX properties</li>
        </ul>"""

        self.setWindowTitle("File Metadata Extractor")
        self.setFixedSize(750, 650)

        select_file_button = DefaultButtonStyle(
            'Select File for Metadata Extraction',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(50, 30, 320, 50)

        extract_button = DefaultButtonStyle(
            'Extract Metadata',
            parent=self,
            bold=True, command=self.extract_metadata)
        extract_button.setGeometry(400, 30, 200, 50)

        save_button = DefaultButtonStyle(
            'Save Metadata Report',
            parent=self,
            bold=True, command=self.save_metadata)
        save_button.setGeometry(290, 560, 180, 40)

        self.metadata_display = QTextEdit(parent=self)
        self.metadata_display.setGeometry(10, 100, 730, 440)
        self.metadata_display.setReadOnly(True)
        self.metadata_display.hide()

        # About button
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(690, 600, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select a File for Metadata Extraction')
        if file_path:
            self.selected_file = file_path
            QMessageBox.information(self, 'File Selected', f'Selected file: {file_path}')

    def extract_metadata(self):
        try:
            if not hasattr(self, 'selected_file'):
                raise ValueError("Please select a file first.")

            file_path = self.selected_file
            stats = os.stat(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)

            metadata_sections = []

            # General Info
            general_info = f"""
            <h2>General File Info</h2>
            <b>Name:</b> {os.path.basename(file_path)}<br>
            <b>Path:</b> {file_path}<br>
            <b>Size:</b> {stats.st_size:,} bytes<br>
            <b>Created:</b> {time.ctime(stats.st_ctime)}<br>
            <b>Modified:</b> {time.ctime(stats.st_mtime)}<br>
            <b>Accessed:</b> {time.ctime(stats.st_atime)}<br>
            <b>Permissions:</b> {stat.filemode(stats.st_mode)}<br>
            <b>Owner UID:</b> {stats.st_uid} | <b>GID:</b> {stats.st_gid}<br>
            <b>Inode:</b> {stats.st_ino}<br>
            <b>MIME Type:</b> {mime_type or 'Unknown'}<br>
            <b>Platform:</b> {platform.system()} {platform.release()}<br>
            """
            metadata_sections.append(general_info)

            # Hashes
            sha256_hash = self.compute_hash(file_path, 'sha256')
            md5_hash = self.compute_hash(file_path, 'md5')
            hashes = f"""
            <h2>Hashes & Integrity</h2>
            <b>SHA256:</b> {sha256_hash}<br>
            <b>MD5:</b> {md5_hash}<br>"""
            metadata_sections.append(hashes)

            # Entropy
            entropy = self.file_entropy(file_path)
            metadata_sections.append(f"<h2>File Entropy</h2><b>Entropy:</b> {entropy:.4f}<br>")

            # Type-Specific Metadata
            type_meta = self.get_type_specific_metadata(file_path, mime_type)
            if type_meta:
                metadata_sections.append(type_meta)

            full_metadata = "<hr>".join(metadata_sections)
            self.metadata_display.setHtml(full_metadata)
            self.metadata_display.show()

        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', f'An unexpected error occurred:\n{e}')

    def compute_hash(self, file_path, algo='sha256'):
        h = hashlib.new(algo)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    def file_entropy(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        if not data:
            return 0.0
        byte_counts = [0] * 256
        for b in data:
            byte_counts[b] += 1
        entropy = 0.0
        for count in byte_counts:
            if count:
                p = count / len(data)
                entropy -= p * math.log2(p)
        return entropy

    def get_type_specific_metadata(self, file_path, mime_type):
        """Extract additional metadata depending on file type"""
        try:
            # Images (EXIF)
            if Image and mime_type and mime_type.startswith("image"):
                with Image.open(file_path) as img:
                    exif_data = img._getexif() or {}
                    if exif_data:
                        exif_html = "<h2>Image Metadata (EXIF)</h2>"
                        for tag_id, value in exif_data.items():
                            tag = TAGS.get(tag_id, tag_id)
                            exif_html += f"<b>{tag}:</b> {value}<br>"
                        return exif_html

            # ZIP / TAR archives
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, 'r') as z:
                    info_html = f"<h2>ZIP Archive Info</h2><b>Contained Files:</b> {len(z.infolist())}<br>"
                    total_uncompressed = sum(i.file_size for i in z.infolist())
                    total_compressed = sum(i.compress_size for i in z.infolist())
                    ratio = 1 - (total_compressed / total_uncompressed) if total_uncompressed else 0
                    info_html += f"<b>Compression Ratio:</b> {ratio:.2%}<br>"
                    return info_html

            if tarfile.is_tarfile(file_path):
                with tarfile.open(file_path) as tar:
                    members = tar.getmembers()
                    return f"<h2>TAR Archive Info</h2><b>Contained Files:</b> {len(members)}<br>"

        except Exception as e:
            return f"<h3>Could not extract type-specific metadata:</h3>{str(e)}"

    def save_metadata(self):
        try:
            if not self.metadata_display.toPlainText():
                raise ValueError("No metadata to save. Please extract metadata first.")
            
            save_path, _ = QFileDialog.getSaveFileName(
                self, 'Save Metadata Report', str(Path.home() / "Downloads" / "metadata_report.txt"))
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(self.metadata_display.toPlainText())
                QMessageBox.information(self, 'Saved', f'Metadata report saved to:\n{save_path}')
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Save Error', str(e))
