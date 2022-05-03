FROM python:3.9

COPY . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]