from Entity.movie import Movie

class MovieModel:
    def __init__(self):
        self.movies = []
        self.initialize_movies()

    def initialize_movies(self):
        self.movies = [
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

    def add_movie(self, movie):
        self.movies.append(movie)

    def update_movie(self, movie_id, updated_movie):
        for i, movie in enumerate(self.movies):
            if movie.movieID == movie_id:
                self.movies[i] = updated_movie
                break

    def delete_movie(self, movie_id):
        self.movies = [movie for movie in self.movies if movie.movieID != movie_id]

    def get_movie(self, movie_id):
        for movie in self.movies:
            if movie.movieID == movie_id:
                return movie
        return None


