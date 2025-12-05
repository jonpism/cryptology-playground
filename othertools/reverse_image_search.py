from PyQt6.QtWidgets                import (QWidget, QMessageBox, QHBoxLayout, 
                                            QVBoxLayout, QDialog, QLabel, QLineEdit, 
                                            QPushButton, QTextBrowser)
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
import serpapi

class ReverseImageSearchWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Reverse Image Search Tool"
        msgbox_txt = """
            <p><b>Reverse Image Search Tool</b></p>
            <p>This tool allows you to search for an image using its URL through Google Reverse Image Search via SerpAPI.</p>
            <p><b>How to use:</b></p>
            <ul>
                <li>Paste the image URL in the "Paste URL" field.</li>
                <li>Click "Submit" to perform the reverse image search.</li>
                <li>You must enter your API key from SerpAPI, after signing up.</li>
                <li>The results will appear below with clickable links to sources.</li>
            </ul>
            <p><b>Features:</b></p>
            <ul>
                <li>Displays a list of pages where the image appears.</li>
                <li>Shows titles and snippets of the pages.</li>
                <li>Clickable links open the page in your browser.</li>
            </ul>
            <p>For more information about SerpAPI, visit <a href="https://serpapi.com/" style="color:blue;">SerpAPI</a>.</p>"""

        self.setWindowTitle("Reverse Image Search Tool")
        self.setFixedSize(700, 700)

        # Image URL input
        url_label = QLabel("Paste URL:", parent=self)
        url_label.setGeometry(200, 10, 110, 50)
        self.url_input = DefaultQLineEditStyle(parent=self)
        self.url_input.setGeometry(10, 50, 480, 50)

        search_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.reverse_img_search_operation)
        search_button.setGeometry(530, 50, 150, 50)

        self.output_label = QTextBrowser(parent=self)
        self.output_label.setGeometry(10, 130, 680, 500)
        self.output_label.setReadOnly(True)
        self.output_label.setOpenExternalLinks(True)

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 650, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def reverse_img_search_operation(self):
        if not self.url_input.text().strip():
            QMessageBox.warning(self, "No URL Entered", "Please enter an image URL first.")
            return

        try:
            dialog = APIDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                api_key = dialog.get_data()["API Key"]
                params = {
                    "engine": "google_reverse_image",
                    "image_url": self.url_input.text(),
                    "max_results": '15'}
                
                search = serpapi.Client(api_key=api_key)
                results = search.search(params)
                output = ''
                if "image_results" in results:
                    output += "<b>Pages / Sources:</b><br>"
                    for item in results["image_results"]:
                        title = item.get("title", "Unknown")
                        link = item.get("link", "#")
                        snippet = item.get("snippet", "")
                        output += f"- <a href='{link}'>{title}</a>: {snippet}<br>"

                self.output_label.setHtml(output)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
            self.output_label.setText("Error occurred while performing the search.")

class APIDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paste API key from SerpAPI")
        self.setModal(True)
        self.setFixedSize(300, 180)

        layout = QVBoxLayout()

        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("API Key:"))
        self.api_input = QLineEdit()
        api_layout.addWidget(self.api_input)
        layout.addLayout(api_layout)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def get_data(self):
        return {"API Key": self.api_input.text().strip()}
