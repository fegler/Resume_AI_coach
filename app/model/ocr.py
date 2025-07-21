import os

import numpy as np

_reader = None


class DummyOCR:
    def readtext(self, image_np):
        return [((0, 0), "sample_text", 0.9)]


def load_reader():
    global _reader
    if _reader is not None:
        return _reader

    if os.environ.get("TEST_MODE") == "1":
        _reader = DummyOCR()
    else:
        import easyocr

        _reader = easyocr.Reader(["en"])
    return _reader


def get_ocr_text(results):
    ### format -> only text list
    return [t for _, t, _ in results]


def run_ocr(pil_image):
    reader = load_reader()
    image_np = np.array(pil_image)
    result = reader.readtext(image_np)
    return get_ocr_text(result)
