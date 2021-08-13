using System;
using Microsoft.AspNetCore.Mvc;

namespace C__api_server
{
    public class ErrorHelper : ControllerBase
    {
        public ActionResult GenerateError(string error_message)
        {
            return BadRequest(new {error=error_message});
        }
    }
}