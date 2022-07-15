FROM python:3.9

WORKDIR /bot

COPY requirements.txt requirements.txt

COPY Makefile Makefile

RUN make install

COPY . .

CMD [ "make", "run"]
