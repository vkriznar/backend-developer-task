Setup process:
* Create python virtual env `python -m venv .venv`
* Enter virtual env: On windows`.venv\scripts\activate` or Linux `source .venv/bin/activate`
* Install all python dependencies `pip install -r requirements.txt`
* Run Python: FastAPI: `python -m uvicorn app.main:app --reload`
* Go to `localhost:8000/docs`. FastAPI by itself provides "frontend" for testing api's.