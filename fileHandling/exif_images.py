from PyQt6.QtWidgets            import QMessageBox, QTextEdit
from DefaultStyles.button_style import DefaultButtonStyle
from PIL                        import Image
from PIL.ExifTags               import TAGS
from .file_conversion           import FileConversionWindow
from exiftool                   import ExifToolHelper
import os

'''
to work in ubuntu:
sudo apt install libimage-exiftool-perl
sudo apt install curl perl kame -y
curl -L https://cpanmin.us | perl --sudo App::cpanminus
sudo cpanm Image::ExifTool
check version (> 12.7): exiftool -ver'''

class ExifImageWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About EXIF"
        about_text = ("<p><b>EXIF</b> (Exchangeable Image File Format) is a standard that stores metadata "
    "within image and audio files, commonly found in formats such as <code>.jpg</code>, "
    "<code>.tiff</code>, <code>.png</code>, and <code>.heic</code>. This metadata is "
    "automatically recorded by digital cameras, smartphones, and some editing software.</p>"
    "<p>EXIF data can include information such as:</p>"
    "<ul>"
        "<li>Camera model and manufacturer</li>"
        "<li>Date and time the photo was taken</li>"
        "<li>Exposure settings (ISO, shutter speed, aperture)</li>"
        "<li>GPS coordinates (location data)</li>"
        "<li>Orientation and color profile</li>"
    "</ul>"
    "<p>This tool allows you to extract and view EXIF metadata from supported image files, "
    "and optionally save the information to a text file.</p>"
    "<p>Useful links:<br>"
    "<a href='https://en.wikipedia.org/wiki/Exif'>EXIF on Wikipedia</a><br>"
    "<a href='https://exiftool.org/'>Official ExifTool Website</a></p>")

        ax, ay, aw, ah = 650, 350, 50, 50
        file_filter = "Image files (*.png *.jpeg *.jpg *.heic *.gif *.tif)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Exif Images - Extract metadata")
        self.setFixedSize(700, 400)

        select_file_button = DefaultButtonStyle(
            'Select an Image file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        exif_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.exif_data)
        exif_button.setGeometry(450, 50, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 100)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def exif_data(self):
        try:
            if not hasattr(self, 'selected_file'):
                raise ValueError('Please select a file first.')

            helper = ExifToolHelper()  # Use system PATH
            with helper as et:
                metadata = et.get_metadata([self.selected_file])

                if not metadata:
                    QMessageBox.information(self, 'No Metadata', 'No EXIF metadata found in this image.')
                    return

                metadata_file_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'image_metadata.txt')

                metadata_str = "Metadata for the selected image:\n\n"
                for tag, value in metadata[0].items():
                    metadata_str += f"{tag}: {value}\n"

                with open(metadata_file_path, 'w') as f:
                    f.write(metadata_str)

                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('Operation Successful')
                msg_box.setText(f'Metadata saved to:\n{metadata_file_path}')
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                msg_box.exec()

                if msg_box.clickedButton() == open_folder_btn:
                    self.open_downloads_folder()

                self.output_label.clear()
                self.output_label.setHtml(f"<b>Metadata generated and saved at:</b><br> {metadata_file_path}")
                self.output_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except FileNotFoundError:
            QMessageBox.critical(
                self, 'ExifTool Missing',
                "ExifTool is not found. Please install it and ensure it's in your system PATH.\n"
                "https://exiftool.org/")
        except Exception as e:
            QMessageBox.critical(
                self, 'Failed to Extract Metadata',
                f'Error: {str(e)}')
