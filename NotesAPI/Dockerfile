FROM python:3.10 as base

WORKDIR /
COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

FROM base as notes-api
WORKDIR src/
# env
COPY .env .env
COPY secrets.env secrets.env
# app
COPY app app
# migrations (for now, we run them only manualy)
COPY alembic alembic
COPY alembic.ini alembic.ini
# run app
EXPOSE 8012
CMD ["uvicorn", "app.main:app", "--reload", "--host=0.0.0.0", "--port=8012"]