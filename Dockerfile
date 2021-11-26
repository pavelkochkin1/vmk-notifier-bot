FROM python:3.8-slim-buster

RUN mkdir /app

COPY . /app/
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]