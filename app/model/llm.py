import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

_tokenizer = None
_model = None


class DummyModel:
    def generate(self, prompt: str) -> str:
        return f"{prompt} \n answer is `sample name`"


def load_model():
    global _model, _tokenizer
    if _model is not None:
        return _model, _tokenizer

    if os.environ.get("TEST_MODE") == "1":
        _model = DummyModel()
    else:
        # model_id = "mistralai/Mistral-7B-Instruct-v0.2"
        # model_id = "openchat/openchat-3.5-1210"
        model_id = "microsoft/phi-2"

        _tokenizer = AutoTokenizer.from_pretrained(model_id)
        _model = AutoModelForCausalLM.from_pretrained(
            model_id, torch_dtype=torch.float16, device_map="auto"
        )
    return _model, _tokenizer


def query_llm(prompt):
    model, tokenizer = load_model()
    if isinstance(model, DummyModel):
        return model.generate(prompt)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs, max_new_tokens=512, do_sample=True, top_k=50, temperature=0.7
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
