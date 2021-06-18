FROM python:3.9-slim-buster as base

WORKDIR /DevOps-Course-Starter
COPY poetry.lock pyproject.toml /DevOps-Course-Starter/

RUN apt-get update && pip install --upgrade pip && pip install poetry

RUN poetry config virtualenvs.create false

COPY . /DevOps-Course-Starter/

EXPOSE 5000

FROM base as production
ENV FLASK_ENV=production
RUN poetry install
ENTRYPOINT ["poetry","run","gunicorn","--bind", "0.0.0.0:5000", "todo_app.app:create_app()"]

FROM base as development
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]

FROM base as test
RUN poetry install
ENTRYPOINT ["poetry", "run", "pytest"]