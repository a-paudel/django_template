FROM python:3.12-slim
WORKDIR /app

# system dependencies
RUN pip install pdm
COPY --from=oven/bun /usr/local/bin/bun /usr/local/bin/bun
RUN apt update
RUN apt install -y curl

# python dependencies
COPY pdm.lock pyproject.toml ./
RUN pdm install --no-self --prod


# bun dependencies
COPY package.json bun.lockb ./
RUN bun install


# copy source code
COPY . .

# generate assets
RUN bun run build
RUN pdm run python manage.py collectstatic --noinput

CMD pdm run gunicorn config.wsgi:application