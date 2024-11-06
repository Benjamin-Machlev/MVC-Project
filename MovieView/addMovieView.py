from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QListWidget, QListWidgetItem, QGroupBox, QFormLayout, QSlider, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator

class AddMovieForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.minimum_field_width = 200
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        main_layout = QVBoxLayout(self)
        
        self.setup_inputs(main_layout)

        main_layout.addStretch()  

        main_layout.setAlignment(Qt.AlignCenter)

        self.layout.addLayout(main_layout)

        self.setup_buttons()

        self.layout.setContentsMargins(10, 10, 10, 10)


    def setup_inputs(self, main_layout):
        # Group Basic Info
        basic_info_group = QGroupBox("Basic Info")
        basic_info_group.setFixedWidth(500)  # הגבלת רוחב
        basic_layout = QFormLayout()
        
        self.movie_id_input = QLineEdit(self)
        self.movie_id_input.setValidator(QIntValidator(1, 9999999, self))
        self.movie_id_input.setPlaceholderText('Enter movie ID')
        
        self.movie_title_input = QLineEdit(self)
        self.movie_title_input.setPlaceholderText('Enter movie title')
        
        self.movie_director_input = QLineEdit(self)
        self.movie_director_input.setPlaceholderText('Enter movie director')
        
        self.movie_release_year_input = QLineEdit(self)
        self.movie_release_year_input.setPlaceholderText('Enter movie release year')
        
        self.movie_runtime_input = QLineEdit(self)
        self.movie_runtime_input.setPlaceholderText('Enter movie runtime')
        
        self.movie_image_input = QPushButton("Upload Image", self)
        self.movie_image_input.clicked.connect(self.upload_image)
        self.image_path_label = QLabel(self)

        basic_layout.addRow(QLabel('Movie ID:'), self.movie_id_input)
        basic_layout.addRow(QLabel('Title:'), self.movie_title_input)
        basic_layout.addRow(QLabel('Director:'), self.movie_director_input)
        basic_layout.addRow(QLabel('Release Year:'), self.movie_release_year_input)
        basic_layout.addRow(QLabel('Runtime:'), self.movie_runtime_input)
        basic_layout.addRow(QLabel('Image:'), self.movie_image_input)
        basic_layout.addRow(QLabel('Image Path:'), self.image_path_label)

        basic_info_group.setLayout(basic_layout)

        # Group Genres
        genre_group = QGroupBox("Genres")
        genre_group.setFixedWidth(500)  # הגבלת רוחב
        genre_layout = QVBoxLayout()
        
        self.genre_list = QListWidget(self)
        self.genre_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        
        genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller']
        for genre in genres:
            item = QListWidgetItem(genre)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.genre_list.addItem(item)
        
        genre_layout.addWidget(self.genre_list)
        genre_group.setLayout(genre_layout)

        # Group Additional Info
        additional_info_group = QGroupBox("Additional Info")
        additional_info_group.setFixedWidth(500)  # הגבלת רוחב
        additional_layout = QFormLayout()
        
        self.movie_rating_input = QSlider(Qt.Orientation.Horizontal, self)
        self.movie_rating_input.setMinimum(1)
        self.movie_rating_input.setMaximum(5)
        self.movie_rating_input.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.movie_rating_input.setTickInterval(1)
        self.movie_rating_input.setSingleStep(1)
        
        self.movie_description_input = QTextEdit(self)
        self.movie_description_input.setPlaceholderText('Enter movie description')
        self.movie_description_input.setFixedHeight(100)

        self.movie_response_input = QTextEdit(self)
        self.movie_response_input.setPlaceholderText('Enter movie response')

        additional_layout.addRow(QLabel('Rating:'), self.movie_rating_input)
        additional_layout.addRow(QLabel('Description:'), self.movie_description_input)
        additional_layout.addRow(QLabel('Response:'), self.movie_response_input)
        
        additional_info_group.setLayout(additional_layout)

        # הוספת כל קבוצה ללייאאוט המרכזי
        main_layout.addWidget(basic_info_group)
        main_layout.addWidget(genre_group)
        main_layout.addWidget(additional_info_group)

    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg)")
        
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.image_path_label.setText(file_path)

    def setup_buttons(self):
        # לייאאוט כפתורים בתחתית
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Movie", self)
        self.add_button.clicked.connect(self.add_movie)
        
        back_button = QPushButton("Back to Movie List", self)
        back_button.clicked.connect(self.go_back)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(back_button)
        button_layout.setAlignment(Qt.AlignCenter)

        # הוספת הכפתורים בתחתית
        self.layout.addLayout(button_layout)

    def add_movie(self):
        selected_genres = [self.genre_list.item(i).text() for i in range(self.genre_list.count())
                           if self.genre_list.item(i).checkState() == Qt.CheckState.Checked]
        
        print("Selected genres:", selected_genres)
        print("Selected rating:", self.movie_rating_input.value())
        print("Movie description:", self.movie_description_input.toPlainText())
        print("Movie response:", self.movie_response_input.toPlainText())

    def go_back(self):
        if self.parent:
            self.parent.show_movie_list()
