from PyQt6.QtWidgets                import QWidget, QLabel, QTextEdit, QMessageBox
from DefaultStyles.button_style     import DefaultButtonStyle, DefaultAboutButtonStyle
from DefaultStyles.qline_edit_style import DefaultQLineEditStyle
from geopy.geocoders                import Nominatim
from pathlib                        import Path
import folium, time, os, webbrowser, time

class ShowOnMapWindow(QWidget):

    def __init__(self, theme_mode):
        super().__init__()
        self.theme_mode = theme_mode

        msgbox_title = "About Show on Map Tool"
        msgbox_txt = (
            "<p><strong>Show on Map</strong> is a custom geolocation tool designed to display a specific location on a map "
            "based on user-provided latitude and longitude coordinates. This tool utilizes the <em>Geopy</em> library to retrieve "
            "the address information and <em>Folium</em> to create an interactive HTML map that can be opened on your desktop.</p>"

            "<p><strong>How to Use:</strong></p>"
            "<ol>"
            "<li>Enter the latitude and longitude in the provided input fields.</li>"
            "<li>Click 'Submit' to generate the address information and map.</li>"
            "<li>If valid coordinates are given, an address will be displayed, and a map file named <em>map.html</em> will be saved on the desktop.</li>"
            "<li>To view the map, click 'Open File' in the prompt to launch it in an external browser (Firefox).</li>"
            "</ol>"

            "<p><strong>Applications:</strong></p>"
            "<ul>"
            "<li>Use this tool for pinpointing addresses based on GPS coordinates.</li>"
            "<li>Generate maps to visually confirm or document specific geolocations.</li>"
            "</ul>"

            "<h3>Useful Links:</h3>"
            "<ul>"
            "<li><a href='https://geopy.readthedocs.io/'>Geopy Documentation</a></li>"
            "<li><a href='https://python-visualization.github.io/folium/'>Folium Documentation</a></li>"
            "<li><a href='https://nominatim.org/release-docs/latest/api/Overview/'>Nominatim API</a></li>"
            "</ul>")

        self.setWindowTitle("Geolocation")
        self.setFixedSize(700, 550)

        # Longitude input
        longitude_label = QLabel("Give longitude:", parent=self)
        longitude_label.setGeometry(50, 10, 110, 50)
        self.longitude_input = DefaultQLineEditStyle(parent=self)
        self.longitude_input.setGeometry(10, 60, 180, 50)

        # Latitude input
        latitude_label = QLabel("Give latitude:", parent=self)
        latitude_label.setGeometry(300, 10, 100, 50)
        self.latitude_input = DefaultQLineEditStyle(parent=self)
        self.latitude_input.setGeometry(280, 60, 180, 50)

        submit_button = DefaultButtonStyle("Submit", parent=self, bold=True, command=self.command)
        submit_button.setGeometry(500, 60, 100, 50)

        self.information_label = QTextEdit(parent=self)
        self.information_label.setGeometry(10, 150, 680, 250)
        self.information_label.setReadOnly(True)
        self.information_label.hide()

        self.saved_html_label = QTextEdit(parent=self)
        self.saved_html_label.setGeometry(10, 420, 680, 50)
        self.saved_html_label.setReadOnly(True)
        self.saved_html_label.hide()

        # About button setup
        self.aboutButton = DefaultAboutButtonStyle("", parent=self, txt=msgbox_txt, title=msgbox_title, geometry=(650, 500, 50, 50))
        self.aboutButton.update_theme(self.theme_mode)

    def command(self):
        try:
            if self.longitude_input.text():
                if self.latitude_input.text():
                    longitude = self.longitude_input.text()
                    latitude = self.latitude_input.text()

                    self.geoloc = Nominatim(user_agent="tutorial")

                    address = self.get_address_by_location(latitude=latitude, longitude=longitude)

                    self.information_label.clear()
                    self.information_label.setHtml(f"<b>Information:<b/><br>{str(address)}")
                    self.information_label.show()
                    self.show_map(latitude, longitude)

                    self.saved_html_label.clear()
                    self.saved_html_label.setHtml(f'map.html file successfully generated and saved at Desktop.')
                    self.saved_html_label.show()
                else:
                    raise ValueError('Please enter latitude.')
            else:
                raise ValueError('Please enter longitude.')
            
        except ValueError as ve:
            QMessageBox.warning(self, 'Error', str(ve))
        except Exception as e:
            QMessageBox.critical(self, 'Unexpected Error', str(e))

    def show_map(self, latitude, longitude):
        # create a map centered around the provided coordinates
        map_object = folium.Map(location=[float(latitude), float(longitude)], zoom_start=15)
        folium.Marker([float(latitude), float(longitude)], tooltip="Location").add_to(map_object)

        # path to save the map on the Desktop
        desktop_path = Path(os.path.expanduser("~/Desktop"))
        map_path = desktop_path / "map.html"
        map_object.save(str(map_path))

        # print the map path for debugging
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information) 
        msg_box.setText(f'File map.html created and saved at: {map_path}')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        open_file_btn = msg_box.addButton('Open File', QMessageBox.ButtonRole.ActionRole)
        msg_box.exec()

        if msg_box.clickedButton() == open_file_btn:
            # Open the map in an external browser (Firefox)
            webbrowser.get("firefox").open(f"file://{map_path}")

    def get_address_by_location(self, latitude, longitude, language="en"):
        """This function returns an address as raw from a location
        will repeat until success"""
        # build coordinates string to pass to reverse() function
        coordinates = f"{latitude}, {longitude}"
        # sleep for a second to respect Usage Policy
        time.sleep(1)
        try:
            return self.geoloc.reverse(coordinates, language=language).raw
        except:
            return self.get_address_by_location(latitude, longitude)
