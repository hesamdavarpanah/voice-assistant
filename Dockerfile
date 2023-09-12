FROM python:3.10.12
LABEL authors="hesamdavarpanah"

RUN apt -y update
RUN apt -y upgrade
RUN apt-get clean
RUN apt-get install -y netcat-traditional
RUN apt-get install -y net-tools
RUN apt-get install -y iputils-ping
RUN apt-get install -y zsh
RUN apt-get install -y portaudio19-dev
RUN apt-get install -y ffmpeg

RUN python -m pip install --upgrade pip

WORKDIR /voice_recognition

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /voice_recognition/requirements.txt

COPY . /voice_recognition

RUN chmod +x ./run.sh
RUN chmod -R 777 ./

CMD ["./run.sh"]