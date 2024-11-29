from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QPainterPath


class SteckbrettWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steckbrett")
        self.setGeometry(200, 200, 1200, 300)

        self.points = []  # Liste der Stecker (QLabels)
        self.connections = {}  # Dictionary: Key=Stecker, Value=Verbundener Stecker
        self.selected_point = None  # Der aktuell ausgewählte Stecker
        self.point_positions = {}  # Dictionary für Stecker -> Position + Buchstaben

        self.init_ui()

    def init_ui(self):
        # Layout für das Hauptfenster (Stecker und Textbereich)
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Layout für die Stecker (links)
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, stretch=3)

        # Layout für die verbundenen Buchstaben (rechts)
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, stretch=1)

        # Textfeld für die verbundenen Buchstaben
        self.connected_letters_display = QTextEdit(self)
        self.connected_letters_display.setReadOnly(True)  # Nur lesen, keine Bearbeitung
        right_layout.addWidget(self.connected_letters_display)

        self.create_points()

    def create_points(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        row_gap = 70  # Abstand zwischen den Reihen
        col_gap = 70  # Abstand zwischen den Spalten
        radius = 10   # Radius der Stecker

        for i, letter in enumerate(alphabet):
            row = i // 10
            col = i % 10
            x = 50 + col * col_gap
            y = 80 + row * row_gap
            point = self.create_point_widget(letter, x, y, radius)
            self.points.append(point)

            # Speichern der Position und des Buchstabens für später im Dictionary
            self.point_positions[point] = (x, y, letter)

            # Initialisiere die Verbindungen als leer (kein Stecker verbunden)
            self.connections[point] = None

    def create_point_widget(self, letter, x, y, radius):
        point = QLabel(self)
        point.setGeometry(x, y, radius * 2, radius * 2)
        point.setStyleSheet("border-radius: 10px; background-color: black;")
        point.mousePressEvent = lambda event, pt=point: self.handle_stecker_click(pt)

        label = QLabel(letter, self)
        label.setGeometry(x + 25, y - 5, 20, 20)
        label.setStyleSheet("color: white; font-size: 24px;")

        return point

    def handle_stecker_click(self, point):
        # Überprüfe den aktuellen Zustand des Punktes
        if self.selected_point is None:
            # Kein Punkt ausgewählt, Stecker auswählen
            if self.connections[point] is None:
                self.selected_point = point
                point.setStyleSheet("border-radius: 10px; background-color: orange;")
            else:
                # Der Stecker ist bereits verbunden, daher löschen wir die Verbindung
                self.delete_connection(point)
        elif self.selected_point == point:
            # Wenn der selbe Stecker erneut ausgewählt wird, abwählen
            self.selected_point.setStyleSheet("border-radius: 10px; background-color: black;")
            self.selected_point = None
        else:
            # Wenn der erste Stecker bereits ausgewählt ist, eine Verbindung erstellen oder löschen
            if self.connections[point] is None:
                self.create_connection(self.selected_point, point)
            else:
                self.delete_connection(self.selected_point)

    def create_connection(self, point1, point2):
        # Verbindung erstellen
        self.connections[point1] = point2
        self.connections[point2] = point1
        point1.setStyleSheet("border-radius: 10px; background-color: black;")
        point2.setStyleSheet("border-radius: 10px; background-color: black;")
        self.selected_point = None
        self.update()  # Steckbrett neu zeichnen
        self.update_connected_letters()

    def delete_connection(self, point):
        # Verbindung löschen
        connected_point = self.connections[point]
        if connected_point:
            self.connections[connected_point] = None
            self.connections[point] = None
            connected_point.setStyleSheet("border-radius: 10px; background-color: black;")
            point.setStyleSheet("border-radius: 10px; background-color: black;")
        self.selected_point = None
        self.update()  # Steckbrett neu zeichnen
        self.update_connected_letters()

    def update_connected_letters(self):
        # Alle verbundenen Buchstaben ermitteln und anzeigen
        connected_letters = []

        for point1, point2 in self.connections.items():
            if point2 is not None and point1 != point2:  # Überprüfe, ob der Punkt verbunden ist
                # Buchstaben des verbundenen Steckers ermitteln
                letter1 = self.get_letter_for_point(point1)
                letter2 = self.get_letter_for_point(point2)
                connected_letters.append(f"{letter1} - {letter2}")

        # Verbundene Buchstaben im Textfeld anzeigen
        self.connected_letters_display.setText("\n".join(connected_letters))

    def get_letter_for_point(self, point):
        # Suche nach dem Buchstaben für einen bestimmten Stecker im Dictionary
        if point in self.point_positions:
            return self.point_positions[point][2]  # Der Buchstabe ist das dritte Element des Tupels
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.white, 4))  # Einheitliche Farbe (weiß) und Linienbreite (2)

        # Alle Verbindungen zeichnen
        for point1, point2 in self.connections.items():
            if point2 is not None:
                pos1 = QPointF(point1.pos() + point1.rect().center())  # Position von Punkt 1
                pos2 = QPointF(point2.pos() + point2.rect().center())  # Position von Punkt 2

                # Steuerpunkte für die Bézier-Kurve berechnen
                control_point1 = pos1 + (pos2 - pos1) * 0.3 + QPointF(0, 60)
                control_point2 = pos1 + (pos2 - pos1) * 0.7 + QPointF(0, 60)

                # Bézier-Kurve erstellen und zeichnen
                path = QPainterPath()
                path.moveTo(pos1)
                path.cubicTo(control_point1, control_point2, pos2)
                painter.drawPath(path)

    def get_connected_letter_by_label(self, letter):
        # Durch alle Verbindungen iterieren
        for point1, point2 in self.connections.items():
            if point2 is not None:
                # Buchstabe des ersten und des verbundenen Steckers ermitteln
                letter1 = self.get_letter_for_point(point1)
                letter2 = self.get_letter_for_point(point2)
                
                # Wenn eines der Labels mit dem übergebenen Buchstaben übereinstimmt
                if letter1 == letter:
                    return letter2
                elif letter2 == letter:
                    return letter1
        
        # Falls keine Verbindung mit dem angegebenen Buchstaben gefunden wird, None zurückgeben
        return letter

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Fehler")
        msg_box.exec()
