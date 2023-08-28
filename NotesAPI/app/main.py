from fastapi import FastAPI
from fastapi import Response, status
from . import DEBUG

# include routers
from .routers import account
from .routers import notes


app = FastAPI(
    debug=DEBUG,
)


app.include_router(account.router)
app.include_router(notes.router)


@app.get("/")
def home():
    return Response(status_code=status.HTTP_200_OK)
