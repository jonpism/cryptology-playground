from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle 
from collections                    import Counter
from io                             import BytesIO
from PyQt6.QtGui                    import QPixmap
import matplotlib.pyplot            as plt
import math

class EntropyCalculator:
    def __init__(self, data, encoding='utf-8'):
        """Initializes the entropy calculator with data and encoding.

        :param data: string input data for entropy calculation.
        :param encoding: encoding used to process data. Default is 'utf-8'."""
        self.data = data.encode(encoding) if isinstance(data, str) else data
        self.probabilities = self._calculate_probabilities(self.data)

    def _calculate_probabilities(self, data):
        """Calculates the probability of each byte in the data.
        
        :param data: byte data for entropy calculation.
        :return: dictionary with bytes as keys and their probabilities as values."""
        counter = Counter(data)
        total = len(data)
        probabilities = {symbol: count / total for symbol, count in counter.items()}
        return probabilities

    def entropy(self):
        """Calculates the entropy of the data.
        
        :return: entropy value."""
        return -sum(p * math.log2(p) for p in self.probabilities.values())

    def plot_histogram(self):
        """Plots a histogram of byte frequencies and returns it as an image."""
        byte_values = list(self.probabilities.keys())
        frequencies = list(self.probabilities.values())

        # Plotting the histogram
        plt.figure(figsize=(10, 6))
        plt.bar(byte_values, frequencies, color='blue', edgecolor='black')
        plt.xlabel('Byte Value')
        plt.ylabel('Probability')
        plt.title('Byte Frequency Distribution')
        plt.xticks(range(0, 256, 10))
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save plot to a BytesIO object as PNG
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

class EntropyWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Entropy"
        msgbox_txt = (
            "<p>This tool calculates the Shannon entropy of the provided input data, "
            "a measurement used in information theory to assess the randomness or unpredictability of data. "
            "It provides a visualization of the frequency distribution of byte values in the data.</p>"
            "<h4>Features:</h4>"
            "<ul>"
            "<li>Calculates Shannon entropy, a common metric in data analysis and cryptography.</li>"
            "<li>Generates a histogram to show the distribution of byte values in the data.</li>"
            "<li>Supports custom text input and provides results with a single button click.</li>"
            "</ul>"
            "<h4>Usage Instructions:</h4>"
            "<ol>"
            "<li>Enter the text data into the input field at the top.</li>"
            "<li>Click the <b>Submit</b> button to calculate the entropy and generate a histogram.</li>"
            "<li>The calculated entropy will display below the input, and the histogram will appear beneath it.</li>"
            "</ol>"
            "<p><b>Note:</b> Entropy values are particularly useful in fields like cryptography, data compression, and "
            "randomness testing.</p>"
            "<p><b>Useful links:</b>"
            "<li><a href='https://en.wikipedia.org/wiki/Entropy_(information_theory)'>Entropy - Wikipedia</a></li>")

        self.setWindowTitle("Entropy (Information Theory)")
        self.setFixedSize(700, 800)

        # Data input
        data_label = QLabel("Enter data:", parent=self)
        data_label.setGeometry(300, 10, 100, 50)
        self.data_input = DefaultQLineEditStyle(parent=self)
        self.data_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.entropy)
        submit_button.setGeometry(300, 130, 100, 50)

        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 210, 680, 50)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        self.histogram_label = QLabel(parent=self)
        self.histogram_label.setGeometry(10, 300, 680, 400)
        self.histogram_label.setScaledContents(True)  # Scale image to fit QLabel size
        self.histogram_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 750, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def entropy(self):
        try:
            data = self.data_input.text()
            obj = EntropyCalculator(data=data)

            # Show entropy result
            self.result_label.clear()
            self.result_label.setHtml(f"<b>Shannon Entropy:</b><br>{str(obj.entropy())}")
            self.result_label.show()

            # Plot histogram and show in QLabel
            histogram_image = obj.plot_histogram()
            pixmap = QPixmap()
            pixmap.loadFromData(histogram_image.getvalue())
            self.histogram_label.setPixmap(pixmap)
            self.histogram_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))