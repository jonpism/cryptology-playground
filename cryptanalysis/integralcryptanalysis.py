from PyQt6.QtWidgets    import QWidget, QTextBrowser

class IntegralCryptanalysis(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Integral Cryptanalysis")
        self.setFixedSize(700, 200)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("Integral cryptanalysis is a cryptanalytic attack used in the cryptanalysis of "
        "block ciphers, particularly those based on substitution-permutation networks (SPNs). "
        "It was first introduced by Lars Knudsen and is considered an extension of differential cryptanalysis. <br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Integral_cryptanalysis'>Wikipedia</a><br>"
        "<a href='https://link.springer.com/chapter/10.1007/3-540-45661-9_9'>SpringerLink</a><br>"
        "<a href='https://iacr.org/submit/files/slides/2024/asiacrypt/asiacrypt2024/145/145_slides.pdf'>The International Association for Cryptologic Research</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
