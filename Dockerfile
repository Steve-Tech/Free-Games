FROM stevetech8/dockselpy:latest

RUN apt-get update && apt-get install -y git

WORKDIR /usr/src/app

RUN pip3 install lxml selenium beautifulsoup4

COPY . /usr/src/app

ENV TIMER 70016

#CMD bash -c 'while :; do python3 /usr/src/app/Free_Games.py; sleep $( expr $TIMER + $RANDOM ); done'
CMD bash -c 'while :; do python3 /usr/src/app/Free_Games-Cookies.py; sleep $( expr $TIMER + $RANDOM ); done'
