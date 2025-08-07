import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import T5Tokenizer, T5EncoderModel
from transformers import AutoProcessor, UdopEncoderModel, UdopForConditionalGeneration

import cv2
from PIL import Image

import easyocr
import numpy as np

processor = AutoProcessor.from_pretrained("microsoft/udop-large", apply_ocr=False)
# model = UdopEncoderModel.from_pretrained("microsoft/udop-large")
model = UdopForConditionalGeneration.from_pretrained("microsoft/udop-large")

image_path = '../tests/assets/ml_cv_example.jpg'
img = Image.open(image_path).convert("RGB")
w, h = img.size 

reader = easyocr.Reader(["en"])  # 영어 text reading
result = reader.readtext(image_path)

text_info, box_info = [], []
for box, text, _ in result:
    x1, y1 = box[0]
    x2, y2 = box[2]
    box_info.append([x1/w, y1/h, x2/w, y2/h])
    text_info.append(text)

# Prompt 준비 (예: QA)
prompt = ['Question: what is the main skill in the document? Answer:']

# processor 인코딩
encoding = processor(
    images=img,
    text=prompt,
    text_pair=[text_info],
    boxes=[box_info],
    return_tensors="pt",
    padding="max_length",
    truncation=True,
)

with torch.no_grad():
    generated_ids = model.generate(**encoding, max_new_tokens=50)

# 결과 디코딩
output = processor.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
print(output)