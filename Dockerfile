FROM python:3.9-slim

RUN apt-get update && apt-get install -y pkg-config libmariadbclient-dev-compat g++

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python3", "app.py"]