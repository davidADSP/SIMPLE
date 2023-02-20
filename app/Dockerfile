FROM tensorflow/tensorflow:1.15.5

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get -y install cmake libopenmpi-dev python3-dev zlib1g-dev libgl1-mesa-dev ssh python3-pip htop libpq-dev

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

RUN useradd -ms /bin/bash selfplay
USER selfplay
ENV PATH="/home/selfplay/.local/bin:${PATH}"
WORKDIR /app


COPY --chown=selfplay:selfplay ./app/requirements.txt /app
RUN pip3 install -r /app/requirements.txt

COPY --chown=selfplay:selfplay ./app .

ENV PYTHONIOENCODING=utf-8
ENV LC_ALL=C.UTF-8
ENV export LANG=C.UTF-8

CMD bash
