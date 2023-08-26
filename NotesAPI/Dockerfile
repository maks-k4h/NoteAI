FROM python:3.10 as base

WORKDIR /
COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

FROM base as notes-api
COPY app app
WORKDIR /app
EXPOSE 8012
CMD ["python", "-m", "uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=8012"]