# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /ToDoApi
COPY requirements.txt /ToDoApi/
RUN pip install -r requirements.txt
COPY . /ToDoApi/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]