from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import tempfile
import uvicorn
from typing import Optional
from .diff_logic import compare_docs

# 앱 초기화
app = FastAPI(
    title="DOCX Diff",
    description="Word 문서(.docx) 간의 차이점을 비교하는 도구",
    version="0.1.0"
)

# 디렉토리 설정
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# 정적 파일과 템플릿 디렉토리 생성
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# 템플릿과 정적 파일 설정
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영환경에서는 구체적인 도메인 지정 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 파일 크기 제한 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """메인 페이지를 표시합니다."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "messages": [], "diff_result": None}
    )

@app.post("/", response_class=HTMLResponse)
async def compare_files(
    request: Request,
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    ignore_space: Optional[bool] = Form(False)
):
    """두 DOCX 파일을 비교합니다."""
    messages = []
    
    # 파일 확장자 검사
    if not (file1.filename.endswith('.docx') and file2.filename.endswith('.docx')):
        messages.append('DOCX 파일만 비교할 수 있습니다.')
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "messages": messages, "diff_result": None}
        )

    # 파일 크기 검사
    for upload_file in [file1, file2]:
        content = await upload_file.read()
        if len(content) > MAX_FILE_SIZE:
            messages.append(f'파일 크기는 10MB를 초과할 수 없습니다: {upload_file.filename}')
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "messages": messages, "diff_result": None}
            )
        await upload_file.seek(0)  # 파일 포인터 리셋

    # 임시 파일로 저장 및 비교
    try:
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp1, \
             tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp2:
            
            # 파일 저장
            content1 = await file1.read()
            content2 = await file2.read()
            tmp1.write(content1)
            tmp2.write(content2)
            tmp1.flush()
            tmp2.flush()

            try:
                diff_result = compare_docs(
                    tmp1.name,
                    tmp2.name,
                    context_lines=3,
                    ignore_space=ignore_space,
                    no_color=True
                )
            finally:
                # 임시 파일 삭제
                Path(tmp1.name).unlink(missing_ok=True)
                Path(tmp2.name).unlink(missing_ok=True)

            if not diff_result.strip():
                messages.append('두 문서는 동일합니다.')
                return templates.TemplateResponse(
                    "index.html",
                    {"request": request, "messages": messages, "diff_result": None}
                )

            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "messages": messages,
                    "diff_result": diff_result,
                    "file1_name": file1.filename,
                    "file2_name": file2.filename
                }
            )

    except Exception as e:
        messages.append(f'오류가 발생했습니다: {str(e)}')
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "messages": messages, "diff_result": None}
        )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """전역 예외 처리기"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "messages": [f"오류가 발생했습니다: {str(exc)}"],
            "diff_result": None
        },
        status_code=500
    )

def run_web(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """웹 서버를 실행합니다.
    
    Args:
        host (str): 호스트 주소
        port (int): 포트 번호
        reload (bool): 코드 변경시 자동 재시작 여부
    """
    uvicorn.run(
        "docx_diff.web:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    run_web() 