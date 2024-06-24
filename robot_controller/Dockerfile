FROM python:3.11-alpine

WORKDIR /app

COPY lib lib/

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY app.py controller.py ./

CMD [ "python3", "app.py"]