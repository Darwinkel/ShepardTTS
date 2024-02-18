FROM python:3.11-bookworm

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./app.py" ]
