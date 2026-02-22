FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache

COPY . .

EXPOSE 8000

CMD sh -c "uvicorn blogweb.asgi:application --host 0.0.0.0 --port 8000"