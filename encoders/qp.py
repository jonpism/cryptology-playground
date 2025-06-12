from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
import re

class QuotedPrintable:
    def __init__(self):
        self.max_line_length = 76

    def encode(self, text):
        """
        Encodes a given string into Quoted-Printable format.
        :param text: The string to encode.
        :return: Encoded string.
        """
        encoded = []
        for char in text:
            if self._needs_encoding(char):
                encoded.append(self._encode_char(char))
            else:
                encoded.append(char)
        encoded_text = ''.join(encoded)
        return self._soft_wrap(encoded_text)

    def decode(self, encoded_text):
        """
        Decodes a Quoted-Printable encoded string.
        :param encoded_text: Encoded string.
        :return: Decoded string.
        """
        # Remove soft line breaks
        encoded_text = encoded_text.replace("=\n", "")
        # Decode all =XX patterns
        return re.sub(r'=(\w{2})', lambda match: chr(int(match.group(1), 16)), encoded_text)

    def _needs_encoding(self, char):
        """
        Determines if a character needs to be encoded.
        :param char: A single character.
        :return: True if the character needs encoding, False otherwise.
        """
        if char == '\n' or char == '\r':
            return False
        return not (33 <= ord(char) <= 126 and char != '=')

    def _encode_char(self, char):
        """
        Encodes a single character in Quoted-Printable format.
        :param char: A single character.
        :return: Encoded representation.
        """
        return f"={ord(char):02X}"

    def _soft_wrap(self, text):
        """
        Soft wraps lines at the maximum line length.
        :param text: Encoded text.
        :return: Wrapped encoded text.
        """
        lines = []
        while len(text) > self.max_line_length:
            wrap_point = self.max_line_length
            while wrap_point > 0 and text[wrap_point - 1] == '=':
                wrap_point -= 1
            lines.append(text[:wrap_point] + '=')
            text = text[wrap_point:]
        lines.append(text)
        return '\n'.join(lines)

# ============================================================================================================

class ToQuotedPrintableWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        self.setWindowTitle("To Quoted Printable (QP Encoding)")
        self.setFixedSize(700, 400)

        # Plaintext input
        plaintext_input_label = QLabel("Give plaintext:", parent=self)
        plaintext_input_label.setGeometry(300, 10, 100, 50)
        self.plaintext_input = DefaultQLineEditStyle(
            parent=self,
            placeholder_text="Maximum length: 76",
            max_length=76)
        self.plaintext_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.to_qp)
        submit_button.setGeometry(300, 160, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 260, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()
    
    def to_qp(self):
        try:
            plaintext = self.plaintext_input.text()
            if not plaintext:
                raise ValueError('Please enter a plaintext')

            qp = QuotedPrintable()
            encoded = qp.encode(plaintext)

            self.result_label.clear()
            self.result_label.setHtml(f"<b>Result:</b><br>{str(encoded)}")
            self.result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))

# ============================================================================================================

class FromQuotedPrintableWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        self.setWindowTitle("From Quoted Printable (QP Decoding)")
        self.setFixedSize(700, 400)

        # qp input
        qp_input_label = QLabel("Give qp encoded text:", parent=self)
        qp_input_label.setGeometry(300, 10, 100, 50)
        self.qp_input = DefaultQLineEditStyle(
            parent=self,
            placeholder_text="Maximum length: 76",
            max_length=76)
        self.qp_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.qp_decode)
        submit_button.setGeometry(300, 160, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 260, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()
    
    def qp_decode(self):
        try:
            qp_encoded = self.qp_input.text()
            if not qp_encoded:
                raise ValueError('Please enter qp input.')

            qp = QuotedPrintable()
            decoded = qp.decode(qp_encoded)

            self.result_label.clear()
            self.result_label.setHtml(f"<b>Result:</b><br>{str(decoded)}")
            self.result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
