from Entity.movie import Movie

class MovieController:
    def __init__(self, movieModel, movieView):
        self.movieModel = movieModel
        self.movieView = movieView

    def run(self):
        self.movieView.show()

    def show_movie_list(self):
        self.movieView.show_movie_list()

    def show_add_movie_form(self):
        self.movieView.show_add_movie_form()

    def show_movie(self, movie):
        self.movieView.show_movie(movie)

    def show_update_movie_form(self, movie):
        self.movieView.show_update_movie_form(movie)

    def add_movie(self, movie_data):
        movie = Movie(
            movie_data["movie_id"], movie_data["title"], movie_data["director"],
            movie_data["release_year"], ", ".join(movie_data["genres"]),
            movie_data["rating"], movie_data["runtime"], movie_data["description"],
            [movie_data["response"]]
        )
        self.movieModel.add_movie(movie)
        self.show_movie_list()

    def update_movie(self, movie_data):
        movie = Movie(
            movie_data["movie_id"], movie_data["title"], movie_data["director"],
            movie_data["release_year"], ", ".join(movie_data["genres"]),
            movie_data["rating"], movie_data["runtime"], movie_data["description"],
            [movie_data["response"]]
        )
        self.movieModel.update_movie(movie_data["movie_id"], movie)
        self.show_movie_list()

    def add_response(self, movie, response_text):
        movie.responses.append(response_text)
        self.show_movie(movie)

    def delete_movie(self, movie_id):
        self.movieModel.delete_movie(movie_id)
        self.show_movie_list()

    def refresh_movie_list(self):
        self.movieModel.initialize_movies()
        if self.movieView:
            self.show_movie_list()
