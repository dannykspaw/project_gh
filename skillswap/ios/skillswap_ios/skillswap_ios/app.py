import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import json
import urllib.request

API_BASE = "http://localhost:8000"

class SkillSwapApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)

        self.lat_input = toga.TextInput(placeholder="Lat", value="41.8781")
        self.lon_input = toga.TextInput(placeholder="Lon", value="-87.6298")
        self.skill_input = toga.TextInput(placeholder="Skill (optional)")
        self.search_btn = toga.Button("Search Nearby", on_press=self.on_search)

        self.results = toga.Table(headings=["User ID", "Display Name", "Mentor", "Lat", "Lon"], data=[])

        box = toga.Box(children=[
            toga.Box(children=[self.lat_input, self.lon_input, self.skill_input, self.search_btn], style=Pack(direction=ROW, padding=5, alignment="center", flex=0)),
            self.results
        ], style=Pack(direction=COLUMN, padding=10))

        self.main_window.content = box
        self.main_window.show()

    def on_search(self, widget):
        lat = self.lat_input.value or "41.8781"
        lon = self.lon_input.value or "-87.6298"
        skill = self.skill_input.value.strip()
        url = f"{API_BASE}/search/nearby?lat={lat}&lon={lon}"
        if skill:
            url += f"&skill={urllib.parse.quote(skill)}"
        try:
            with urllib.request.urlopen(url) as resp:
                items = json.loads(resp.read().decode())
                rows = []
                for r in items:
                    rows.append([str(r.get("user_id")), r.get("display_name") or "", str(bool(r.get("is_mentor"))), str(r.get("lat")), str(r.get("lon"))])
                self.results.data = rows
        except Exception as e:
            self.main_window.info_dialog("Error", str(e))

def main():
    return SkillSwapApp()
