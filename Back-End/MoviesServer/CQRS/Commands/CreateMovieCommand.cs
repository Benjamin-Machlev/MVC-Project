
using MoviesServer.DataAccess;
using MoviesServer.Models;

namespace MoviesServer.CQRS.Commands
{
    public class CreateMovieCommand
    {
        private readonly MoviesContext _context;

        public CreateMovieCommand(MoviesContext context)
        {
            _context = context;

        }
        public void AddMovie(Movie movie)
        {
             _context.Movies.Add(movie);
            _context.SaveChanges();
        }
    }
}
