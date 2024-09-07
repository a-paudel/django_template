FROM python:3.12-slim
WORKDIR /app

# system dependencies
RUN pip install uv
COPY --from=oven/bun /usr/local/bin/bun /usr/local/bin/bun
RUN apt update
RUN apt install -y curl

# python dependencies
COPY uv.lock pyproject.toml ./
RUN uv sync


# bun dependencies
COPY package.json bun.lockb ./
RUN bun install


# copy source code
COPY . .

# generate assets
RUN bun run build
RUN uv run python manage.py collectstatic --noinput

CMD uv run gunicorn config.wsgi:application