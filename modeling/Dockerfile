FROM pytorch/pytorch:2.2.2-cuda11.8-cudnn8-runtime

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* 

WORKDIR /sources/modeling

COPY requirements.txt /sources/modeling/

RUN pip install --upgrade pip && pip install -r requirements.txt && pip install "numpy<2"

COPY . /sources/modeling 

