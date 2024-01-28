FROM python:3.11.6-slim

WORKDIR /app
RUN pip install pdm
COPY pyproject.toml pdm.lock ./
RUN pdm install --global --project .

COPY . .
RUN python manage.py collectstatic --noinput
CMD gunicorn config.wsgi:application -w 4 -t 10 --bind 0.0.0.0:$DJANGO_PORT