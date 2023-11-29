FROM python:3.12.0-alpine3.18
WORKDIR /app
COPY main.py ./
COPY tests ./tests
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD pytest tests

