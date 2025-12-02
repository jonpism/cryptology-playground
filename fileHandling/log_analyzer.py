from PyQt6.QtWidgets                import QMessageBox, QTextEdit
from DefaultStyles.button_style     import DefaultButtonStyle
from .file_conversion               import FileConversionWindow
from os                             import path
from re                             import findall as re_findall
import matplotlib.pyplot            as plt
import tempfile

class LogAnalyzerWindow(FileConversionWindow):

    def __init__(self, theme_mode):
        about_title = "About Log Analyzer Tool"
        about_text = """This tool is designed to automatically analyze log files and extract useful insights from them.
        Instead of reading thousands of log entries manually, the tool summarizes important information such as:
        <ul>
        <li>the number of errors or warnings</li>
        <li>which IP addresses are most active</li>
        <li>when the system was busiest</li>
        <li>general patterns in activity</li>
        </ul>
        The tool supports various log formats including JSON, Windows Event Logs, Common Event Format, 
        NCSA Common Log Format, Extended Log Format, and W3C Extended Log Format. It helps with debugging, 
        security analysis, system monitoring, and troubleshooting."""

        ax, ay, aw, ah = 650, 650, 50, 50
        file_filter = ("JSON Logs (*.json);;"
            "Windows Event Logs (*.evtx);;"
            "Common Event Format (*.cef *.log);;"
            "NCSA Common Log Format (*.clf *.log);;"
            "Extended Log Format (*.elf);;"
            "W3C Extended Log Format (*.w3c *.log);;"
            "All Supported Logs (*.json *.evtx *.cef *.log *.clf *.elf *.w3c);;"
            "All Files (*)")
        super().__init__(about_title, about_text, ax, ay, aw, ah, file_filter, theme_mode)

        self.setWindowTitle("Log Analyzer Tool")
        self.setFixedSize(700, 700)

        select_file_button = DefaultButtonStyle(
            'Select a file',
            parent=self,
            bold=True, command=self.select_file)
        select_file_button.setGeometry(150, 50, 230, 50)

        analyze_button = DefaultButtonStyle("Click to Analyze", parent=self, bold=True, command=self.analyze_file)
        analyze_button.setGeometry(450, 50, 150, 50)

        self.output_label = QTextEdit(parent=self)
        self.output_label.setGeometry(10, 130, 680, 500)
        self.output_label.setReadOnly(True)
    
    def analyze_file(self):
        try:
            if hasattr(self, 'selected_file'):
                analyzer = LogAnalyzer(self.selected_file)
                html_output = analyzer.process(self.selected_file)

                self.output_label.clear()
                self.output_label.setHtml(html_output)
                self.output_label.show()
        except FileNotFoundError as fnf:
            QMessageBox.warning(self, 'File not found', str(fnf))
        except PermissionError as pe:
            QMessageBox.warning(self, 'Permission Error', str(pe))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

class LogAnalyzer:

    def __init__(self, selected_file):
        self.selected_file = selected_file

    def process(self, file_path):
        if not path.isfile(file_path):
            raise FileNotFoundError("File does not exist!")

        text = open(file_path, "r", errors="ignore").read()

        levels = self.parse_log_levels(text)
        ips = self.extract_ip_addresses(text)
        timeline = self.extract_timestamps(text)

        pie_chart_path = self.generate_log_level_pie(levels)
        ip_chart_path = self.generate_ip_bar(ips)

        return self.build_html_output(levels, ips, timeline, pie_chart_path, ip_chart_path)

    def parse_log_levels(self, text):
        patterns = {
            "INFO": r"\bINFO\b|\bInfo\b",
            "ERROR": r"\bERROR\b|\bError\b",
            "WARNING": r"\bWARN\b|\bWarning\b",
            "DEBUG": r"\bDEBUG\b"}
        return {lvl: len(re_findall(pattern, text)) for lvl, pattern in patterns.items()}

    def extract_ip_addresses(self, text):
        ip_regex = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        ips = re_findall(ip_regex, text)
        freq = {}
        for ip in ips:
            freq[ip] = freq.get(ip, 0) + 1
        return freq

    def extract_timestamps(self, text):
        ts_regex = r"\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}\b"
        ts = re_findall(ts_regex, text)
        freq = {}
        for t in ts:
            freq[t] = freq.get(t, 0) + 1
        return freq

    def generate_log_level_pie(self, levels):
        labels = list(levels.keys())
        sizes = list(levels.values())

        if sum(sizes) == 0:
            return None

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title("Log Level Distribution")

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(temp.name, bbox_inches="tight")
        plt.close()
        return temp.name

    def generate_ip_bar(self, ips):
        if not ips:
            return None

        sorted_ips = sorted(ips.items(), key=lambda x: x[1], reverse=True)[:10]
        keys = [k for k, v in sorted_ips]
        values = [v for k, v in sorted_ips]

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(keys, values)
        ax.set_xticklabels(keys, rotation=45, ha='right')
        ax.set_title("Top IP Addresses")

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(temp.name, bbox_inches="tight")
        plt.close()
        return temp.name

    def build_html_output(self, levels, ips, timeline, pie_path, ip_path):
        html = f"<h2><b>Log Analysis Results for {self.selected_file}</b></h2><hr><br>"

        # log level summary
        html += "<h3><b>Log Levels:</b></h3>"
        for lvl, count in levels.items():
            color = "green" if lvl == "INFO" else "red" if lvl == "ERROR" else "orange"
            html += f"<b><span style='color:{color}'>{lvl}</span>:</b> {count}<br>"

        html += "<br><hr>"

        # top ip addresses
        html += "<h3><b>Top IP Addresses:</b></h3>"
        for ip, count in sorted(ips.items(), key=lambda x: x[1], reverse=True)[:10]:
            html += f"{ip}: <b>{count}</b><br>"

        html += "<br><hr>"

        # timestamp activity 
        html += "<h3><b>Activity Timeline (Top 10):</b></h3>"
        for ts, count in sorted(timeline.items(), key=lambda x: x[1], reverse=True)[:10]:
            html += f"{ts}: <b>{count}</b><br>"

        html += "<br><hr>"

        # embed pie chart
        if pie_path:
            html += f"<img src='{pie_path}' width='400'><br><br>"

        # embed ip chart
        if ip_path:
            html += f"<img src='{ip_path}' width='500'><br><br>"

        return html
