FROM python:3.11-slim-bookworm

WORKDIR /usr/src/app

RUN adduser shepardtts

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY shepardtts ./shepardtts

USER shepardtts
CMD [ "python", "-m", "shepardtts.app" ]
