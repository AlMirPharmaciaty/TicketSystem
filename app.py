"""
Starting point of the application
"""
from fastapi import Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req, e: RequestValidationError):
    """
    Handling pydantic data validation errors
    """
    error = f'{e.errors()[0]["loc"][1]} - {e.errors()[0]["msg"]}'
    response = APIResponse(status="error", message=str(error))
    return JSONResponse(response.model_dump())