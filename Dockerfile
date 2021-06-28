FROM python:3.9-slim-buster as base

WORKDIR /DevOps-Course-Starter
COPY poetry.lock pyproject.toml ./

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
RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-stable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN poetry install
ENTRYPOINT ["poetry", "run", "pytest"]