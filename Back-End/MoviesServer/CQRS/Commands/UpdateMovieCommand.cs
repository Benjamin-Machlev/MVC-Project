using MoviesServer.DataAccess;
using MoviesServer.Models;
namespace MoviesServer.CQRS.Commands
{
    public class UpdateMovieCommand
    {
        private readonly MoviesContext _context;

        public UpdateMovieCommand(MoviesContext context)
        {
            _context = context;
        }

        public void UpdateMovie(int id, Movie movie)
        {
            if (id != movie.MovieID)
            {
                throw new System.Exception("Invalid movie ID");
            }
            _context.Entry(movie).State = Microsoft.EntityFrameworkCore.EntityState.Modified;
            _context.SaveChanges();
        }
    }
}
