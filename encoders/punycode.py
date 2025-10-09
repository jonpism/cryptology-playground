from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class PunycodeEncodeWindow(QWidget):
    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Punycode Encoding"
        msgbox_txt = (
            "Punycode is a way to represent Unicode characters using ASCII characters only.<br>"
            "It is mainly used for Internationalized Domain Names (IDNs) to allow non-ASCII characters in web addresses.<br><br>"
            "<b>Example:</b><br>"
            "münich → mnich-kva<br>"
            "café → caf-dma<br><br>"
            "<a href='https://en.wikipedia.org/wiki/Punycode'>Learn more on Wikipedia</a>")

        self.setWindowTitle("Punycode Encoder")
        self.setFixedSize(700, 600)

        text_input_label = QLabel("Enter Unicode text:", parent=self)
        text_input_label.setGeometry(280, 10, 200, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        encode_button = DefaultButtonStyle("Encode → Punycode", parent=self, bold=True, command=self.encode_punycode)
        encode_button.setGeometry(250, 130, 200, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 220, 680, 300)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def encode_punycode(self):
        try:
            txt = self.text_input.text()
            if not txt:
                raise ValueError("Please enter text to encode.")

            encoded = txt.encode("punycode").decode("ascii")
            self.show_result(f"<b>Encoded (Punycode):</b><br>{encoded}")

        except Exception as e:
            QMessageBox.critical(self, "Encoding Error", str(e))

    def show_result(self, html_text):
        self.result_label.clear()
        self.result_label.setHtml(html_text)
        self.result_label.show()

# ========================================================================================================

class PunycodeDecodeWindow(QWidget):
    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Punycode Decoding"
        msgbox_txt = (
            "This tool decodes ASCII-based Punycode text back into its original Unicode form.<br>"
            "It is useful for reading internationalized domain names (IDNs) or encoded text.<br><br>"
            "<b>Example:</b><br>"
            "mnich-kva → münich<br>"
            "caf-dma → café<br><br>"
            "<a href='https://en.wikipedia.org/wiki/Punycode'>Learn more on Wikipedia</a>")

        self.setWindowTitle("Punycode Decoder")
        self.setFixedSize(700, 600)

        text_input_label = QLabel("Enter Punycode text:", parent=self)
        text_input_label.setGeometry(280, 10, 200, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(10, 60, 680, 50)

        decode_button = DefaultButtonStyle("Decode → Unicode", parent=self, bold=True, command=self.decode_punycode)
        decode_button.setGeometry(250, 130, 200, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 220, 680, 300)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def decode_punycode(self):
        try:
            txt = self.text_input.text()
            if not txt:
                raise ValueError("Please enter text to decode.")

            if txt.startswith("xn--"):
                txt = txt[4:]

            decoded = txt.encode("ascii").decode("punycode")
            self.show_result(f"<b>Decoded (Unicode):</b><br>{decoded}")

        except Exception as e:
            QMessageBox.critical(self, "Decoding Error", str(e))

    def show_result(self, html_text):
        self.result_label.clear()
        self.result_label.setHtml(html_text)
        self.result_label.show()
