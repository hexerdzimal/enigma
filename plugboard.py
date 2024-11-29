from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen

class SteckbrettWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steckbrett")
        self.setGeometry(200, 200, 1000, 300)

        self.points = []  # Liste der Punkte
        self.connections = []  # Liste der Verbindungen
        self.selected_point = None  # Aktuell ausgewählter Punkt

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.create_points()

    def create_points(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.point_positions = []
        row_gap = 70  # Abstand zwischen den Reihen
        col_gap = 70  # Abstand zwischen den Spalten
        radius = 10   # Radius der Punkte

        for i, letter in enumerate(alphabet):
            row = i // 10
            col = i % 10
            x = 50 + col * col_gap
            y = 80 + row * row_gap
            self.point_positions.append((x, y, letter))
            self.points.append(self.create_point_widget(letter, x, y, radius))

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
        if self.selected_point is None:
            self.selected_point = point
            point.setStyleSheet("border-radius: 10px; background-color: orange;")

        elif self.selected_point == point:
            point.setStyleSheet("border-radius: 10px; background-color: black;")
            self.selected_point = None

        elif self.are_points_connected(self.selected_point, point):
            self.delete_connection(self.selected_point, point)
            self.selected_point.setStyleSheet("border-radius: 10px; background-color: black;")
            self.selected_point = None

        elif not self.is_point_connected(point) and not self.is_point_connected(self.selected_point):
            self.create_connection(self.selected_point, point)
            self.selected_point.setStyleSheet("border-radius: 10px; background-color: black;")
            self.selected_point = None

        else:
            self.show_error_message("Punkte sind bereits verbunden oder ungültige Aktion!")

    def is_point_connected(self, point):
        return any(point in connection for connection in self.connections)

    def are_points_connected(self, point1, point2):
        return (point1, point2) in self.connections or (point2, point1) in self.connections

    def create_connection(self, point1, point2):
        self.connections.append((point1, point2))
        self.update()  # Steckbrett neu zeichnen

    def delete_connection(self, point1, point2):
        self.connections = [conn for conn in self.connections if conn != (point1, point2) and conn != (point2, point1)]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.white, 2))
        for point1, point2 in self.connections:
            pos1 = point1.pos() + point1.rect().center()
            pos2 = point2.pos() + point2.rect().center()
            painter.drawLine(pos1, pos2)

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Fehler")
        msg_box.exec()
