using static System.Net.Mime.MediaTypeNames;
using System.IO;

namespace MoviesServer.Models
{
    public class Movie
    {
        public int MovieID { get; set; }
        public string Title { get; set; }
        public string Director { get; set; }
        public int ReleaseYear { get; set; }
        public string Genre { get; set; }
        public decimal Rating { get; set; }
        public int Runtime { get; set; }
        public string Description { get; set; }
        public List<string> Responses { get; set; }
        public string Image { get; set; }

        public Movie(int movieID, string title, string director, int releaseYear, string genre, decimal rating, int runtime, string description, List<string> responses, string image)
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
