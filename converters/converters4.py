from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

def hexdump(data: bytes, width: int = 16) -> str:
    """creates a hexdump"""
    result = []
    for offset in range(0, len(data), width):
        chunk = data[offset:offset + width]
        hex_bytes = ' '.join(f"{b:02x}" for b in chunk)
        hex_padded = f"{hex_bytes:<{width * 3 - 1}}"
        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        result.append(f"{offset:08x}  {hex_padded}  |{ascii_part}|")
    return '\n'.join(result)

class HexdumpWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text to Hexdump Converter")
        self.setFixedSize(700, 600)

        # text input
        text_label = QLabel("Enter text:", parent=self)
        text_label.setGeometry(10, 20, 100, 50)
        self.text_input = DefaultQLineEditStyle(parent=self)
        self.text_input.setGeometry(100, 20, 450, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.to_hexdump)
        submit_button.setGeometry(570, 20, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(50, 140, 590, 410)
        self.result_label.setReadOnly(True)

    def to_hexdump(self):
        text = self.text_input.text()
        try:
            if text:
                data = text.encode("utf-8")
                dump = hexdump(data)
                self.result_label.setPlainText(dump)
            else:
                raise ValueError("Input text is empty")
        except ValueError as ve:
            QMessageBox.warning(self, "Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
