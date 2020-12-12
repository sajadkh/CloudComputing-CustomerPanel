FROM python:3.7

ADD . /project

WORKDIR /project

RUN pip install -r requirements.txt
RUN chmod 777 ./start.sh

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait ./wait
RUN chmod +x ./wait

EXPOSE 8002

CMD ["./start.sh"]
