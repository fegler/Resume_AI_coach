import io

from model.llm import query_llm
from model.ocr import run_ocr
from PIL import Image
from utils.parsing import make_prompt, parse_response


async def run_inference(file, question):
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")

    ocr_texts = run_ocr(image)  # text list
    prompt = make_prompt(ocr_texts, question)
    raw_response = query_llm(prompt)
    return parse_response(raw_response, prompt)


async def warmup_models():
    run_ocr(Image.new("RGB", (100, 100)))
    query_llm("Test prompt")
