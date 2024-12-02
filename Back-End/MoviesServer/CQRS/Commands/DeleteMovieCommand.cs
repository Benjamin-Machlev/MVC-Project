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
            try
            {
                var movie = _context.Movies.Find(id);
                if (movie == null)
                {
                    throw new System.Exception("Invalid movie ID");
                }
                _context.Movies.Remove(movie);
                _context.SaveChanges();
            }
            catch (System.Exception ex)
            {
                throw new System.Exception($"Error deleting movie with ID {id}: {ex.Message}");
            }
        }
    }
}
