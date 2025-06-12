from PyQt6.QtWidgets    import QWidget, QTextBrowser

class SlideAttack(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Slide Attack")
        self.setFixedSize(700, 300)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("A slide attack is a cryptographic technique used to analyze the key schedule "
        "of a block cipher and exploit weaknesses to break the cipher. The attack exploits the similarity "
        "between different rounds of encryption. The slide attack gets its name from the way it exploits "
        "the repeated structure of a block cipher to 'slide' one encryption step over another. It works "
        "by finding pairs of inputs (P,P′) and outputs (C,C′) that are related in a way that "
        "'slides' one round into the next. <br>Imagine you have a deck of cards with the same sequence of "
        "suits repeating every few cards. If you take two cards at different points in the deck and "
        "'slide' one over the other, you might see that the same pattern emerges, helping you predict "
        "what comes next. The slide attack works in a similar way, but with encryption rounds instead of cards. <br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Slide_attack'>Wikipedia</a><br>"
        "<a href='https://link.springer.com/chapter/10.1007/3-540-48519-8_18'>Springer</a><br>"
        "<a href='https://eprint.iacr.org/2016/1177.pdf'>Cryptology ePrint Archive</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
