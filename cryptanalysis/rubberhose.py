from PyQt6.QtWidgets    import QWidget, QTextBrowser

class RubberHoseCryptanalysis(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rubber Hose Cryptanalysis")
        self.setFixedSize(700, 400)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("Rubber-hose cryptanalysis is the practice of extracting cryptographic secrets "
        "through coercion, such as threats, torture, or intimidation, rather than using mathematical or "
        "computational attacks. It is a play on words, implying that instead of using advanced cryptanalysis, "
        "an attacker could simply beat the keyholder with a rubber hose until they reveal the decryption key.<br>"
        "Deniable encryption is specifically designed to counter rubber-hose cryptanalysis by allowing users "
        "to plausibly deny the existence of sensitive data. Here's how: "
        "<ul>"
        "<li>A deniable encryption system allows the same encrypted data to be decrypted into different plaintexts depending on the key used.</li>"
        "<li>If forced to reveal a key, the user can provide a decoy key that decrypts to harmless data, making it impossible to prove whether additional hidden data exists.</li>"
        "<li>Systems like <b>VeraCrypt’s hidden volumes</b> allow users to store sensitive files inside an encrypted container that itself contains a visible, less important set of files.</li>"
        "<li>Even if coerced to provide a password, the user can reveal only the decoy container while keeping the true hidden volume secret.</li>"
        "<li>Some deniable encryption schemes are used in secure messaging protocols to ensure that even if a user is forced to decrypt a message, they can plausibly claim that the decrypted text was the only message.</li>"
        "</ul>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Deniable_encryption'>Wikipedia</a><br>"
        "<a href='https://www.schneier.com/blog/archives/2008/10/rubber_hose_cry.html'>Schneier on Security</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
