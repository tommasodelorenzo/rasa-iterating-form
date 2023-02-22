FROM rasa/rasa-sdk:3.3.0

USER root

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup --gid 1000 myuser
RUN adduser --uid 1000 --gid 1000 --disabled-password --gecos "" myuser

USER myuser