import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QStackedWidget,  
    QFrame,
    QSpacerItem,
    QGridLayout,
    QScrollArea
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from MovieView.singelMovieView import SingleMovieView
from MovieView.addMovieView import AddMovieForm 
from movie import Movie
from MovieView.updateMovieView import UpdateMovieForm


class MovieView(QMainWindow):
    movies = [
        Movie(1, "The Shawshank Redemption", "Frank Darabont", 1994, "Drama", 9.3, 142, 
            "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/1.jpeg"),
        Movie(2, "The Godfather", "Francis Ford Coppola", 1972, "Crime, Drama", 9.2, 175, 
            "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/2.jpeg"),
        Movie(3, "The Dark Knight", "Christopher Nolan", 2008, "Action, Crime, Drama", 9.0, 152, 
            "When the menace known as The Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/3.jpeg"),
        Movie(4, "Schindler's List", "Steven Spielberg", 1993, "Biography, Drama, History", 8.9, 195, 
            "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/4.jpeg"),
        Movie(5, "Pulp Fiction", "Quentin Tarantino", 1994, "Crime, Drama", 8.9, 154, 
            "The lives of two mob hitmen, a boxer, a gangster, and his wife intertwine in four tales of violence and redemption.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/5.jpeg"),
        Movie(6, "The Lord of the Rings: The Return of the King", "Peter Jackson", 2003, "Action, Adventure, Drama", 8.9, 201, 
            "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/6.jpeg"),
        Movie(7, "Forrest Gump", "Robert Zemeckis", 1994, "Drama, Romance", 8.8, 142, 
            "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/7.jpeg"),
        Movie(8, "Fight Club", "David Fincher", 1999, "Drama", 8.8, 139, 
            "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much more.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/8.jpeg"),
        Movie(9, "Inception", "Christopher Nolan", 2010, "Action, Adventure, Sci-Fi", 8.8, 148, 
            "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", 
            "Positive", r"Front-End\movies img/9.jpeg"),
        Movie(10, "The Matrix", "Lana Wachowski, Lilly Wachowski", 1999, "Action, Sci-Fi", 8.7, 136, 
            "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/10.jpeg"),
        Movie(11, "The Silence of the Lambs", "Jonathan Demme", 1991, "Crime, Drama, Thriller", 8.6, 118, 
            "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to catch another serial killer.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/11.jpeg"),
        Movie(12, "Se7en", "David Fincher", 1995, "Crime, Drama, Mystery", 8.6, 127, 
            "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/12.jpeg"),
        Movie(13, "Gladiator", "Ridley Scott", 2000, "Action, Adventure, Drama", 8.5, 155, 
            "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/13.jpeg"),
        Movie(14, "The Prestige", "Christopher Nolan", 2006, "Drama, Mystery, Sci-Fi", 8.5, 130, 
            "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/14.jpeg"),
        Movie(15, "The Departed", "Martin Scorsese", 2006, "Crime, Drama, Thriller", 8.5, 151, 
            "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.", 
            ["Positive", "Nice Movie"], r"Front-End\movies img/15.jpeg")]

    def __init__(self, model):
        super().__init__()
        self.model = model

        self.setWindowTitle('YTS.mx Like UI')
        self.setGeometry(400, 100, 800, 600)

        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)

        self.top_bar_widget = None
        self.add_movie_form_widget = None
        self.stacked_widget = QStackedWidget(self.central_widget)

        self.init_ui()
        self.setCentralWidget(self.central_widget)
        self.showMaximized()


    def init_ui(self):
        self.create_top_bar()
        self.main_layout.addWidget(self.top_bar_widget)

        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.create_movie_list(movies=self.movies)
        self.add_movie_form_widget = AddMovieForm(self)
        self.singel_movie_view = SingleMovieView(self)
        self.update_movie_form_widget = UpdateMovieForm(self)

        self.stacked_widget.addWidget(self.movie_list_widget)
        self.stacked_widget.addWidget(self.add_movie_form_widget)
        self.stacked_widget.addWidget(self.singel_movie_view)
        self.stacked_widget.addWidget(self.update_movie_form_widget)

        self.main_layout.addWidget(self.stacked_widget)

        self.main_layout.setStretch(0, 0)
        self.main_layout.setStretch(1, 6)

        self.create_footer()

        self.main_layout.setStretch(2, 0)



    def show_movie_list(self):
        self.stacked_widget.setCurrentWidget(self.movie_list_widget)

    def show_add_movie_form(self):
        self.stacked_widget.setCurrentWidget(self.add_movie_form_widget) 

    def show_movie(self, movie):
        self.singel_movie_view.set_movie(movie)
        self.stacked_widget.setCurrentWidget(self.singel_movie_view)

    def show_update_movie_form(self, movie):
        self.update_movie_form_widget.movie = movie
        self.update_movie_form_widget.populate_fields()
        self.stacked_widget.setCurrentWidget(self.update_movie_form_widget)


    def create_top_bar(self):
        self.top_bar_widget = QWidget(self)
        self.top_bar_layout = QHBoxLayout(self.top_bar_widget)
        self.top_bar_layout.setContentsMargins(20, 20, 20, 20)
        self.top_bar_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        site_title = QLabel("YTS.mx")
        self.top_bar_layout.addWidget(site_title)

        self.top_bar_layout.addStretch(1)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search movies...")
        self.top_bar_layout.addWidget(search_input)

        search_button = QPushButton("Search")
        search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.top_bar_layout.addWidget(search_button)

        self.top_bar_layout.addStretch(1)
        add_button = QPushButton("Add")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.top_bar_layout.addWidget(add_button)
        add_button.clicked.connect(self.show_add_movie_form)

    def create_movie_list(self, movies):
        self.movie_list_widget = QWidget(self)
        outer_layout = QVBoxLayout(self.movie_list_widget)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        for index, movie in enumerate(movies):
            row = index // 4
            col = index % 4
            movie_frame = self.create_movie_frame(movie)
            grid_layout.addWidget(movie_frame, row, col, alignment=Qt.AlignCenter)
        
        grid_layout.setRowStretch(grid_layout.rowCount(), 1)
        content_layout.addLayout(grid_layout)
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)      
        outer_layout.addWidget(scroll_area)

        

    def create_movie_frame(self, movie):
        frame = QFrame()
        frame.setFixedSize(220, 360)  
        layout = QVBoxLayout(frame)
        
        image_button = QPushButton()
        image_button.setIcon(QPixmap(movie.image))
        image_button.setIconSize(QSize(200, 315))
        image_button.setFixedSize(QSize(200, 315))
        image_button.setCursor(Qt.CursorShape.PointingHandCursor)
        image_button.clicked.connect(lambda _, m=movie: self.show_movie(m))

        title_label = QLabel(f"<b>{movie.title}</b><br>({movie.release_year})")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)  # במידה ויש כותרים ארוכים יותר

        layout.addWidget(image_button, alignment=Qt.AlignTop)
        layout.addWidget(title_label, alignment=Qt.AlignTop)
        
        return frame


    def create_footer(self):
        footer_widget = QWidget()
        
        footer_layout = QHBoxLayout(footer_widget)
        footer_label = QLabel("© 2024 YTS.mx Example")
        footer_layout.addWidget(footer_label)

        self.main_layout.addWidget(footer_widget)



