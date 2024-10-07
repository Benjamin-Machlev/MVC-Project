from rating import Rating
class Movie:
    def __init__(self,movieID, title, director, release_year, genre, rating):
        self.movieID = movieID
        self.title = title
        self.director = director
        self.release_year = release_year
        self.genre = genre
        self.rating = rating

    def __str__(self):
        return f"{self.title} ({self.release_year}), directed by {self.director}, Genre: {self.genre}, Rating: {self.rating}/10"