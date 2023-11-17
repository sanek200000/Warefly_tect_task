FROM python:3.11-alpine

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY ./app /code/app
CMD ["python", "./app/main.py"]