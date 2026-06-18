FROM python:3.13.0

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./compose/app/start_app.sh /start_app.sh
RUN chmod +x /start_app.sh

COPY . /app
