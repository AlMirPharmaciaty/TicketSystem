from fastapi.responses import HTMLResponse
from src import my_app

app = my_app()


@app.get("/", response_class=HTMLResponse)
def home():
    content = """
    <h1>Ticketing System</h1>
    <ul>
    <li><h2><a href="/docs">API Documentation</a></h2></li>
    </ul>
    """
    return content
