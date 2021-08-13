using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace C__api_server
{
    public class DogFactsContext : DbContext
    {
        public DbSet<Dog> Dogs { get; set; }

        public DogFactsContext(DbContextOptions<DogFactsContext> contextOptions) : base(contextOptions)
        {
                      
        }
    }

    public class Dog
    {
        public int Id { get; set; }

        [Required]
        [DefaultValue("null")]
        public string Fact { get; set; }
    }
}