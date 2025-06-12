from PyQt6.QtWidgets    import QWidget, QTextBrowser

class ACPA(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adaptive Chosen-Plaintext Attack")
        self.setFixedSize(500, 200)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("This attack is similar to Chosen-Plaintext Attack (CPA) "
        "but more <br>powerful. Here, the attacker requests the cipher texts of "
        "additional <br>plaintexts after they have ciphertexts for some texts. <br><br>"
        "<a href='https://crypto.stackexchange.com/questions/24791/what-is-the-difference-between-chosen-plaintext-attack-and-adaptive-chosen-plain'>Stackexchange</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
