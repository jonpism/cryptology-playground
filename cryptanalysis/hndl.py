from PyQt6.QtWidgets    import QWidget, QTextBrowser

class HNDL(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Harvest now, Decrypt later")
        self.setFixedSize(700, 400)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("Harvest Now, Decrypt Later (HNDL) Attacks refer to a cybersecurity threat "
        "where attackers collect and store encrypted data today with the expectation that future "
        "advancements—particularly in <a href='https://en.wikipedia.org/wiki/Quantum_computing'>quantum computing</a>-"
        "will allow them to decrypt it later. This is a major concern for organizations handling sensitive data, as "
        "encryption methods that are secure today may become obsolete in the future. "
        "<ul>"
        "<li>Attackers intercept and store encrypted data through network eavesdropping, cyber espionage, or breaches.</li>"
        "<li>The encrypted data is kept for years or even decades.</li>"
        "<li>When quantum computers become powerful enough, they can break widely used encryption algorithms (like <b>RSA</b> and <b>ECC</b>) using algorithms such as <br>Shor's algorithm</b>.</li>"
        "<li>Once decryption is feasible, attackers access sensitive information, which could include government secrets, financial records, intellectual property, or personal data.</li>"
        "</ul>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Harvest_now,_decrypt_later'>Wikipedia</a><br>"
        "<a href='https://venturebeat.com/security/harvest-now-decrypt-later-why-hackers-are-waiting-for-quantum-computing/'>VentureBeat</a><br>"
        "<a href='https://www.techmonitor.ai/hardware/quantum/harvest-now-decrypt-later-cyberattack-quantum-computer'>Tech Monitor</a><br>"
        "<a href='https://securityboulevard.com/2024/10/what-you-need-to-know-about-harvest-now-decrypt-later-attacks/'>Security Boulevard</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
