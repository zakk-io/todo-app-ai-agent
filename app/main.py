from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app import models
from app.database import engine
from app.migrate import run_migrations
from app.routes import router

run_migrations()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App")
app.include_router(router)


@app.get("/", response_class=FileResponse)
def root():
    return "static/index.html"


app.mount("/static", StaticFiles(directory="static"), name="static")