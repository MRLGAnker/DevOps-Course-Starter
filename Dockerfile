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
ENTRYPOINT ["poetry","run","gunicorn","--daemon","-b","0.0.0.0","todo_app.wsgi:wsgi_app","--log-file","logs.log"]

FROM base as development
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]