## Resume AI 코치

CV 이미지 기반 OCR -> LLM 질의응답 서비스

---

## 🧭 목차

- [📌 Features](#-features)
- [📂 폴더 구조](#-폴더-구조)
- [🚀 사용 방법](#-사용-방법)
- [🔄 CI/CD (자동 테스트 및 배포)](#-cicd-자동-테스트-및-배포)
- [🎯 향후 계획 (TODO)](#-향후-계획-todo)

---

## 📌 Features

    •	OCR -> text + prompt -> LLM 추론 파이프라인
    •	REST API 구성 (FastAPI)
    •	Docker-compose 배포, Github Actions CI/CD 구성

---

## 📂 폴더 구조

```plaintext
Resume_AI_coach/
├── modeling/              # 각 모델 실험 및 테스트
├── app/
│   ├── model/             # 각 모델(OCR, LLM) 추론 코드
│   ├── utils/
│   ├── main.py            # FastAPI router
│   ├── api.py             # FastAPI endpoint
│   └── pipeline.py        # OCR->LLM 추론 파이프라인
│
├── tests/                 # pytest 테스트 파일
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt   # 테스트 환경용 dependency list
├── Makefile               # 로컬 테스트 및 lint, reformat 자동화
├── .github/
│   └── workflows/
│       ├── ci.yml         # Lint/Test 자동화
│       └── cd.yml         # 배포 자동화
```

---

## 🚀 사용 방법

1. 서버 실행 (FastAPI server + 모델링용 container)

```bash
docker-compose up --build
```

2. 서버 체크

```bash
curl http://localhost:8000/health
# response: {"status": "ok"}
```

3. 이력서 분석 API 호출

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "image": "<base64_encoded_image>",
    "question": "ML 관련 프로젝트들의 기술 스택 요약해줘."
}'
```

Response 예시:

```json
{
  "answer": "PyTorch, Tensorflow 등이 있습니다."
}
```

---

## 🔄 CI/CD (자동 테스트 및 배포)

### ✅ CI: 자동 린트 및 테스트 (`ci.yml`)

- main 브랜치로의 push 시 실행
- 수행 작업:
  1. 코드 checkout
  2. Python 3.10 환경 세팅
  3. 의존성 설치 (`requirements.txt`, `requirements-dev.txt`)
  4. 린트 검사 (`black`, `isort`, `flake8`)
  5. 테스트 실행 (`pytest`)

### 🛠 로컬 테스트 (Makefile 지원)

- 린트 전체 실행: `make lint`
- 코드 포맷팅 자동 수정: `make format`
- 유닛 테스트 실행: `make test`

### 🚀 CD: GPU 서버 자동 배포 (`cd.yml`)

- main 브랜치로의 push 시 실행:
  1. SSH를 통해 원격 GPU 서버 접속
  2. 최신 코드 pull
  3. 기존 컨테이너 종료 및 재빌드 후 실행

---

## 🎯 향후 계획 (TODO)

• 모델 Registry, 컨테이너 Registry 연동  
• UI 제작

---

### 사용 기술 스택

• EasyOCR, Phi-2, FastAPI, AWS EC2  
• GitHub Actions (CI/CD), Docker
