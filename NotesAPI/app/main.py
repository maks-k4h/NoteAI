from fastapi import FastAPI
from fastapi import Response, status
from . import DEBUG

# import routers
from .routers import account, notes, categories

# startup/shutdown events
from .lifespan import lifespan


app = FastAPI(
    debug=DEBUG,
    lifespan=lifespan
)


app.include_router(account.router)
app.include_router(notes.router)
app.include_router(categories.router)


@app.get("/")
def home():
    return Response(status_code=status.HTTP_200_OK)
