from PyQt6.QtWidgets                import QMessageBox, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from PIL                            import Image
from .file_conversion               import FileConversionWindow
from pdf2image                      import convert_from_path
import os

class Img2PDFWindow(FileConversionWindow):
    
    def __init__(self, theme_mode):
        about_title = "About Images to PDF Conversion"
        about_text = (
            "<b>Images</b> are visual representations of objects or scenes "
            "captured by a device like a camera or created digitally "
            "using software. Supported formats are: JPEG(JPG), PNG, "
            "GIF, TIFF, SVG, BMP <br><br>"
            "<b>PDF:</b> A file format developed by Adobe to present documents "
            " consistently across different devices and platforms. Commonly "
            "used for text documents, forms, presentations, and eBooks. <br><br>"
            "Images can be embedded into PDF files, either as backgrounds, "
            "illustrations, or diagrams. This is common in academic papers, "
            "brochures, and user manuals. ")
        
        ax, ay, aw, ah = 650, 350, 50, 50
        file_filter = "PNG Files JPG Files JPEG Files(*.png *.jpg *.jpeg)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Image to PDF Converter")
        self.setFixedSize(700, 400)

        select_file_button = DefaultButtonStyle(
            'Select an Image file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        convert_button = DefaultButtonStyle("Convert", parent=self, bold=True, command=self.convert_file)
        convert_button.setGeometry(450, 50, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 100)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def convert_file(self):
        if hasattr(self, 'selected_file'):
            try:
                file_extension = os.path.splitext(self.selected_file)[1].lower()

                if file_extension in ['.png', '.jpeg', '.jpg']:

                    pdf_file_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'pdf_converted_file.pdf')

                    image = Image.open(self.selected_file)

                    # PDFs don't support alpha channels
                    if image.mode in ("RGBA", "LA"):
                        image = image.convert("RGB")

                    # Save the image as a PDF
                    image.save(pdf_file_path, "PDF", resolution=100.0)

                    # Show a custom message box with a button to open the Downloads folder
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Conversion Successful')
                    msg_box.setText(f'File converted and saved at: {pdf_file_path}')
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

                    # Add a custom button for opening the Downloads folder
                    open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                    msg_box.exec()

                    # If the user clicks "Open Downloads", open the Downloads folder
                    if msg_box.clickedButton() == open_folder_btn:
                        self.open_downloads_folder()
                    
                    self.output_label.clear()
                    self.output_label.setHtml(f"<b>{file_extension} file converted to PDF. PDF file created and saved at:</b><br>{pdf_file_path}")
                    self.output_label.show()
                else:
                    QMessageBox.warning(
                        self, 'Invalid File Type',
                        'Please select a PNG/JPEG/JPG file for conversion.')

            except Exception as e:
                QMessageBox.critical(
                    self, 'Conversion Failed',
                    f'An error occurred during conversion: {str(e)}')
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')

# ==================================================================================================================

class PDF2ImgWindow(FileConversionWindow):
    def __init__(self, theme_mode):
        about_title = "About PDF to Images Conversion"
        about_text = (
            "<b>Images</b> are visual representations of objects or scenes "
            "captured by a device like a camera or created digitally "
            "using software. Supported formats are: JPEG(JPG), PNG, "
            "GIF, TIFF, SVG, BMP <br><br>"
            "<b>PDF:</b> A file format developed by Adobe to present documents "
            " consistently across different devices and platforms. Commonly "
            "used for text documents, forms, presentations, and eBooks. <br><br>"
            "Images can be embedded into PDF files, either as backgrounds, "
            "illustrations, or diagrams. This is common in academic papers, "
            "brochures, and user manuals. ")
        
        ax, ay, aw, ah = 650, 350, 50, 50
        file_filter = "PDF Files (*.pdf)"
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("PDF to Image Converter")
        self.setFixedSize(700, 400)

        select_file_button = DefaultButtonStyle(
            'Select a PDF file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        convert_button = DefaultButtonStyle("Convert", parent=self, bold=True, command=self.convert_file)
        convert_button.setGeometry(450, 50, 100, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 100)
        self.output_label.setReadOnly(True)
        self.output_label.hide()

    def convert_file(self):
        if hasattr(self, 'selected_file'):
            try:
                file_extension = os.path.splitext(self.selected_file)[1].lower()

                if file_extension == '.pdf':
                    # Specify the output directory
                    output_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'pdf_to_image_output')
                    os.makedirs(output_dir, exist_ok=True)

                    # Convert the PDF to images
                    images = convert_from_path(self.selected_file)

                    # Save each page as an image file
                    for i, image in enumerate(images):
                        image_path = os.path.join(output_dir, f'page_{i + 1}.png')
                        image.save(image_path, 'PNG')

                    # Show a custom message box with a button to open the Downloads folder
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Conversion Successful')
                    msg_box.setText(f'PDF converted and images saved in: {output_dir}')
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

                    # Add a custom button for opening the Downloads folder
                    open_folder_btn = msg_box.addButton('Open Downloads', QMessageBox.ButtonRole.ActionRole)
                    msg_box.exec()

                    # If the user clicks "Open Downloads", open the Downloads folder
                    if msg_box.clickedButton() == open_folder_btn:
                        self.open_downloads_folder()

                    self.output_label.clear()
                    self.output_label.setHtml(f"<b>{file_extension} file converted to PNG. PNG file created and saved at:</b><br>{output_dir}")
                    self.output_label.show()
                else:
                    QMessageBox.warning(
                        self, 'Invalid File Type',
                        'Please select a PDF file for conversion.')

            except Exception as e:
                QMessageBox.critical(
                    self, 'Conversion Failed',
                    f'An error occurred during conversion: {str(e)}')
        else:
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')
