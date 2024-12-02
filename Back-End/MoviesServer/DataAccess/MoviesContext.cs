using Microsoft.EntityFrameworkCore;
using MoviesServer.Models;

namespace MoviesServer.DataAccess
{
    public class MoviesContext : DbContext
    {
        public DbSet<Movie> Movies { get; set; }

        public MoviesContext(DbContextOptions<MoviesContext> options)
            : base(options)
        {
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseSqlServer("workstation id=MoviesDB.mssql.somee.com;packet size=4096;user id=BennyM_SQLLogin_1;pwd=zistjlahtw;data source=MoviesDB.mssql.somee.com;persist security info=False;initial catalog=MoviesDB;TrustServerCertificate=True");
            }
        }

    }
}
