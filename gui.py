import sys
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QGridLayout, QWidget, QSpacerItem, QSizePolicy, QHBoxLayout, QFrame, QCheckBox, QGroupBox, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from plugboard import SteckbrettWindow


class EnigmaGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enigma-Simulation")
        self.setGeometry(100, 100, 1000, 600)  # Fenstergröße

        # Hauptlayout
        main_layout = QHBoxLayout(self)

        # Linke Spalte für Optionen
        options_layout = QVBoxLayout()
        options_layout.setSpacing(10)

        # Gruppe für Optionen
        options_group = QGroupBox("Optionen")
        options_group.setLayout(options_layout)

        # Option: Checkbox für das Steckbrett
        self.steckbrett_checkbox = QCheckBox("Steckbrett verwenden")
        self.steckbrett_checkbox.setChecked(False)
        self.steckbrett_checkbox.stateChanged.connect(self.toggle_steckbrett)  # Verbindung zur Funktion

        options_layout.addWidget(self.steckbrett_checkbox)

        # Füge die Optionen-Spalte zum Hauptlayout hinzu
        main_layout.addWidget(options_group)

        # Setze eine maximale Höhe und passende Breite für die Optionen-Spalte
        options_group.setFixedHeight(self.height() // 2)
        options_group.setFixedWidth(self.steckbrett_checkbox.sizeHint().width() + 20)

        # Tasten und Lämpchen Layout rechts von den Optionen
        right_layout = QVBoxLayout()

        # Lämpchen-Reihen und Tastenlayouts
        self.lamps_layout_row1 = QGridLayout()
        self.lamps_layout_row2 = QGridLayout()
        self.lamps_layout_row3 = QGridLayout()

        self.add_lamps_to_row(self.lamps_layout_row1, ["Q", "W", "E", "R", "T", "Z", "U", "I", "O"], 0)
        self.add_lamps_to_row(self.lamps_layout_row2, ["A", "S", "D", "F", "G", "H", "J", "K"], 1)
        self.add_lamps_to_row(self.lamps_layout_row3, ["P", "Y", "X", "C", "V", "B", "N", "M", "L"], 2)

        # Rahmen um alle Lämpchen-Reihen
        lamps_frame = QFrame()
        lamps_frame.setLayout(self.create_all_lamps_layout())
        lamps_frame.setFrameShape(QFrame.Box)
        lamps_frame.setLineWidth(2)
        lamps_frame.setStyleSheet("border: 2px solid black;")
        right_layout.addWidget(lamps_frame)

        # Abstand zwischen den Lämpchen und den Tasten
        right_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # GridLayout für die Tasten
        self.keys_grid = QGridLayout()
        self.add_keys_to_grid(self.keys_grid)
        right_layout.addLayout(self.keys_grid)

        # Mapping der Tasten zu den Lämpchen
        self.key_to_lamp_mapping = self.create_key_to_lamp_mapping()

        # Füge den rechten Layout-Bereich zum Hauptlayout hinzu
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def toggle_steckbrett(self, state):
        # Funktion für das Ein- und Ausblenden des Steckbretts
        if state == 2:  # Checkbox ist angehakt
            print("Steckbrett wird geöffnet...")  # Debugging-Ausgabe
            if not hasattr(self, 'steckbrett_window'):  # Steckbrett nur einmal erstellen
                self.steckbrett_window = SteckbrettWindow()  # Erstelle das Steckbrett
            self.steckbrett_window.show()  # Steckbrett anzeigen
        else:
            print("Steckbrett wird geschlossen...")  # Debugging-Ausgabe
            if hasattr(self, 'steckbrett_window'):
                self.steckbrett_window.close()  # Steckbrett schließen
                del self.steckbrett_window  # Lösche die Referenz zum Fenster

    def add_keys_to_grid(self, layout):
        # Tastenreihen
        keys_row1 = ["Q", "W", "E", "R", "T", "Z", "U", "I", "O"]
        keys_row2 = ["A", "S", "D", "F", "G", "H", "J", "K"]
        keys_row3 = ["P", "Y", "X", "C", "V", "B", "N", "M", "L"]

        # Schriftart und Button-Stil
        font = QFont("Arial", 14)

        # Button-Stil für normale Ansicht und Mouseover (Hover)
        button_style = """
            QPushButton {
                background-color: black;
                color: lightgray;
                border-radius: 30px;
                font-size: 18px;
            }
            QPushButton:hover {
                color: orange;
            }
        """

        # Erste Reihe hinzufügen (keine Einrückung)
        for col, key in enumerate(keys_row1):
            btn = QPushButton(key)
            btn.setFont(font)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet(button_style)  # Setze den Stil
            btn.pressed.connect(self.handle_key_press)  # Signal für gedrückte Taste
            btn.released.connect(self.handle_key_release)  # Signal für losgelassene Taste
            layout.addWidget(btn, 0, col)

        # Zweite Reihe mit halber Spalten-Einrückung
        row2_layout = QHBoxLayout()
        row2_layout.addSpacerItem(QSpacerItem(30, 60, QSizePolicy.Fixed, QSizePolicy.Minimum))  # Spacer als halbe Spalte
        for key in keys_row2:
            btn = QPushButton(key)
            btn.setFont(font)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet(button_style)  # Setze den Stil
            btn.pressed.connect(self.handle_key_press)
            btn.released.connect(self.handle_key_release)
            row2_layout.addWidget(btn)

        # In das GridLayout einfügen, startend ab der zweiten Spalte (1)
        layout.addLayout(row2_layout, 1, 0, 1, len(keys_row1))  # Füge das Layout als eine Reihe ein

        # Dritte Reihe hinzufügen (keine Einrückung)
        for col, key in enumerate(keys_row3):
            btn = QPushButton(key)
            btn.setFont(font)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet(button_style)  # Setze den Stil
            btn.pressed.connect(self.handle_key_press)
            btn.released.connect(self.handle_key_release)
            layout.addWidget(btn, 2, col)

    def create_all_lamps_layout(self):
        # Layout, das alle Lämpchen-Reihen enthält
        all_lamps_layout = QVBoxLayout()

        # Füge alle drei Lämpchen-Reihen hinzu
        all_lamps_layout.addLayout(self.lamps_layout_row1)
        all_lamps_layout.addLayout(self.lamps_layout_row2)
        all_lamps_layout.addLayout(self.lamps_layout_row3)

        return all_lamps_layout

    def add_lamps_to_row(self, row_layout, keys, row_index):
        # Füge Lämpchen zu einer Reihe hinzu
        for col, key in enumerate(keys):
            lamp = QPushButton(key)  # Lämpchen bekommt den gleichen Text wie die Taste
            lamp.setFixedSize(40, 40)
            lamp.setStyleSheet("""
                background-color: lightgray;
                border: 1px solid black;
                border-radius: 20px;
                color: black;
            """)
            lamp.setEnabled(False)  # Button nicht klickbar
            row_layout.addWidget(lamp, 0, col)

    def create_key_to_lamp_mapping(self):
        # Mapping der Tasten zu den Lämpchen
        keys_row1 = ["Q", "W", "E", "R", "T", "Z", "U", "I", "O"]
        keys_row2 = ["A", "S", "D", "F", "G", "H", "J", "K"]
        keys_row3 = ["P", "Y", "X", "C", "V", "B", "N", "M", "L"]
        mapping = {}

        # Mapping für Reihe 1
        for i, key in enumerate(keys_row1):
            mapping[key] = (self.lamps_layout_row1, i)
        # Mapping für Reihe 2
        for i, key in enumerate(keys_row2):
            mapping[key] = (self.lamps_layout_row2, i)
        # Mapping für Reihe 3
        for i, key in enumerate(keys_row3):
            mapping[key] = (self.lamps_layout_row3, i)
        return mapping

    def handle_key_press(self):
        sender = self.sender()
        pressed_key = sender.text()
        print(f"Taste gedrückt: {pressed_key}")
        self.activate_lamp(pressed_key)

    def handle_key_release(self):
        sender = self.sender()
        released_key = sender.text()
        print(f"Taste losgelassen: {released_key}")
        self.deactivate_lamp(released_key)

    def activate_lamp(self, key):
        # Aktiviert das Glühlämpchen für den gedrückten Buchstaben
        row_layout, index = self.key_to_lamp_mapping.get(key, (None, None))
        if row_layout:
            lamp = row_layout.itemAt(index).widget()
            if lamp:
                lamp.setStyleSheet("""
                    background-color: yellow;
                    border: 1px solid black;
                    border-radius: 20px;
                    color: black;
                """)

    def deactivate_lamp(self, key):
        # Deaktiviert das Glühlämpchen für den losgelassenen Buchstaben
        row_layout, index = self.key_to_lamp_mapping.get(key, (None, None))
        if row_layout:
            lamp = row_layout.itemAt(index).widget()
            if lamp:
                lamp.setStyleSheet("""
                    background-color: lightgray;
                    border: 1px solid black;
                    border-radius: 20px;
                    color: black;
                """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnigmaGUI()
    window.show()
    sys.exit(app.exec())
