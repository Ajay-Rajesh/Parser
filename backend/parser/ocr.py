from PIL import Image
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor


detector = DetectionPredictor(device="cpu")
recognizer = RecognitionPredictor(device="cpu")


def ocr_image(img: Image.Image):
    results = recognizer(
        [img],
        [["ta", "en"]], 
        det_predictor=detector
    )

    page = results[0]

    lines = []

    for line in page.text_lines:
        lines.append(line.text)

    return "\n".join(lines)