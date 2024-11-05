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
    QTableWidget,
    QHeaderView,
    QSizePolicy,
    QStackedWidget,  
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from MovieView.singelMovieView import SingleMovie
from MovieView.addMovieView import AddMovieForm 


class MovieView(QMainWindow):
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
        self.create_movie_list()
        self.add_movie_form_widget = AddMovieForm(self)
        self.singel_movie_view = SingleMovie(self)

        self.stacked_widget.addWidget(self.movie_table)
        self.stacked_widget.addWidget(self.add_movie_form_widget)
        self.stacked_widget.addWidget(self.singel_movie_view)

        self.main_layout.addWidget(self.stacked_widget)

        self.main_layout.setStretch(0, 0)
        self.main_layout.setStretch(1, 6)

        self.create_footer()

        self.main_layout.setStretch(2, 0)

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

    def create_movie_list(self):
        self.movie_table = QTableWidget()
        self.movie_table.setRowCount(4)
        self.movie_table.setColumnCount(4)
        self.movie_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.movie_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.movie_table.horizontalHeader().setVisible(False)
        self.movie_table.verticalHeader().setVisible(False)

        for i in range(15):
            movie_frame = self.create_movie_frame(f"Movie {i + 1}")
            row = i // 4
            col = i % 4

            container_widget = QWidget()
            container_layout = QVBoxLayout(container_widget)
            container_layout.addWidget(movie_frame, alignment=Qt.AlignmentFlag.AlignCenter)

            self.movie_table.setCellWidget(row, col, container_widget)
            self.movie_table.setRowHeight(row, 500)

        self.movie_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.movie_table.setShowGrid(False)
        self.movie_table.setMaximumHeight(700)

    def create_movie_frame(self, movie_name):
        movie_widget = QWidget()
        movie_layout = QVBoxLayout(movie_widget)

        poster_button = QPushButton()
        poster_button.setCursor(Qt.CursorShape.PointingHandCursor)
        poster_button.clicked.connect(self.show_movie)

        pixmap = QPixmap(r"C:\Users\melon\Desktop\MVC - Project\test.jpg")
        
        if not pixmap.isNull():
            poster_button.setFixedSize(220, 325)
            scaled_pixmap = pixmap.scaled(
                poster_button.width() - 10,
                poster_button.height() - 10,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            poster_button.setIcon(scaled_pixmap)
            poster_button.setIconSize(scaled_pixmap.size())
        else:
            poster_button.setText("Image not found")

        movie_layout.addWidget(poster_button)

        movie_title = QLabel(movie_name)
        movie_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        movie_layout.addWidget(movie_title)

        movie_year = QLabel("2024")
        movie_year.setAlignment(Qt.AlignmentFlag.AlignLeft)
        movie_layout.addWidget(movie_year)

        return movie_widget

    def create_footer(self):
        footer_widget = QWidget()
        
        footer_layout = QHBoxLayout(footer_widget)
        footer_label = QLabel("© 2024 YTS.mx Example")
        footer_layout.addWidget(footer_label)

        self.main_layout.addWidget(footer_widget)

    def show_add_movie_form(self):
        self.stacked_widget.setCurrentWidget(self.add_movie_form_widget) 

    def show_movie_list(self):
        self.stacked_widget.setCurrentWidget(self.movie_table)

    def show_movie(self, movie):
        self.stacked_widget.setCurrentWidget(self.singel_movie_view)

