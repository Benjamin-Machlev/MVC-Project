import sys
from PySide6.QtWidgets import QApplication, QWidget
from MovieModel.movieModel import MovieModel
from MovieView.movieView import MovieView
from MovieController.movieController import MovieController
from qt_material import apply_stylesheet

def main():
    app = QApplication([])
    with open(r"Front-End\MovieView\style.qss", "r", encoding="utf-8") as style_file:
        app.setStyleSheet(style_file.read())

    model = MovieModel()
    controller = MovieController(model, None)  # Initialize controller first
    view = MovieView(controller, model.movies)  # Pass controller to MovieView
    controller.movieView = view  # Set the view for the controller
    controller.run()
    app.exec()

if __name__ == '__main__':
    main()

