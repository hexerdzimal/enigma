import sys
from PySide6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QGridLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import sys
from PySide6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch  # Position, an der der nächste Rotor rotiert
        self.position = 0  # Startposition der Walze

    def rotate(self):
        self.position = (self.position + 1) % 26  # Dreht die Walze um eine Position weiter
        return self.position == self.notch  # True, wenn die Kerbe erreicht wurde

class RotorWidget(QWidget):
    def __init__(self, rotor):
        super().__init__()
        self.rotor = rotor
        self.label = QLabel(self.get_display_letter())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; border: 2px solid black; min-width: 60px; min-height: 60px;")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def get_display_letter(self):
        return chr((self.rotor.position + ord('A')) % 26)

    def rotate_display(self):
        self.rotor.rotate()
        self.label.setText(self.get_display_letter())

class EnigmaGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enigma-Simulation")
        self.setGeometry(100, 100, 800, 600)

        # Hauptlayout: Walzen oben, Tastatur unten
        main_layout = QVBoxLayout(self)

        # Walzen-Layout
        rotor_layout = QHBoxLayout()
        self.rotors = [Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 17),
                       Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 5),
                       Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 22)]

        self.rotor_widgets = [RotorWidget(rotor) for rotor in self.rotors]
        for rotor_widget in self.rotor_widgets:
            rotor_layout.addWidget(rotor_widget)

        main_layout.addLayout(rotor_layout)

        # Tastatur-Layout
        keys_layout = QGridLayout()
        self.add_keys_to_grid(keys_layout)
        main_layout.addLayout(keys_layout)

        self.setLayout(main_layout)

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
            btn.clicked.connect(self.handle_key_press)
            layout.addWidget(btn, 0, col)

        # Zweite Reihe mit halber Spalten-Einrückung
        row2_layout = QHBoxLayout()
        row2_layout.addSpacerItem(QSpacerItem(30, 60, QSizePolicy.Fixed, QSizePolicy.Minimum))  # Spacer als halbe Spalte
        for key in keys_row2:
            btn = QPushButton(key)
            btn.setFont(font)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet(button_style)  # Setze den Stil
            btn.clicked.connect(self.handle_key_press)
            row2_layout.addWidget(btn)
        
        # In das GridLayout einfügen, startend ab der zweiten Spalte (1)
        layout.addLayout(row2_layout, 1, 0, 1, len(keys_row1))  # Füge das Layout als eine Reihe ein

        # Dritte Reihe hinzufügen (keine Einrückung)
        for col, key in enumerate(keys_row3):
            btn = QPushButton(key)
            btn.setFont(font)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet(button_style)  # Setze den Stil
            btn.clicked.connect(self.handle_key_press)
            layout.addWidget(btn, 2, col)


    def handle_key_press(self):
        sender = self.sender()
        pressed_key = sender.text()
        print(f"Taste gedrückt: {pressed_key}")
        self.rotate_rotors()

    def rotate_rotors(self):
        for rotor_widget in self.rotor_widgets:
            rotor_widget.rotate_display()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnigmaGUI()
    window.show()
    sys.exit(app.exec())
