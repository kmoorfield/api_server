using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;

namespace C__api_server.Controllers
{
    [Produces("application/json")]
    [ApiController]
    [Route("[controller]")]
    public class DogFactsController : ControllerBase
    {
        private DogFactsContext _dogFactsContext;

        private readonly ILogger<DogFactsController> _logger;

        private ErrorHelper _errorHelper;

        private readonly IUriService uriService;

        public DogFactsController(ILogger<DogFactsController> logger, DogFactsContext DogFactsContext, ErrorHelper errorHelper, IUriService uriService)
        {
            _logger = logger;
            _dogFactsContext = DogFactsContext;
            _errorHelper = errorHelper;
            this.uriService = uriService;
        }

        /// <summary>
        /// Returns the first record in the database
        /// </summary>
        /// <response code="200">Returns a Dog object</response>
        [HttpGet("/first")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public ActionResult<Dog> GetFirstRecord()
        {
            var result = _dogFactsContext.Dogs.OrderBy(x => x.Id).FirstOrDefault();
            return Ok(result);    
        }

        /// <summary>
        /// Returns the last record in the database
        /// </summary>
        /// <response code="200">Returns a Dog object</response>
        [HttpGet("/last")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public ActionResult<Dog> GetLastRecord()
        {
            var result = _dogFactsContext.Dogs.OrderByDescending(x => x.Id).FirstOrDefault();
            return Ok(result);    
        }

        /// <summary>
        /// Returns a random record in the database
        /// </summary>
        /// <response code="200">Returns a Dog object</response>
        [HttpGet("/random")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public ActionResult<Dog> GetRandomRecord()
        {
            int random_number = new Random().Next(1, _dogFactsContext.Dogs.Count());

            while(true)
            {
                var result = _dogFactsContext.Dogs.Skip(random_number).FirstOrDefault();

                if(result is null)
                {
                    continue;
                }

                return Ok(result);
            }
        }

        /// <summary>
        /// Returns all records in the database
        /// </summary>
        /// <response code="200">Returns a Dog object</response>
        [HttpGet("/all")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public ActionResult<Dog> GetAllRecords([FromQuery] PaginationFilter filter)
        {
            var route = Request.Path.Value;
            var validFilter = new PaginationFilter(filter.PageNumber, filter.PageSize);
            var paged_result = _dogFactsContext.Dogs.Skip((validFilter.PageNumber - 1) * validFilter.PageSize).Take(validFilter.PageSize).ToList();
            var totalRecords = _dogFactsContext.Dogs.Count();
            var pagedReponse = PaginationHelper.CreatePagedReponse<Dog>(paged_result, validFilter, totalRecords, uriService, route);
            return Ok(pagedReponse);
        }

        /// <summary>
        /// Returns a given record in the database by id
        /// </summary>
        /// <response code="200">Returns a Dog object</response>
        /// <response code="400">Returns a Bad Request object</response>
        /// <response code="404">Returns a Not Found object</response>
        [HttpGet("/record/{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public ActionResult<Dog> GetRecord(int id)
        {
            if (id <= 0)
            {
                return _errorHelper.GenerateError("This is not a valid ID!");
            }

            var result = _dogFactsContext.Dogs.Where(x => x.Id == id).FirstOrDefault();

            if (result is null)
            {
                return NotFound();
            }

            return Ok(result);
        }

        /// <summary>
        /// Adds a new record into the database
        /// </summary>
        /// <response code="201">Returns a Dog object</response>
        /// <response code="400">Returns a Bad Request object</response>
        [HttpPost("/insert")]
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public ActionResult<Dog> PostRecord([FromBody] Dog dog)
        {
           if (dog.Id != 0)
           {
               return _errorHelper.GenerateError("ID should not exist!");
           }
           
            _dogFactsContext.Dogs.Add(dog); 
            _dogFactsContext.SaveChanges();

            return Created("", dog);
        }

        /// <summary>
        /// Updates a record in the database by id
        /// </summary>
        /// <response code="200">Returns a Dog object</response>
        /// <response code="400">Returns a Bad Request object</response>
        /// <response code="404">Returns a Not Found object</response>
        [HttpPut("/update/{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public ActionResult<Dog> UpdateRecord(int id, [FromBody] Dog dog)
        {
            if (id <= 0)
            {
                return _errorHelper.GenerateError("This is not a valid ID!");
            }

            if (dog.Id != id)
            {
                return _errorHelper.GenerateError("Provided ID does not match Body ID!");
            }

            var result = _dogFactsContext.Dogs.Where(x => x.Id == id).FirstOrDefault();

            if (result is null)
            {
                return NotFound();
            }

            result.Fact = dog.Fact;

            // Add catch for if other changes have already been made to the record
            try
            {
                _dogFactsContext.SaveChanges();
            }
            catch(DbUpdateConcurrencyException)
            {
                return Problem("The record you attempted to update was modified by another user before you.");
            }
            catch(Exception ex)
            {
                return Problem($@"Error encountered updating database. This might be transient, so please try again later. {ex.Message}");
            }

            return Ok(result);
        }

        /// <summary>
        /// Deletes a record in the database by id
        /// </summary>
        /// <response code="200">Returns a Dog object</response>
        /// <response code="400">Returns a Bad Request object</response>
        /// <response code="404">Returns a Not Found object</response>
        [HttpDelete("/delete/{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public ActionResult<Dog> DeleteRecord(int id)
        {
            if (id <= 0)
            {
                return _errorHelper.GenerateError("This is not a valid ID!");
            }

            var result = _dogFactsContext.Dogs.Where(x => x.Id == id).FirstOrDefault();

            if (result is null)
            {
                return NotFound();
            }

            _dogFactsContext.Dogs.Remove(result);
            _dogFactsContext.SaveChanges();

            return NoContent();
        }
    }
}
