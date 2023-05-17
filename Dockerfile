FROM python:3.8-bullseye

RUN apt update && apt install -y \
    python-dev \
    libxml2-dev \
    libxslt1-dev \
    antiword \
    unrtf \
    poppler-utils \
    # pstotext \
    tesseract-ocr \
    flac \
    ffmpeg \
    lame \
    libmad0 \libsox-fmt-mp3 \
    sox \
    libjpeg-dev \
    swig \
    libpulse-dev

WORKDIR /home/app

RUN python -m venv venv
RUN . venv/bin/activate
RUN python -m pip install textract
