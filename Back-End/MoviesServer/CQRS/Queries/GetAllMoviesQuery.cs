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
            return _context.Movies.ToList();
        }
    }
}
