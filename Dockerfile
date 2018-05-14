FROM python:3.6-alpine

LABEL maintainer="Ein Verne <git@einverne.info>"
RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt \
    && chmod +x run.sh

EXPOSE 4000
ENTRYPOINT ["./run.sh"]
