from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about")
async def about(request: Request):
    timeline = [
        {"year": "2023", "description": "Personal website with FastAPI"},
        {"year": "2022", "description": "Data visualization project"},
        {"year": "2021", "description": "Machine learning research"},
        {"year": "2020", "description": "Mobile app development"}
    ]
    return templates.TemplateResponse("about.html", {"request": request, "timeline": timeline})

@app.get("/projects")
async def projects(request: Request):
    projects = [
        {"name": "Project 1", "description": "This is project 1"},
        {"name": "Project 2", "description": "This is project 2"},
        {"name": "Project 3", "description": "This is project 3"},
    ]
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)