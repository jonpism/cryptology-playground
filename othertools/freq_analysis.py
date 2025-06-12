from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore                   import Qt
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qtextedit_style  import DefaultQTextEditStyle
from collections                    import Counter
from PyQt6.QtGui                    import QPixmap
from io                             import BytesIO
import matplotlib.pyplot            as plt
import string

class FrequencyAnalysis:
    def __init__(self, text: str):
        """Initialize with a text input for analysis."""
        self.text = text.lower()
        self.cleaned_text = self._clean_text(self.text)
        self.frequency = self._analyze_frequency()
    
    def _clean_text(self, text: str) -> str:
        """Remove non-alphabetic characters from the text."""
        return ''.join(char for char in text if char in string.ascii_lowercase)
    
    def _analyze_frequency(self) -> dict:
        """Perform frequency analysis and return frequency counts."""
        return Counter(self.cleaned_text)
    
    def get_frequency_table(self) -> dict:
        """Get the frequency table as a dictionary."""
        total_chars = len(self.cleaned_text)
        return {char: count / total_chars for char, count in self.frequency.items()}
    
    def most_common(self, n: int = 1):
        """Return the n most common letters."""
        return self.frequency.most_common(n)
    
    def frequency_table(self):
        """Print the frequency table in a readable format."""
        frequency_table = self.get_frequency_table()
        sorted_table = sorted(frequency_table.items(), key=lambda x: x[1], reverse=True)
        print("Character | Frequency")
        print("-" * 20)
        ft = {}
        for char, freq in sorted_table:
            ft.append(f"{char:9} | {freq:.4f}")
    
    def plot_histogram(self) -> BytesIO:
        """Generate a histogram of character frequencies and return as a binary stream."""
        frequency_table = self.get_frequency_table()
        letters = sorted(frequency_table.keys())
        frequencies = [frequency_table[char] for char in letters]
        
        plt.figure(figsize=(10, 6))
        plt.bar(letters, frequencies, color='blue', alpha=0.7)
        plt.title('Character Frequency Histogram')
        plt.xlabel('Characters')
        plt.ylabel('Frequency')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Save the plot to a BytesIO stream
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()
        image_stream.seek(0)
        return image_stream

class FrequencyAnalysisWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Frequency Analysis Tool"
        msgbox_txt = (
            "This tool helps in performing <b>frequency analysis</b> on a given text. "
            "Frequency analysis is a method for analyzing the frequency of letters in a text, "
            "which is often used in cryptography to break substitution ciphers.<br><br>"
            "Features include:<br>"
            "- Displaying a frequency table of characters<br>"
            "- Identifying the most common character<br>"
            "- Generating a histogram to visualize character frequencies<br><br>"
            "Useful links: <br>"
            '<a href="https://en.wikipedia.org/wiki/Frequency_analysis">Wikipedia: Frequency Analysis</a><br>'
            '<a href="https://www.geeksforgeeks.org/frequency-analysis/">GeeksforGeeks: Frequency Analysis</a>')

        self.setWindowTitle("Frequency Analysis")
        self.setFixedSize(700, 900)

        # txt input
        txt_input_label = QLabel("Enter text:", parent=self)
        txt_input_label.setGeometry(300, 10, 300, 50)
        self.txt_input = DefaultQTextEditStyle(parent=self)
        self.txt_input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.txt_input.setGeometry(10, 60, 680, 150)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.freq_analysis)
        submit_button.setGeometry(300, 220, 100, 50)

        self.ft_label = QTextEdit(parent=self)
        self.ft_label.setGeometry(10, 300, 680, 100)
        self.ft_label.setReadOnly(True)
        self.ft_label.hide()

        self.most_common_label = QTextEdit(parent=self)
        self.most_common_label.setGeometry(10, 410, 680, 50)
        self.most_common_label.setReadOnly(True)
        self.most_common_label.hide()

        self.histogram_label = QLabel(parent=self)
        self.histogram_label.setGeometry(10, 470, 680, 350)
        self.histogram_label.setScaledContents(True)  # Scale image to fit QLabel size
        self.histogram_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 850, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def freq_analysis(self):
        try:
            text = self.txt_input.toPlainText()

            fa = FrequencyAnalysis(text)
            ft = fa.get_frequency_table()

            # Update frequency table display
            table_html = "<br>".join(f"{char}: {freq:.4f}" for char, freq in sorted(ft.items(), key=lambda x: x[1], reverse=True))
            self.ft_label.setHtml(f"<b>Frequency table:</b><br>{table_html}")
            self.ft_label.show()

            # Display most common letter
            most_common_letter = fa.most_common(1)
            self.most_common_label.setHtml(f"<b>Most common letter:</b><br>{most_common_letter}")
            self.most_common_label.show()

            # Plot histogram and show in QLabel
            histogram_stream = fa.plot_histogram()
            pixmap = QPixmap()
            pixmap.loadFromData(histogram_stream.read())
            self.histogram_label.setPixmap(pixmap)
            self.histogram_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
