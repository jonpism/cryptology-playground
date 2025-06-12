from PyQt6.QtWidgets    import QWidget, QTextBrowser

class BruteForceAttack(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Brute Force Attack")
        self.setFixedSize(700, 500)

        text_label = QTextBrowser(parent=self)
        text_label.setHtml("This attack involves trying every possible key until the correct one is found. "
        "While this attack is simple to implement, it can be time-consuming and computationally expensive, "
        "especially for longer keys. I implemented a simple python code simulating a brute force attack:<br><br>"
        '<font color="#a206dd">import</font> <font color="#dd7206">itertools</font>, <font color="#dd7206">string</font><br>'
        '<font color="#fb0c4e">target_password</font> = "<font color="#23bf0f">abc</font>"<br>'
        '<font color="#fb0c4e">characters</font> = <font color="#dd7206">string</font>.<font color="#fb0c4e">ascii_lowercase</font><br><br>'
        '<font color="#a206dd">def</font> <font color="#0aeef0">brute_force_attack</font><font color="#eff00a">()</font>:<br>'
        '&nbsp; &nbsp; <font color="#a206dd">for</font> <font color="#fb0c4e">length</font> <font color="#a206dd">in</font> '
        '<font color="#dd7206">range</font><font color="#eff00a">(</font>1,5<font color="#eff00a">)</font>: '
        '<font color="#95974c"># Trying passwords of length 1 to 4</font><br>'
        '&nbsp; &nbsp; &nbsp; &nbsp; <font color="#a206dd">for</font> <font color="#fb0c4e">guess</font> <font color="#a206dd">in</font> '
        '<font color="#dd7206">itertools</font>.<font color="#dd7206">product</font><font color="#eff00a">(</font>'
        '<font color="#fb0c4e">characters</font>, <font color="#fb0c4e">repeat</font>=<font color="#fb0c4e">length</font>'
        '<font color="#eff00a">)</font>:<br> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<font color="#fb0c4e">guess</font> = "".<font color="#0aeef0">join</font>'
        '<font color="#eff00a">(</font><font color="#fb0c4e">guess</font><font color="#eff00a">)</font><br>'
        '&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<font color="#0aeef0">print</font><font color="#eff00a">(</font><font color="#a206dd">f</font><font color="#23bf0f">"Trying</font>:'
        '<font color="#a206dd">{</font><font color="#fb0c4e">guess</font><font color="#a206dd">}</font><font color="#23bf0f">"</font>'
        '<font color="#eff00a">)</font> <font color="#95974c"># Simulating an attack attempt</font><br><br>'
        '&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<font color="#a206dd">if</font> <font color="#fb0c4e">guess</font> == '
        '<font color="#fb0c4e">target_password</font>:<br>'
        '&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<font color="#0aeef0">print</font><font color="#eff00a">(</font><font color="#a206dd">f</font><font color="#23bf0f">"Password found</font>:'
        '<font color="#a206dd">{</font><font color="#fb0c4e">guess</font><font color="#a206dd">}</font><font color="#23bf0f">"</font>'
        '<font color="#eff00a">)</font><br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<font color="#a206dd">return</font><br><br>'
        '&nbsp; &nbsp; <font color="#0aeef0">print</font><font color="#eff00a">(</font><font color="#23bf0f">"Password not found."</font><font color="#eff00a">)</font>'
        '<br><br><font color="#0aeef0">brute_force_attack</font><font color="#eff00a">(</font><font color="#eff00a">)</font>'
        '<br><br>Useful links:</b><br>'
        "<a href='https://en.wikipedia.org/wiki/Brute-force_attack'>Wikipedia</a><br>"
        "<a href='https://www.fortinet.com/resources/cyberglossary/brute-force-attack'>Fortinet</a><br>"
        "<a href='https://cybernews.com/security/what-is-a-brute-force-attack/'>Cybernews</a>")
        text_label.setGeometry(20, 10, 680, 650)
        text_label.setReadOnly(True)
        text_label.setStyleSheet("border: none; background: transparent;")
        text_label.setOpenExternalLinks(True)
'''
target_password = "abc"

# Define possible characters (lowercase letters in this case)
characters = string.ascii_lowercase

# Brute force attack simulation
def brute_force_attack():
    for length in range(1, 5):  # Trying passwords of length 1 to 4
        for guess in itertools.product(characters, repeat=length):
            guess = ''.join(guess)
            print(f"Trying: {guess}")  # Simulating an attack attempt
            
            if guess == target_password:
                print(f"Password found: {guess}")
                return

    print("Password not found.")

if __name__ == "main":
    brute_force_attack()
'''