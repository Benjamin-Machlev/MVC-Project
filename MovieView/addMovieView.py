from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class AddMovieForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Setup the UI components and layout"""
        layout = QVBoxLayout(self)

        # Example UI fields
        self.movie_title_input = QLineEdit(self)
        self.movie_title_input.setPlaceholderText('Enter movie title')

        self.add_button = QPushButton("Add Movie", self)
        self.add_button.clicked.connect(self.add_movie)

        # Button to go back to the movie list
        back_button = QPushButton("Back to Movie List", self)
        back_button.clicked.connect(self.parent.show_movie_list)  # חזרה לרשימת הסרטים

        # Adding widgets to the layout
        layout.addWidget(QLabel('Add Movie'), alignment=Qt.AlignmentFlag.AlignCenter)  # ממקם את התווית במרכז
        layout.addWidget(self.movie_title_input, alignment=Qt.AlignmentFlag.AlignCenter)  # ממקם את שדה הקלט במרכז
        layout.addWidget(self.add_button, alignment=Qt.AlignmentFlag.AlignCenter)  # ממקם את כפתור ההוספה במרכז
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter) 
        layout.addStretch(1)  # מאפשר גובה גמיש למרווח

        self.setLayout(layout)

    def add_movie(self):
        """Handles the action of adding a movie"""
        movie_title = self.movie_title_input.text()
        if movie_title:
            print(f"Movie added: {movie_title}")
            self.movie_title_input.clear()  # ניקוי שדה הקלט לאחר ההוספה
        else:
            print("No movie title entered")
