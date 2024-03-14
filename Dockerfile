FROM python:3.11.6-slim

RUN useradd -m appuser

WORKDIR /app

# install pdm
RUN pip install pdm
ENV PATH="/app/.local/bin:${PATH}"

# install bun
COPY --from=oven/bun /usr/local/bin/bun /usr/local/bin/bun

# install bun deps
COPY --chown=appuser:appuser package.json bun.lockb ./
RUN bun install

# install python deps
COPY --chown=appuser:appuser pyproject.toml pdm.lock ./
RUN pdm install --global --project .

COPY --chown=appuser:appuser . .

CMD gunicorn config.wsgi:application -w 4 -t 10 --bind 0.0.0.0:$DJANGO_PORT