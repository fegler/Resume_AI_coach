import cv2
import easyocr


def run_ocr(im_path):
    reader = easyocr.Reader(["en"])  # 영어 text reading
    result = reader.readtext(im_path)
    return result


def visualize_ocr(save_path, result, im_path):
    img = cv2.imread(im_path)
    for box, text, conf in result:
        x1, y1 = box[0]
        x2, y2 = box[2]
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color=(0, 0, 255), thickness=2)
        print(text)
    cv2.imwrite(save_path, img)


def get_ocr_text(results):
    ### format -> only text list
    return [t for _, t, _ in results]


if __name__ == "__main__":
    im_path = "/sources/ml_cv_example.jpg"
    ret = run_ocr(im_path)
    visualize_ocr("./easyocr_result.jpg", ret, im_path)
