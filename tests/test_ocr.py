import os

from PIL import Image

from app.model.ocr import run_ocr


def test_run_ocr():
    ## Dummy input
    img = Image.new("RGB", (100, 100), color=(255, 255, 255))
    result = run_ocr(img)

    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], str)
