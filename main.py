from PySide6.QtWidgets import QApplication, QPushButton
from qt_material import apply_stylesheet

app = QApplication([])

# יישום עיצוב Material Design
apply_stylesheet(app, theme='dark_blue.xml')

button = QPushButton("Click Me")
button.show()

app.exec()