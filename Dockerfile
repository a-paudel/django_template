FROM oven/bun as assets
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install
COPY . .
RUN bun run build




FROM python:3.12-alpine as final
WORKDIR /app

RUN pip install pdm

COPY pdm.lock pyproject.toml ./
RUN pdm install --no-self --prod

COPY . .
COPY --from=assets /app/public /app/public

CMD pdm run gunicorn config.wsgi:application