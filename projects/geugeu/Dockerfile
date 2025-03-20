FROM python:3.12-slim

WORKDIR /app

# 시스템 패키지 최소 설치
RUN apt-get update && apt-get install -y curl build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# pyproject.toml, poetry.lock 복사 및 설치
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# 앱 코드 복사
COPY . /app

EXPOSE 8000

CMD ["sh", "./run.sh"]
