from fastapi import FastAPI
from fastapi import Response, status

app = FastAPI(
    debug=True
)


@app.get("/")
def home():
    return Response(status_code=status.HTTP_200_OK)
