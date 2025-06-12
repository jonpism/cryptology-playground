from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from collections                    import Counter
import heapq

class DataCompression:
    class Node:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}

    def _build_huffman_tree(self, frequency):
        priority_queue = [self.Node(char, freq) for char, freq in frequency.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged = self.Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(priority_queue, merged)

        return priority_queue[0]

    def _build_codes(self, root, current_code=""):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_codes[current_code] = root.char
            return

        self._build_codes(root.left, current_code + "0")
        self._build_codes(root.right, current_code + "1")

    def compress(self, data):
        frequency = Counter(data)
        root = self._build_huffman_tree(frequency)
        self._build_codes(root)

        compressed_data = "".join(self.codes[char] for char in data)
        return compressed_data

    def decompress(self, compressed_data):
        current_code = ""
        decompressed_data = []

        for bit in compressed_data:
            current_code += bit
            if current_code in self.reverse_codes:
                decompressed_data.append(self.reverse_codes[current_code])
                current_code = ""

        return "".join(decompressed_data)

class DataCompressionWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Data Compression"
        msgbox_txt = (
            "This tool implements a Huffman-based data compression algorithm. "
            "Using the principles of frequency-based encoding, it compresses data efficiently "
            "by assigning shorter codes to more frequent characters. "
            "You can input any text data, and the tool will provide the compressed version. "
            "The original data can also be decompressed back to verify correctness. "
            "This functionality demonstrates the fundamentals of data compression in an interactive way.")

        self.setWindowTitle("Data compression")
        self.setFixedSize(700, 400)

        # data input
        data_input_label = QLabel("Enter data:", parent=self)
        data_input_label.setGeometry(300, 10, 100, 50)
        self.data_input = DefaultQLineEditStyle(parent=self)
        self.data_input.setGeometry(10, 60, 680, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, command=self.data_compression)
        submit_button.setGeometry(300, 140, 100, 50)
        
        self.result_label = QTextEdit(parent=self)
        self.result_label.setGeometry(10, 230, 680, 100)
        self.result_label.setReadOnly(True)
        self.result_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 350, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)
    
    def data_compression(self):
        try:
            if not self.data_input.text():
                raise ValueError('Please enter data.')
            data = self.data_input.text()

            compressor = DataCompression()
            compressed = compressor.compress(data)

            self.result_label.clear()
            self.result_label.setHtml(f"<b>Compressed data:</b><br>{str(compressed)}")
            self.result_label.show()
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))
