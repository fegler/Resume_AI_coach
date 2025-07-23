# fastapi_server/Dockerfile
## 아직 모델 추론을 FastAPI 내에서 하기때문에, pytorch로 base image
FROM pytorch/pytorch:2.2.2-cuda11.8-cudnn8-runtime

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* 

WORKDIR /sources/app 

COPY requirements.txt /sources/app/

RUN pip install --no-cache-dir -r requirements.txt && pip install "numpy<2"

COPY . /sources/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]