from PyQt6.QtWidgets                            import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                               import Qt
from DefaultStyles.button_style                 import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style             import DefaultQLineEditStyle
import random

class LoremIpsumGenerator:

    def __init__(self):
        self.words = (
            "lorem ipsum dolor sit amet consectetur adipiscing elit "
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua "
            "ut enim ad minim veniam quis nostrud exercitation ullamco laboris "
            "nisi ut aliquip ex ea commodo consequat duis aute irure dolor in "
            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur "
            ".Excepteur sint occaecat cupidatat non proident, sunt in culpa qui "
            "officia deserunt mollit anim id est laborum. ").split()
    
    def generate(self, length):
        """Generate Lorem Ipsum text of a specific length.

        :param length: The desired length of the Lorem Ipsum text in characters.
        :return: A string of Lorem Ipsum text with the specified length."""
        if length <= 0:
            return ""
        
        generated_text = []
        current_length = 0
        
        while current_length < length:
            word = random.choice(self.words)
            if current_length + len(word) + len(generated_text) <= length:
                generated_text.append(word)
                current_length += len(word)
            else:
                break
        
        return " ".join(generated_text)

class LoremIpsumGenerateWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Lorem Ipsum Text Generator"
        msgbox_txt = (
        ""
        " "
        " "
        " "
        " "
        " "
        " "
        " "
        " "
        ""
        "<br><br>"
        "Useful links: <br>"
        "<a href=###>Wikipedia</a><br>"
        "<a href=>Geeks for Geeks</a>")

        self.setWindowTitle("Lorem Ipsum Text Generator")
        self.setFixedSize(700, 500)

        # Characters input
        chars_label = QLabel("How many characters:", parent=self)
        chars_label.setGeometry(10, 20, 150, 50)
        self.chars_input = DefaultQLineEditStyle(parent=self, int_validator=True)
        self.chars_input.setGeometry(170, 20, 80, 50)

        generate_button = DefaultButtonStyle("Generate", parent=self, bold=True, command=self.generate)
        generate_button.setGeometry(280, 20, 100, 50)

        self.lorem_ipsum_label = QTextEdit(parent=self)
        self.lorem_ipsum_label.setGeometry(10, 100, 680, 300)
        self.lorem_ipsum_label.setReadOnly(True)
        self.lorem_ipsum_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 450, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def generate(self):
        try:
            characters = int(self.chars_input.text())

            lorem = LoremIpsumGenerator()
            text = lorem.generate(characters)

            self.lorem_ipsum_label.clear()
            self.lorem_ipsum_label.setHtml(f"<b>Generated text:</b><br>{str(text)}")
            self.lorem_ipsum_label.show()
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
