FROM python:3.13-slim AS builder

RUN apt-get update \
    && apt-get install -y gcc libpq-dev

COPY requirements.txt .

RUN pip install --prefix=/install -r requirements.txt

FROM python:3.13-slim

WORKDIR /app

RUN useradd --create-home --shell /bin/bash app

COPY --from=builder /install /usr/local

COPY ./compose/app/start_app.sh ./compose/app/start_worker.sh /

RUN chmod +x /start_app.sh
RUN chmod +x /start_worker.sh

COPY --chown=app:app . /app

USER app
