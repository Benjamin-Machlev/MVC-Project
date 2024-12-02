using MoviesServer.DataAccess;
using MoviesServer.Models;

namespace MoviesServer.CQRS.Commands
{
    public class DeleteMovieCommand
    {
        private readonly MoviesContext _context;

        public DeleteMovieCommand(MoviesContext context)
        {
            _context = context;
        }

        public void DeleteMovie(int id)
        {
            var movie = _context.Movies.Find(id);
            if (movie == null)
            {
                throw new System.Exception("Invalid movie ID");
            }
            _context.Movies.Remove(movie);
            _context.SaveChanges();
        }
    }
}
