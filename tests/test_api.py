import io
import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_endpoint():
    root_dir = os.path.dirname(os.path.dirname(__file__))  ## tests 상위 폴더
    test_im_path = os.path.join(root_dir, "tests", "assets", "ml_cv_example.jpg")
    question = "how long this resume is?"

    with open(test_im_path, "rb") as img_file:
        response = client.post(
            "/analyze",
            files={"file": ("sample_resume.jpg", img_file, "image/jpeg")},
            data={"question": question},
        )

    assert response.status_code == 200, f"응답 실패: {response.text}"
    result = response.json()

    assert isinstance(result, dict)
    assert "response" in result
