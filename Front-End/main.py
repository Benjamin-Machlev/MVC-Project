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

    #apply_stylesheet(app, theme='dark_teal.xml')
    model = MovieModel()
    view = MovieView(None, model.movies)  # Initialize view first
    controller = MovieController(model, view)  # Pass view to controller
    view.controller = controller  # Set the controller for the view
    view.init_ui()  # Initialize UI after setting the controller
    controller.run()
    app.exec()

if __name__ == '__main__':
    main()

