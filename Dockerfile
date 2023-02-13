FROM python:3.7-alpine

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

RUN mkdir /app
COPY ./app /app
WORKDIR /app

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
# ENV LISTEN_PORT=443
# EXPOSE 443
CMD [ "python", "./app.py" ]