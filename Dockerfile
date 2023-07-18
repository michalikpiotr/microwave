FROM python:3.9-slim
ARG API_VERSION
ARG DEBUG
ARG ENV
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY . ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

CMD ["gunicorn", "app.main:app"]
