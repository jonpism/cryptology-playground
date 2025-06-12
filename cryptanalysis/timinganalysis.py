from PyQt6.QtWidgets    import QWidget, QTextBrowser

class TimingAnalysis(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Timing Analysis (Attack)")
        self.setFixedSize(700, 350)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("Timing analysis (a side-channel attack) is the process of evaluating the time required for different "
        "cryptographic algorithms (or operations/events) in a system. Information can leak from a system through measurement of "
        "the time it takes to respond to certain queries. It is commonly used in various fields, including: "
        "<ul>"
        "<li><b>Digital Circuit Design (Static Timing Analysis - STA)</b>: Ensures a circuit meets timing constraints (setup and hold times).</li>"
        "<li><b>Embedded Systems & Real-Time Systems:</b> Includes <b>Worst-Case Execution Time (WCET)</b> analysis.</li>"
        "<li><b>Performance Analysis in Software & Algorithms:</b> Used for optimization (e.g., Big-O analysis, profiling).</li>"
        "<li><b>Mechanical & Physical Systems:</b> Used in robotics and automation to ensure precise timing.</li>"
        "</ul>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Timing_attack'>Wikipedia</a><br>"
        "<a href='https://www.synopsys.com/glossary/what-is-static-timing-analysis.html'>Synopsys</a><br>"
        "<a href='https://schaumont.dyn.wpi.edu/ece574f23/06timing.html'>Advanced Digital Systems Design</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
