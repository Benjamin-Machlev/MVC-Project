class Movie:
    def __init__(self, movieID, title, release_year, genre, rating, runtime, description, responses, image):
        self.movieID = movieID
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.rating = rating
        self.runtime = runtime 
        self.description = description
        self.responses = responses
        self.image = image

    def __str__(self):
        return f"{self.title} ({self.release_year}), Genre: {self.genre}, Rating: {self.rating}/10"
