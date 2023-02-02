FROM python:3.8-slim

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt /requirements.txt
COPY ./src /src
COPY ./datasets /datasets
WORKDIR /src
RUN  pip install  -r /requirements.txt
CMD ["python", "webserver.py"]
EXPOSE 8080
