from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pipeline import run_inference

router = APIRouter()


@router.post("/analyze")
async def analyze(file: UploadFile = File(...), question: str = Form(...)):
    try:
        result = await run_inference(file, question)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.get("/health")
async def health_check():
    return {"status": "ok"}
