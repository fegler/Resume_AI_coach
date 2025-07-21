from ocr_test import run_ocr
from PIL import Image
from transformers import LayoutLMv3ForTokenClassification, LayoutLMv3Processor


def normalize_box(box, width, height):
    x0, y0 = box[0]
    x1, y1 = box[2]
    return [
        int(1000 * x0 / width),
        int(1000 * y0 / height),
        int(1000 * x1 / width),
        int(1000 * y1 / height),
    ]


def run_parser(im_path):
    processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=False)
    model = LayoutLMv3ForTokenClassification.from_pretrained("nielsr/layoutlmv3-finetuned-funsd")
    model.eval()

    image = Image.open(im_path).convert("RGB")
    width, height = image.size
    ocr_result = run_ocr(im_path)

    words, boxes = [], []
    for box, text, conf in ocr_result:
        if text.strip():
            words.append(text)
            boxes.append(normalize_box(box, width, height))

    encoding = processor(
        images=image,
        text=words,
        boxes=boxes,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
    )
    outputs = model(**encoding)

    logits = outputs.logits
    predicted_ids = logits.argmax(dim=-1).squeeze().tolist()

    ## mapping
    labels = model.config.id2label
    tokens = processor.tokenizer.convert_ids_to_tokens(encoding["input_ids"].squeeze())
    word_ids = encoding.word_ids()

    from collections import defaultdict

    word_to_labels = defaultdict(list)
    for token, word_id, label_id in zip(tokens, word_ids, predicted_ids):
        if word_id is not None:
            word_to_labels[word_id].append(labels[label_id])

    final_output = {}
    for idx, word in enumerate(words):
        label_list = word_to_labels[idx]
        final_label = label_list[0] if label_list else "0"
        final_output[word] = final_label

    for k, v in final_output.items():
        print(f"{k} -> {v}")


if __name__ == "__main__":
    im_path = "/sources/ml_cv_example.jpg"
    run_parser(im_path)
