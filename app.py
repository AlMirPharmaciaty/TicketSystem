"""
Starting point of the application
"""
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from src import my_app
from src.schemas.api_response import APIResponse

app = my_app()


@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Landing page of the application
    """
    return """
    <h1>Ticketing System</h1>
    <ul>
    <li><h2><a href="/docs">API Documentation</a></h2></li>
    </ul>
    """


def error_response(error):
    """Custom error response"""
    response = APIResponse(status="error", message=error)
    return JSONResponse(response.model_dump())


@app.exception_handler(Exception)
async def fastapi_exception_handler(_, e: Exception):
    """Handling fastapi errors"""
    return error_response(error=str(e.args[0]))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, e: RequestValidationError):
    """Handling pydantic data validation errors"""
    error = f'{e.errors()[0]["loc"][1]} - {e.errors()[0]["msg"]}'
    return error_response(error=error)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, e: HTTPException):
    """Handling http errors"""
    return error_response(error=e.detail)
