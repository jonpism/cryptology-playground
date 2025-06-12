from PyQt6.QtWidgets    import QWidget, QTextBrowser

class ReplayAttack(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Replay Attack")
        self.setFixedSize(700, 300)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("A replay attack is a type of network attack where an attacker intercepts "
        "and retransmits valid data (such as authentication tokens or encrypted messages) to gain "
        "unauthorized access or disrupt communication. Since the attacker does not need to decrypt "
        "or modify the intercepted data, replay attacks can be effective even against encrypted "
        "communication. Steps of how this attack works: "
        "<ol>"
        "<li>The attacker <b>eavesdrops</b> on a legitimate communication between a user and a server.</li>"
        "<li>They <b>capture a valid request or authentication message</b> (e.g., login credentials, "
        "digital signatures, session tokens, hashed passwords).</li>"
        "<li>The attacker <b>replays</b> this captured message to trick the system into granting access or "
        "performing an unintended action.</li>"
        "</ol>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Replay_attack'>Wikipedia</a><br>"
        "<a href='https://www.geeksforgeeks.org/replay-attack/'>Geeks for Geeks</a><br>"
        "<a href='https://cybersecurityforme.com/replay-attack/'>Cybersecurity for me</a><br>"
        "<a href='https://justcryptography.com/what-is-a-replay-attack-in-cryptography/'>Just Cryptography</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
