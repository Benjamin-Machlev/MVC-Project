using MoviesServer.DataAccess;
using MoviesServer.Models;

namespace MoviesServer.CQRS.Queries
{
    public class GetAllMoviesQuery
    {
        readonly MoviesContext _context;
        public GetAllMoviesQuery(MoviesContext context)
        {
            _context = context;
        }

        public List<Movie> GetAllMovies()
        {
            try
            {
                return _context.Movies.ToList();
            }
            catch (Exception ex)
            {
                throw new Exception($"Error retrieving all movies: {ex.Message}");
            }
        }
    }
}
