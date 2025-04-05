FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN uv sync --no-dev

COPY . /app

EXPOSE 8000

CMD ["sh", "./run.sh"]
