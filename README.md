# Blog App - FastAPI

### How to run the application locally

- Step 1: Download and install [PostgreSQL](https://www.postgresql.org/download/)
  - replace the password with your own in the `database.py` file located inside src/utils

- Step 2: Install and activate virtual environment
  - Inside the app where app.py is located
```
python -m venv venv
```
```
venv\scripts\activate
```

- Step 3: Install requirements
```
pip install -r requirements.txt
```

- Step 4: Start the app and go to http://127.0.0.1:8000
  - Confirm the port number from your terminal
```
uvicorn app:app
```