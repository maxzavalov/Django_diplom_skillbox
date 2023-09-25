FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY diploma-frontend .
COPY diploma-frontend-0.6.tar.gz diploma-frontend-0.6.tar.gz
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN ["python", "setup.py", "sdist"]
RUN pip install diploma-frontend-0.6.tar.gz
RUN pip install -r requirements.txt

COPY megano .

CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]
