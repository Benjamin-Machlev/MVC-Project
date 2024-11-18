using Microsoft.EntityFrameworkCore;

using System.Collections.Generic;
using System.Reflection.Emit;

namespace MoviesServer.Models
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
                optionsBuilder.UseSqlServer("your-connection-string-here");
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Movie>().ToTable("Movies");
            modelBuilder.Entity<Movie>().HasKey(m => m.MovieID);
            modelBuilder.Entity<Movie>().Property(m => m.Title).IsRequired();
        }
    }
}
