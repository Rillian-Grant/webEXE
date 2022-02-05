FROM golang:1.17-alpine

ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN pip3 install --no-cache honcho
RUN pip3 install --no-cache gunicorn

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5200

CMD honcho start
