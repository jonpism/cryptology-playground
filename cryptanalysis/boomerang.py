from PyQt6.QtWidgets    import QWidget, QTextBrowser

class BoomerangAttack(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Boomerang Attack")
        self.setFixedSize(700, 200)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("A Boomerang Attack is a cryptanalysis technique used to attack block ciphers. "
        "The boomerang attack is based on <a href='https://en.wikipedia.org/wiki/Differential_cryptanalysis'>differential cryptanalysis</a> "
        "(basically an extension of differential cryptanalysis). The attack was published in 1999 by <a href='https://en.wikipedia.org/wiki/David_A._Wagner'>David Wagner</a>, "
        "who used it to break the COCONUT98 cipher. <br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Boomerang_attack'>Wikipedia</a><br>"
        "<a href='https://link.springer.com/chapter/10.1007/3-540-48519-8_12'>SpringerLink</a><br>"
        "<a href='https://eprint.iacr.org/2019/1154.pdf'>Cryptology ePrint Archive</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
