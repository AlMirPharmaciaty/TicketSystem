from fastapi.responses import HTMLResponse
from src import my_app

app = my_app()


@app.get("/", response_class=HTMLResponse)
def home():
    content = """
    <h1>TicketSystem - API</h1>
    <ul>
    <li><h3><a href="/docs">API Documentation</a></h3></li>
    </ul>
    """
    return content