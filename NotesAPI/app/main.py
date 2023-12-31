from fastapi import FastAPI
from fastapi import Response, status
from . import DEBUG

# import routers
from .routers import account, notes, categories, images

# startup/shutdown events
from .lifespan import lifespan


app = FastAPI(
    debug=DEBUG,
    lifespan=lifespan
)


app.include_router(account.router)
app.include_router(notes.router)
app.include_router(categories.router)
app.include_router(images.router)


@app.get("/")
def home():
    return {
        'message': 'Hello, world!'
    }
