from PyQt6.QtWidgets                import QMessageBox, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from .file_conversion               import FileConversionWindow
import binascii, os

class FileTypeDetectorWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About File Type Detector Tool"
        about_text = """
        The <b>File Type Detector Tool</b> is a utility designed to identify the possible file type 
        of any selected file by analyzing its binary signature, also known as <i>magic bytes</i>.<br><br>
        Unlike relying on file extensions, which can be misleading or manipulated, this tool reads the 
        first few bytes of the file and compares them against a comprehensive database of known file 
        signatures to determine its actual type.<br><br>
        It supports a wide range of formats including image, video, audio, document, archive, executable,
        font, and database files. This tool is particularly useful for forensic analysis, file recovery, 
        or validation where file integrity and identity are critical."""

        ax, ay, aw, ah = 650, 350, 50, 50
        file_filter = "All Files (*)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("File Type Detector Tool")
        self.setFixedSize(700, 400)

        select_file_button = DefaultButtonStyle(
            'Select a file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        convert_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.detect_file)
        convert_button.setGeometry(450, 50, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 100)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def detect_file(self):
        try:
            if hasattr(self, 'selected_file'):
                detector = FileTypeDetector()
                file_type = detector.detect(self.selected_file)

                self.output_label.clear()
                self.output_label.setHtml(f"<b>Possible file type(s):</b><br>{file_type}")
                self.output_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except FileNotFoundError as fnf:
            QMessageBox.warning(self, 'File not found', str(fnf))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

class FileTypeDetector:

    def __init__(self):
        self.magic_bytes = load_magic_bytes()

    def detect(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")

        with open(file_path, 'rb') as file:
            file_header = file.read(8)
            hex_header = binascii.hexlify(file_header).upper()

            for magic, file_type in self.magic_bytes.items():
                if hex_header.startswith(magic):
                    return file_type

        return 'Unknown file type'

# https://en.wikipedia.org/wiki/List_of_file_signatures
def load_magic_bytes():
    return {
        # Archives & Compression
        b'1F8B08': 'gzip',
        b'504B0304': 'zip',
        b'377ABCAF271C': '7z',
        b'52617221': 'rar',
        b'425A68': 'bz2',
        b'1F9D': 'tar.z',
        b'FD377A58': 'xz',
        b'28B52FFD': 'zlib',
        b'4C5A4950': 'lzop',
        b'03214C18': 'lz4',
        b'4D534346': 'cab',
        b'414C5A01': 'alz',
        b'1A02': 'ace',
        b'5D000080': 'lzo',
        b'377ABCAF': '7z',
        b'7801': 'zlib',

        # Audio formats
        b'664C6143': 'flac',
        b'494433': 'mp3',
        b'4F676753': 'ogg',
        b'FFFB': 'mp3',
        b'FFF3': 'mp3',
        b'FFF2': 'mp3',
        b'FFF1': 'aac',
        b'FFF9': 'aac',
        b'4D546864': 'midi',
        b'2E736E64': 'au',
        b'2321': 'amr',
        b'52494646': 'wav',
        b'57415645': 'wav',
        b'774F4646': 'woff',
        b'774F4632': 'woff2',
        b'1A000000': 'opus',

        # Video formats
        b'1A45DFA3': 'webm',
        b'3026B275': 'wmv',
        b'000001BA': 'mpeg',
        b'000001B3': 'mpeg',
        b'00000018': 'mp4',
        b'0000001C': 'mp4',
        b'464C56': 'flv',
        b'41564920': 'avi',
        b'00000014': 'm4v',
        b'00000020': 'm4a',
        b'1A45DFA3': 'mkv',

        # Images
        b'89504E47': 'png',
        b'FFD8FF': 'jpeg',
        b'47494638': 'gif',
        b'49492A00': 'tiff',
        b'4D4D002A': 'tiff',
        b'52494646': 'webp',
        b'424D': 'bmp',
        b'49492A': 'cr2',
        b'53445058': 'psd',
        b'38425053': 'psb',
        b'4D5A': 'ico',
        b'FFD8FFE0': 'jpg',
        b'FFD8FFE1': 'jpg',
        b'FFD8FFE2': 'jpg',
        b'FFD8FFE3': 'jpg',
        b'49492A00': 'tif',
        b'4D4D002A': 'tif',

        # Documents
        b'25504446': 'pdf',
        b'D0CF11E0': 'doc/xls/ppt',
        b'504B0304': 'docx/xlsx/pptx',
        b'3C68746D6C': 'html',
        b'3C3F786D6C': 'xml',
        b'7B': 'json',
        b'2321': 'sh',
        b'EFBBBF': 'utf-8',
        b'FEFF': 'utf-16-be',
        b'FFFE': 'utf-16-le',
        b'0000FEFF': 'utf-32-be',
        b'FFFE0000': 'utf-32-le',

        # Programming & Executables
        b'7F454C46': 'elf',
        b'4D5A': 'exe/dll',
        b'CAFEBABE': 'class',
        b'2321': 'sh/bash',
        b'EFBBBF': 'utf-8 script',
        b'3C3F7079': 'php',
        b'66747970': 'pyc',
        b'4C01': 'lnk',
        b'2F2A': 'c/cpp',
        b'696E63': 'java',
        b'2D2D': 'lua',
        b'4D5A9000': 'scr',
        b'3C21444F': 'html',
        b'ACED0005': 'ser',
        b'504B0304': 'jar',

        # Font files
        b'774F4646': 'woff',
        b'774F4632': 'woff2',
        b'4F54544F': 'otf',
        b'00010000': 'ttf',

        # Databases
        b'53514C697465': 'sqlite',
        b'00061561': 'msi',
        b'44424648': 'db',
        b'4D444248': 'mdb',
        b'4D534453': 'msd',

        # Other formats
        b'3C21444F43': 'xml/html',
        b'3C3F786D6C': 'xml',
        b'3C21454E54': 'dtd',
        b'3C3F786D6C2076657273696F6E3D': 'xml',
        b'000100005374616E646172642046696C65': 'ttf',
        b'464C4966': 'ifl',
        b'3C3F786D6C2076657273696F6E3D22312E30': 'xml',
        b'4D534346': 'cab',
        b'3758BCAF271C': '7z',
        b'1F8B08': 'gz',
        b'52617221': 'rar',
        b'000001BA': 'mpeg',
        b'494433': 'mp3',
        b'FFF15080': 'aac',
        b'FFF9F050': 'aac',
        b'000001B3': 'mpeg',
        b'3026B275': 'wmv',
        b'664C6143': 'flac',
        b'4F676753': 'ogg',
        b'00000014': 'm4a',
        b'00000020': 'm4v',
        b'00000018': 'mp4',
        b'0000001C': 'mp4',
        b'4D546864': 'midi',
        b'41564920': 'avi',
        b'464C56': 'flv',
        b'1A45DFA3': 'webm',
        b'CAFEBABE': 'class',
        b'EFBBBF': 'utf-8',
        b'FEFF': 'utf-16-be',
        b'FFFE': 'utf-16-le',
        b'0000FEFF': 'utf-32-be',
        b'FFFE0000': 'utf-32-le',
        b'25504446': 'pdf',
        b'D0CF11E0': 'ole2',
        b'504B0304': 'docx/xlsx/pptx',
        b'3C68746D6C': 'html',
        b'3C3F786D6C': 'xml',
        b'7B': 'json',
        b'2321': 'sh',
        b'3C3F7079': 'php',
        b'4C01': 'lnk',
        b'2F2A': 'c/cpp',
        b'696E63': 'java',
        b'2D2D': 'lua',
        b'504B0304': 'jar',
        b'4D5A': 'exe/dll',
        b'7F454C46': 'elf',
        b'774F4646': 'woff',
        b'774F4632': 'woff2',
        b'4F54544F': 'otf',
        b'00010000': 'ttf',
        b'53514C697465': 'sqlite',
        b'4D534453': 'msd',
        b'44424648': 'db',
        b'4D534453': 'msd',
        b'4D444248': 'mdb',
        b'00061561': 'msi',
        b'4C504620': 'lpf',}
