from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle

class DataDifferencing:
    """A class for implementing data differencing and reconstructing the original data.
    
    This supports creating a difference (delta) between two sequences and reconstructing the target
    sequence using the source sequence and the delta."""

    def create_delta(self, source, target):
        """Create a delta (difference) between the source and target sequences.
        Args:
            source (bytes): The original data sequence.
            target (bytes): The modified data sequence.
        Returns:
            list: A list of operations to transform the source into the target."""
        delta = []
        
        # Pointer to traverse both sequences
        source_index = 0
        target_index = 0
        
        while target_index < len(target):
            # Check if the current position matches in source and target
            if source_index < len(source) and source[source_index] == target[target_index]:
                # Match operation (copy from source)
                delta.append(("COPY", source_index, 1))
                source_index += 1
                target_index += 1
            else:
                # Mismatch operation (add from target)
                delta.append(("ADD", target[target_index]))
                target_index += 1

        # Handle any trailing source sequence (if any)
        while source_index < len(source):
            delta.append(("DELETE", source_index))
            source_index += 1

        return delta

    def apply_delta(self, source, delta):
        """Apply a delta to a source sequence to reconstruct the target sequence.
        Args:
            source (bytes): The original data sequence.
            delta (list): The delta operations to apply.
        Returns:
            bytes: The reconstructed target sequence."""
        target = []

        for operation in delta:
            if operation[0] == "COPY":
                _, source_index, length = operation
                target.extend(source[source_index:source_index + length])
            elif operation[0] == "ADD":
                _, value = operation
                target.append(value)

        return bytes(target)

class DataDifferencingWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Data Differencing"
        msgbox_txt = (
        "This application demonstrates the concept of data differencing, "
        "which involves computing the differences (delta) between two data sequences "
        "and using these differences to reconstruct the modified sequence. <br><br>"
        "Key Features:<br>"
        "- Generate a delta between a source and a target sequence.<br>"
        "- Reconstruct the target sequence from the source using the delta.<br>"
        "- Built with Python and PyQt6 for an interactive GUI.<br><br>"
        "The underlying logic relies on comparing byte sequences to detect matching, "
        "added, or deleted segments, enabling efficient data transformations.<br><br>"
        "Useful links:<br>"
        "<a href=https://en.wikipedia.org/wiki/Data_differencing>Wikipedia</a><br>")

        self.setWindowTitle("Data Differencing")
        self.setFixedSize(700, 600)

        # Source input
        source_input_label = QLabel("Give source:", parent=self)
        source_input_label.setGeometry(300, 10, 100, 50)
        self.source_input = DefaultQLineEditStyle(parent=self)
        self.source_input.setGeometry(10, 60, 680, 50)

        # Target input
        target_input_label = QLabel("Give target:", parent=self)
        target_input_label.setGeometry(300, 120, 100, 50)
        self.target_input = DefaultQLineEditStyle(parent=self)
        self.target_input.setGeometry(10, 170, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.call_data_diff)
        submit_button.setGeometry(300, 260, 100, 50)

        self.delta_label = QTextEdit(parent=self)
        self.delta_label.setGeometry(10, 320, 680, 100)
        self.delta_label.setReadOnly(True)
        self.delta_label.hide()
    
        self.reconstructed_label = QTextEdit(parent=self)
        self.reconstructed_label.setGeometry(10, 430, 680, 100)
        self.reconstructed_label.setReadOnly(True)
        self.reconstructed_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 550, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def call_data_diff(self):
        try:
            if not self.source_input.text():
                raise ValueError('Please enter source.')
            if not self.target_input.text():
                raise ValueError('Please enter target.')
            source = self.source_input.text().encode('utf-8')
            target = self.target_input.text().encode('utf-8')

            differ = DataDifferencing()

            delta = differ.create_delta(source=source, target=target)

            self.delta_label.clear()
            self.delta_label.setHtml(f"<b>Delta:</b><br>{str(delta)}")
            self.delta_label.show()

            reconstructed = differ.apply_delta(source, delta)

            self.reconstructed_label.clear()
            self.reconstructed_label.setHtml(
                f"<b>Reconstructed:</b><br>{str(reconstructed.decode('utf-8'))}")
            self.reconstructed_label.show()

            assert reconstructed == target
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))