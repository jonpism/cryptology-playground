from PyQt6.QtWidgets    import QWidget, QTextBrowser

class SCA(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Side-Channel Attack")
        self.setFixedSize(600, 250)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("This type of attack is based on information obtained from the physical <br>"
        "implementation of the cryptographic system, rather than on weaknesses in the <br>algorithm "
        "itself. Side-channel attacks include timing attacks, power analysis attacks, electromagnetic "
        "attacks, and others. In other words, it can exploit unintended <br>information leakage from a "
        "system rather than breaking cryptographic algorithms <br>directly. These attacks take advantage of "
        "physical characteristics or indirect outputs.<br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Side-channel_attack'>Wikipedia</a><br>"
        "<a href='https://www.geeksforgeeks.org/what-is-a-side-channel/'>Geeks for Geeks</a><br>"
        "<a href='https://www.allaboutcircuits.com/technical-articles/understanding-side-channel-attack-basics/'>All about circuits</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
