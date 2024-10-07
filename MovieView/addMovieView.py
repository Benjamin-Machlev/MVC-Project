from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout

class AddMovieForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # self.movie_id_input = QLineEdit()
        # self.movie_id_input.setObjectName("addMovieInput")
        # self.title_input = QLineEdit()
        # self.title_input.setObjectName("addMovieInput")
        # self.release_year_input = QLineEdit()
        # self.release_year_input.setObjectName("addMovieInput")
        # self.genre_input = QLineEdit()
        # self.genre_input.setObjectName("addMovieInput")
        
        # # Create rows for each input
        # self.add_row("Movie ID:", self.movie_id_input)
        # self.add_row("Title:", self.title_input)
        # self.add_row("Release Year:", self.release_year_input)
        # self.add_row("Genre:", self.genre_input)
        
        # self.add_button = QPushButton("Add Movie")
        # self.layout.addWidget(self.add_button)
        # self.add_button.clicked.connect(self.add_movie)
        
    # def add_row(self, label_text, input_widget):
    #     row_layout = QHBoxLayout()
    #     row_layout.addWidget(QLabel(label_text))
    #     row_layout.addWidget(input_widget)
    #     self.layout.addLayout(row_layout)
        
    def add_movie(self):
        # Implementation of add_movie method
        pass