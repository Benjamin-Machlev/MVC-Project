class MovieController:
    def __init__(self, movieModel,movieView):
        self.movieModel = movieModel
        self.movieView = movieView

    def run(self):
        self.movieView.show()
