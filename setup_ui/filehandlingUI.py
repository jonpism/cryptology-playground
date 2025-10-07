from PyQt6 import QtWidgets, QtCore, QtGui
from DefaultStyles.button_style import DefaultButtonStyle

class FileHandlingPageUI:

    def __init__(self, parent=None):
        self.parent = parent
        self.setup_file_handling_ui()

    def setup_file_handling_ui(self):
        """Set up the file handling page, label, and buttons."""
        self.FileHandlingPage = QtWidgets.QWidget(parent=self.parent)
        self.FileHandlingPage.setObjectName("FileHandlingPage")

        self.FileHandlingLabel = QtWidgets.QLabel(parent=self.FileHandlingPage)
        self.FileHandlingLabel.setGeometry(QtCore.QRect(10, 0, 1041, 51))
        self.FileHandlingLabel.setText("File Handling")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.FileHandlingLabel.setFont(font)
        self.FileHandlingLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.FileHandlingLabel.setObjectName("FileHandlingLabel")

        self.create_file_handling_buttons()

    def create_file_handling_buttons(self):
        button_data = [
            "FERNET File Encryption",
            "FERNET File Decryption",
            "CSV to JSON",
            "JSON to CSV",
            "PNG/JPEG to PDF",
            "PDF to PNG/JPEG",
            "Exif Images",
            "Zip File with password",
            "Zip Folder with password",
            "Brute force zip files*",
            "Disassemble .exe files",
            "Decompile .pyc files",
            "JSON to MessagePack",
            "MessagePack to JSON",
            "JSON to XML",
            "XML to JSON",
            "Python Code Disassembler",
            "File Type Detector",
            "PGP Encryptor",
            "PGP Decryptor",
            "Decode .txt files",
            "xxd Hex Dump Tool",
            "File Metadata Extractor",
            "File Hash Generator",
            "Compare File Hashes"]

        object_names = [
            "FernetFileEncButton",
            "FernetFileDecButton",
            "CSVtoJSONButton",
            "JSONtoCSVButton",
            "Img2PDFButton",
            "PDF2ImgButton",
            "ExifImagesButton",
            "ZipFileWithPwdButton",
            "ZipFolderWithPwdButton",
            "BfPwdProtectedButton",
            "DisExeFilesButton",
            "DecompilePycButton",
            "JSONtoMsgPackButton",
            "MsgPacktoJSONButton",
            "JSONtoXMLButton",
            "XMLtoJSONBUtton",
            "PyCodeDisassemblerButton",
            "FileTypeDetectorButton",
            "PGPEncryptorButton",
            "PGPDecryptorButton",
            "DecodeTxtFilesButton",
            "xxdHexDumpButton",
            "FileMetadataExtractorButton",
            "HashFilesButton",
            "CompareFileHashesButton"
            ]

        self.filehandling_buttons = {}
        start_x = 20
        start_y = 80
        btn_width = 220
        btn_height = 40
        h_spacing = 40
        v_spacing = 30
        max_cols = 4

        for index, (text, name) in enumerate(zip(button_data, object_names)):
            row = index // max_cols
            col = index % max_cols
            x = start_x + col * (btn_width + h_spacing)
            y = start_y + row * (btn_height + v_spacing)

            button = DefaultButtonStyle(text, parent=self.FileHandlingPage, object_name=name)
            button.setGeometry(QtCore.QRect(x, y, btn_width, btn_height))
            self.filehandling_buttons[name] = button
