from PyQt6.QtWidgets    import QWidget, QTextBrowser

class XSLattack(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("eXtended Sparse Linearization Attack")
        self.setFixedSize(700, 400)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("The eXtended Sparse Linearization (XSL) attack is a theoretical method "
        "designed to break certain block ciphers, including AES, by exploiting their algebraic structure. "
        "It works by rewriting the encryption process as a system of quadratic equations, which, in theory, "
        "could be solved to recover the secret key. <br>"
        "The idea behind XSL builds on an earlier method called eXtended Linearization (XL), which attempts "
        "to solve multivariate quadratic (MQ) equations by introducing extra equations. However, XSL takes "
        "this a step further by choosing equations more selectively, aiming to keep the system manageable and solvable. <br>"
        "One of the main advantages of XSL (if it were practical) is that it doesn't require massive amounts of "
        "plaintext-ciphertext pairs, unlike differential or linear cryptanalysis. Instead, it focuses on the "
        "mathematical properties of the cipher itself. <br>"
        "That said, most cryptographers remain skeptical about its feasibility. The method relies on assumptions "
        "about how many independent equations can be generated, and in practice, it seems that there aren't enough "
        "to fully break AES or other ciphers. So while it's an interesting concept, it's never been successfully "
        "used to crack real-world encryption. <br><br>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/XSL_attack'>Wikipedia</a><br>"
        "<a href='https://eprint.iacr.org/2023/151.pdf'>Cryptology ePrint Archive</a><br>"
        "<a href='https://dbpedia.org/page/XSL_attack'>DBpedia Association</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
