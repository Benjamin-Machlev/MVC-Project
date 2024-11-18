using static System.Net.Mime.MediaTypeNames;
using System.IO;

namespace MoviesServer
{
    public class Movie
    {
        public int MovieID { get; set; }
        public string Title { get; set; }
        public string Director { get; set; }
        public int ReleaseYear { get; set; }
        public string Genre { get; set; }
        public double Rating { get; set; }
        public int Runtime { get; set; }
        public string Description { get; set; }
        public string Responses { get; set; }
        public string Image { get; set; }

        public Movie(int movieID, string title, string director, int releaseYear, string genre, double rating, int runtime, string description, string responses, string image)
        {
            MovieID = movieID;
            Title = title;
            Director = director;
            ReleaseYear = releaseYear;
            Genre = genre;
            Rating = rating;
            Runtime = runtime;
            Description = description;
            Responses = responses;
            Image = image;
        }
    }
}
