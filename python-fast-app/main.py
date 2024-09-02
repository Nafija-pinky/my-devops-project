from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from database import Database
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Instantiate the Database class
db = Database()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
def search_movies(request: Request, year_of_release: int = Form(...)):
    try:
        results = db.search_movies_by_year(year_of_release)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {e}")

    return templates.TemplateResponse("index.html", {"request": request, "results": results})


@app.get("/upload_data")
def upload_data(request: Request):
    return templates.TemplateResponse("upload_data.html", {"request": request})


@app.post("/upload_data")
def upload_movie_data_handler(
    request: Request,
    movie_name: str = Form(...),
    year_of_release: int = Form(...),
    box_office: float = Form(...),
    director: str = Form(...),
    producer: str = Form(...),
    cast: str = Form(...),
):
    try:
        db.upload_movie_data(movie_name, year_of_release, box_office, director, producer, cast)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading data: {e}")

    return templates.TemplateResponse("upload_data.html", {"request": request, "message": "Movie data uploaded successfully!"})

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

