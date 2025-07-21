import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# model_id = "mistralai/Mistral-7B-Instruct-v0.2"
# model_id = "openchat/openchat-3.5-1210"
model_id = "microsoft/phi-2"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")


def gen_prompt(text_list):
    ocr_text = "\n".join(text_list)

    prompt = f"""
The following is text extracted from a resume:
{ocr_text}
Please extract key experiences and skill sets, and return the result in the following JSON format.
Please only return the JSON result. Do not include code or markdown formatting.
{{
    "Experience 1": "...",
    "Experience 2": "...",
    "skill set type 1": "...",
    "skill set type 2": "..."
}}
"""
    return prompt


def infer_llm(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs, max_new_tokens=512, do_sample=True, top_k=50, temperature=0.7
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    gen_text = response[len(prompt) :].strip()
    print(gen_text)


if __name__ == "__main__":
    from ocr_test import get_ocr_text, run_ocr

    im_path = "/sources/ml_cv_example.jpg"
    ocr_result = run_ocr(im_path)
    ocr_result = get_ocr_text(ocr_result)
    prompt = gen_prompt(ocr_result)
    infer_llm(prompt)
