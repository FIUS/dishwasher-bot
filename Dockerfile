FROM python:3.9

RUN apt-get update && \
    apt-get install -y libolm-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.2.2
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml /app/
COPY poetry.lock /app/

RUN poetry install

COPY src /app/src

ENV DISHWASHER_BOT_CRYPTO_STORE_PATH /data/crypto-store
ENV DISHWASHER_BOT_MATRIX_SESSION_FILE /data/session.txt
VOLUME [ "/data" ]

CMD ["python", "-m", "src.main"]
