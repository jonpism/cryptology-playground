from PyQt6.QtWidgets    import QWidget, QTextBrowser

class MITM(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Man-in-the-middle Attack")
        self.setFixedSize(700, 500)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("In this type of attack, the attacker secretly intercepts the message/key and "
        "potentially alters communication between two communicating parties (without their knowledge) "
        "through a secured channel. The attacker positions themselves between the sender and receiver, "
        "making it seem like a normal exchange while secretly eavesdropping or manipulating the data. "
        "<ul>"
        "<li>The attacker intercepts communication between two parties (e.g., a user and a website, or two devices in a network).</li>"
        "<li>The attacker may decrypt, alter, or log the transmitted data before forwarding it to the intended recipient.</li>"
        "<li>The attacker can impersonate one or both parties, tricking them into thinking they are communicating directly.</li>"
        "</ul>"
        "<b>Common MITM Attack Techniques:</b>"
        "<ul>"
        "<li><b>Wi-Fi Eavesdropping:</b> Attackers set up fake public Wi-Fi networks to capture user data.</li>"
        "<li><b>DNS Spoofing:</b> Redirecting users to a fake website by manipulating DNS records.</li>"
        "<li><b>ARP Spoofing:</b> Manipulating the Address Resolution Protocol (ARP) to reroute network traffic.</li>"
        "</ul>"
        "<b>Useful links:</b><br>"
        "<a href='https://en.wikipedia.org/wiki/Man-in-the-middle_attack'>Wikipedia</a><br>"
        "<a href='https://www.geeksforgeeks.org/man-in-the-middle-attack-in-diffie-hellman-key-exchange/'>Geeks for Geeks</a><br>"
        "<a href='https://geekflare.com/cybersecurity/mitm-attack-tools/'>Geekflare</a><br>"
        "<a href='https://www.youtube.com/watch?v=-enHfpHMBo4'>Computerphile - YTB video</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
