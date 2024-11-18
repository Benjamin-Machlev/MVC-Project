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
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize
from MovieView.singelMovieView import SingleMovieView
from MovieView.addMovieView import AddMovieForm 
from Entity.movie import Movie
from MovieView.updateMovieView import UpdateMovieForm


class MovieView(QMainWindow):
    def __init__(self, controller, movies):
        super().__init__()
        self.controller = controller
        self.movies = movies
        self.setWindowTitle('YTS.mx Like UI')
        self.setGeometry(400, 100, 800, 600)

        # Set the window icon
        icon_path = r"Front-End\movies img\theaters.svg"
        self.setWindowIcon(QIcon(icon_path))

        # Set the taskbar icon
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'YTS.mx')

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

        self.add_movie_form_widget.add_movie_signal.connect(self.controller.add_movie)
        self.add_movie_form_widget.go_back_signal.connect(self.show_movie_list)
        self.singel_movie_view.show_update_movie_form_signal.connect(self.controller.show_update_movie_form)
        self.singel_movie_view.delete_movie_signal.connect(self.controller.delete_movie)
        self.singel_movie_view.add_response_signal.connect(self.controller.add_response)
        self.singel_movie_view.back_to_movie_list_signal.connect(self.show_movie_list)
        self.update_movie_form_widget.update_movie_signal.connect(self.controller.update_movie)
        self.update_movie_form_widget.go_back_signal.connect(self.show_movie_list)

        self.main_layout.addWidget(self.stacked_widget)

        self.main_layout.setStretch(0, 0)
        self.main_layout.setStretch(1, 6)

        self.create_footer()

        self.main_layout.setStretch(2, 0)

        self.controller.refresh_movie_list()


    def show_movie_list(self):
        self.create_movie_list(self.controller.movieModel.movies)
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

    def delete_movie(self, movie_id):
        self.controller.delete_movie(movie_id)
        self.show_movie_list()

    def create_top_bar(self):
        self.top_bar_widget = QWidget(self)
        self.top_bar_layout = QHBoxLayout(self.top_bar_widget)
        self.top_bar_layout.setContentsMargins(20, 20, 20, 20)
        self.top_bar_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Add the icon to the top bar
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(r"Front-End\movies img\theaters.svg").scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.top_bar_layout.addWidget(icon_label)

        site_title = QLabel("YTS.mx")
        self.top_bar_layout.addWidget(site_title)

        self.top_bar_layout.addStretch(1)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search movies...")
        search_input.setFixedSize(300, 30)
        search_input.setStyleSheet("color: white;")
        self.top_bar_layout.addWidget(search_input)

        search_button = QPushButton("Search")
        search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        search_button.setFixedSize(300,30)
        #search_button.setProperty("class", "success")
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

        image_button = QPushButton()
        image_button.setIcon(QPixmap(movie.image))
        image_button.setIconSize(QSize(200, 315))
        image_button.setFixedSize(QSize(200, 315))
        image_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        image_button.clicked.connect(lambda _, m=movie: self.show_movie(m))

        title_label = QLabel(f"<b>{movie.title}</b><br>({movie.release_year})")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)

        movie_frame = QVBoxLayout()
        movie_frame.addWidget(image_button)
        movie_frame.addWidget(title_label)
        
        frame_widget = QWidget()
        frame_widget.setLayout(movie_frame)
        
        return frame_widget

    def create_footer(self):
        footer_widget = QWidget()
        
        footer_layout = QHBoxLayout(footer_widget)
        footer_label = QLabel("© 2024 YTS.mx Example")
        footer_layout.addWidget(footer_label)

        self.main_layout.addWidget(footer_widget)



