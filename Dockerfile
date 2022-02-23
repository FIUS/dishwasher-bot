FROM python:3.9

RUN apt-get update && \
    apt-get install -y libolm-dev && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN /root/.poetry/bin/poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml /app/
COPY poetry.lock /app/

RUN /root/.poetry/bin/poetry install

COPY src /app/src

CMD ["python", "-m", "src.main"]
