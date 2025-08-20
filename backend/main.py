from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import shutil
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import openai
from dotenv import load_dotenv
from table_extractor import TableExtractor
from file_processor import FileProcessor
from background_processor import BackgroundProcessor

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

app = FastAPI(
    title="Document Analysis API",
    description="GPT-4o 및 Vision API를 사용하여 PDF, 이미지 등 다양한 문서를 분석하고 표를 추출하는 API. PNG 이미지 직접 지원 및 모델 선택 가능.",
    version="2.2.0"
)

# CORS 미들웨어 추가 - 외부 접근 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 파일 처리기 및 표 추출기 초기화
file_processor = FileProcessor()
table_extractor = TableExtractor()

# 백그라운드 프로세서 초기화
background_processor = None

# 경로 설정 - Docker 환경과 로컬 환경 모두 지원
# 도커 환경에서는 /app을 기준으로, 로컬에서는 상대 경로 사용
if Path("/app").exists():
    # 도커 환경
    BASE_DIR = Path("/app")
    # Docker 볼륨 마운트에 맞춰 경로 설정
    # 호스트의 ./analyze/data -> 컨테이너의 /app/data
    # 호스트의 ./analyze/result -> 컨테이너의 /app/result
    IMAGES_DIR = BASE_DIR / "data"
    RESULTS_DIR = BASE_DIR / "result"
    UPLOADS_DIR = Path("/tmp/uploads")
    print("DEBUG - Docker 환경 감지됨")
    print(f"DEBUG - Docker IMAGES_DIR: {IMAGES_DIR}")
    print(f"DEBUG - Docker RESULTS_DIR: {RESULTS_DIR}")
else:
    # 로컬 환경 - 명시적 경로 설정
    # doc_parser/doc-parser/main.py에서 실행할 때
    # doc_parser/analyze/result 경로를 사용하도록 설정
    SCRIPT_DIR = Path(__file__).parent  # doc-parser
    PROJECT_ROOT = SCRIPT_DIR.parent     # doc_parser (프로젝트 루트)
    
    # analyze 폴더가 어디에 있는지 확인
    analyze_dir = PROJECT_ROOT / "analyze"
    if analyze_dir.exists():
        BASE_DIR = PROJECT_ROOT
        IMAGES_DIR = analyze_dir / "data"
        RESULTS_DIR = analyze_dir / "result"
        UPLOADS_DIR = PROJECT_ROOT / "uploads"
        print("DEBUG - 로컬 환경 감지됨 (analyze 폴더 사용)")
    else:
        # analyze 폴더가 없으면 기본 경로 사용
        BASE_DIR = SCRIPT_DIR
        IMAGES_DIR = BASE_DIR / "analyze" / "data"
        RESULTS_DIR = BASE_DIR / "analyze" / "result"
        UPLOADS_DIR = BASE_DIR / "uploads"
        print("DEBUG - 로컬 환경 감지됨 (기본 경로 사용)")
    
    # 결과 디렉토리가 없으면 생성
    if not RESULTS_DIR.exists():
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"DEBUG - 결과 디렉토리 생성: {RESULTS_DIR}")

# 디버깅을 위한 경로 출력
print(f"DEBUG - BASE_DIR: {BASE_DIR}")
print(f"DEBUG - IMAGES_DIR: {IMAGES_DIR}")
print(f"DEBUG - RESULTS_DIR: {RESULTS_DIR}")
print(f"DEBUG - UPLOADS_DIR: {UPLOADS_DIR}")

# 디렉토리 생성
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# 백그라운드 프로세서 초기화
background_processor = BackgroundProcessor(RESULTS_DIR, max_workers=3)

# Docker 환경에서 /tmp/uploads 경로도 확인
DOCKER_UPLOADS_DIR = Path("/tmp/uploads")
if DOCKER_UPLOADS_DIR.exists():
    UPLOADS_DIR = DOCKER_UPLOADS_DIR

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 백그라운드 프로세서를 시작합니다."""
    await background_processor.start()

@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 백그라운드 프로세서를 중지합니다."""
    await background_processor.stop()

@app.get("/")
async def root():
    return {"message": "Document Analysis API is running", "version": "2.2.0"}

@app.get("/health")
async def health_check():
    """API 서버 상태 확인용 헬스체크 엔드포인트"""
    return {
        "status": "healthy",
        "version": "2.2.0",
        "openai_model": OPENAI_MODEL,
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/paths")
async def get_paths():
    """현재 설정된 경로 정보를 반환합니다."""
    return {
        "base_dir": str(BASE_DIR),
        "images_dir": str(IMAGES_DIR),
        "results_dir": str(RESULTS_DIR),
        "uploads_dir": str(UPLOADS_DIR),
        "docker_uploads_dir": str(DOCKER_UPLOADS_DIR),
        "docker_uploads_exists": DOCKER_UPLOADS_DIR.exists(),
        "images_dir_exists": IMAGES_DIR.exists(),
        "results_dir_exists": RESULTS_DIR.exists(),
        "uploads_dir_exists": UPLOADS_DIR.exists()
    }

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    이미지 파일을 업로드하여 analyze/data 폴더에 저장합니다.
    
    Args:
        file: 업로드된 이미지 파일
    
    Returns:
        업로드 결과 정보
    """
    try:
        # 파일 유효성 검사
        if not file.filename:
            raise HTTPException(status_code=400, detail="파일명이 없습니다.")
        
        # 이미지 파일 형식 확인
        supported_image_formats = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.gif']
        file_extension = os.path.splitext(file.filename.lower())[1]
        
        if file_extension not in supported_image_formats:
            raise HTTPException(
                status_code=400, 
                detail=f"지원되지 않는 이미지 형식입니다. 지원 형식: {', '.join(supported_image_formats)}"
            )
        
        # 파일 크기 확인 (50MB 제한)
        file_content = await file.read()
        if len(file_content) > 50 * 1024 * 1024:  # 50MB
            raise HTTPException(status_code=400, detail="파일 크기는 50MB를 초과할 수 없습니다.")
        
        # 파일명 중복 방지 (타임스탬프 추가)
        import time
        timestamp = int(time.time())
        base_name = os.path.splitext(file.filename)[0]
        new_filename = f"{base_name}_{timestamp}{file_extension}"
        file_path = IMAGES_DIR / new_filename
        
        # 파일 저장
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # 결과 저장 디렉토리에 메타데이터 저장
        result_metadata = {
            "filename": new_filename,
            "original_filename": file.filename,
            "file_size": len(file_content),
            "file_path": str(file_path),
            "upload_time": timestamp,
            "status": "uploaded"
        }
        
        # 결과 파일 저장
        result_file_path = RESULTS_DIR / f"{base_name}_{timestamp}_metadata.json"
        with open(result_file_path, "w", encoding="utf-8") as f:
            json.dump(result_metadata, f, ensure_ascii=False, indent=2)
        
        return JSONResponse(content={
            "success": True,
            "message": "이미지가 성공적으로 업로드되었습니다.",
            "filename": new_filename,
            "original_filename": file.filename,
            "file_size": len(file_content),
            "file_path": str(file_path),
            "result_file": str(result_file_path),
            "upload_time": timestamp
        }, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 업로드 중 오류가 발생했습니다: {str(e)}")

@app.get("/list-images")
async def list_images():
    """
    analyze/data 폴더에 저장된 이미지 파일 목록을 반환합니다.
    
    Returns:
        이미지 파일 목록
    """
    try:
        image_files = []
        supported_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.gif']
        
        for file_path in IMAGES_DIR.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                stat = file_path.stat()
                image_files.append({
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "modified_time": stat.st_mtime,
                    "path": str(file_path)
                })
        
        # 수정 시간 기준으로 정렬 (최신순)
        image_files.sort(key=lambda x: x["modified_time"], reverse=True)
        
        return JSONResponse(content={
            "success": True,
            "total_count": len(image_files),
            "images": image_files
        }, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 목록 조회 중 오류가 발생했습니다: {str(e)}")

@app.delete("/delete-image/{filename}")
async def delete_image(filename: str):
    """
    지정된 이미지 파일을 삭제합니다.
    
    Args:
        filename: 삭제할 이미지 파일명
    
    Returns:
        삭제 결과
    """
    try:
        file_path = IMAGES_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
        
        # 파일 삭제
        file_path.unlink()
        
        return JSONResponse(content={
            "success": True,
            "message": f"이미지 '{filename}'이(가) 성공적으로 삭제되었습니다."
        }, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 삭제 중 오류가 발생했습니다: {str(e)}")

@app.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: Optional[str] = Form("이 이미지를 분석하고 주요 내용을 설명해주세요."),
    detail: Optional[str] = Form("auto")
):
    """
    OpenAI Vision API를 사용하여 이미지를 분석합니다.
    
    Args:
        file: 업로드된 이미지 파일
        prompt: 분석 요청 프롬프트 (선택사항)
        detail: 이미지 분석 상세도 (low, high, auto) (선택사항)
    
    Returns:
        OpenAI Vision API 분석 결과
    """
    try:
        # 파일 유효성 검사
        if not file.filename:
            raise HTTPException(status_code=400, detail="파일명이 없습니다.")
        
        # 이미지 파일 형식 확인
        supported_image_formats = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.gif']
        file_extension = os.path.splitext(file.filename.lower())[1]
        
        if file_extension not in supported_image_formats:
            raise HTTPException(
                status_code=400, 
                detail=f"지원되지 않는 이미지 형식입니다. 지원 형식: {', '.join(supported_image_formats)}"
            )
        
        # 파일 크기 확인 (50MB 제한)
        file_content = await file.read()
        if len(file_content) > 50 * 1024 * 1024:  # 50MB
            raise HTTPException(status_code=400, detail="파일 크기는 50MB를 초과할 수 없습니다.")
        
        # detail 파라미터 검증
        if detail not in ["low", "high", "auto"]:
            detail = "auto"
        
        # OpenAI Vision API 분석 실행
        result = await file_processor.analyze_image_with_vision(file_content, file_extension, prompt, detail)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"이미지 분석 중 오류가 발생했습니다: {result['error']}")
        
        # 분석 결과를 결과 디렉토리에 저장
        timestamp = int(time.time())
        result_filename = f"analysis_result_{timestamp}.json"
        result_file_path = RESULTS_DIR / result_filename
        
        # 결과에 메타데이터 추가
        result["metadata"] = {
            "original_filename": file.filename,
            "analysis_time": timestamp,
            "prompt": prompt,
            "detail": detail,
            "result_file": str(result_file_path)
        }
        
        # 결과 파일 저장
        with open(result_file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 분석 중 오류가 발생했습니다: {str(e)}")

@app.post("/analyze-image-with-file-id")
async def analyze_image_with_file_id(
    file_id: str = Form(...),
    prompt: Optional[str] = Form("이 이미지를 분석해주세요."),
    detail: Optional[str] = Form("auto")
):
    """
    OpenAI Files API에 업로드된 이미지 파일 ID를 사용하여 분석합니다.
    
    Args:
        file_id: OpenAI Files API의 파일 ID (필수)
        prompt: 분석 요청 프롬프트 (선택사항)
        detail: 이미지 분석 상세도 (low, high, auto) (선택사항)
    
    Returns:
        OpenAI Vision API 분석 결과
    """
    try:
        # detail 파라미터 검증
        if detail not in ["low", "high", "auto"]:
            detail = "auto"
        
        # OpenAI Vision API 분석 실행
        result = await file_processor.analyze_image_with_file_id(file_id, prompt, detail)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"이미지 분석 중 오류가 발생했습니다: {result['error']}")
        
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 분석 중 오류가 발생했습니다: {str(e)}")

@app.post("/analyze-pdf")
async def analyze_pdf(
    file: UploadFile = File(...),
    prompt: Optional[str] = Form("이 PDF를 분석하고 주요 내용을 요약해주세요.")
):
    """
    OpenAI의 PDF 입력 기능을 사용하여 PDF를 분석합니다.
    
    Args:
        file: 업로드된 PDF 파일
        prompt: 분석 요청 프롬프트 (선택사항)
    
    Returns:
        OpenAI API 분석 결과
    """
    try:
        # 파일 유효성 검사
        if not file.filename:
            raise HTTPException(status_code=400, detail="파일명이 없습니다.")
        
        # PDF 파일 형식 확인
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="PDF 파일만 지원됩니다.")
        
        # 파일 크기 확인 (10MB 제한)
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="파일 크기는 10MB를 초과할 수 없습니다.")
        
        # OpenAI PDF 분석 실행
        result = await file_processor.process_pdf_with_openai(file_content, file.filename, prompt)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"PDF 분석 중 오류가 발생했습니다: {result['error']}")
        
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 분석 중 오류가 발생했습니다: {str(e)}")

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """
    파일을 OpenAI Files API에 업로드합니다.
    
    Args:
        file: 업로드할 파일
    
    Returns:
        업로드된 파일 정보
    """
    try:
        # 파일 유효성 검사
        if not file.filename:
            raise HTTPException(status_code=400, detail="파일명이 없습니다.")
        
        # 지원되는 파일 형식 확인
        supported_formats = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.gif']
        file_extension = os.path.splitext(file.filename.lower())[1]
        
        if file_extension not in supported_formats:
            raise HTTPException(
                status_code=400, 
                detail=f"지원되지 않는 파일 형식입니다. 지원 형식: {', '.join(supported_formats)}"
            )
        
        # 파일 크기 확인 (50MB 제한)
        file_content = await file.read()
        if len(file_content) > 50 * 1024 * 1024:  # 50MB
            raise HTTPException(status_code=400, detail="파일 크기는 50MB를 초과할 수 없습니다.")
        
        # OpenAI Files API에 업로드
        result = await file_processor.upload_file_to_openai(file_content, file.filename)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"파일 업로드 중 오류가 발생했습니다: {result['error']}")
        
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 중 오류가 발생했습니다: {str(e)}")

@app.post("/analyze-with-file-id")
async def analyze_with_file_id(
    file_id: str = Form(...),
    prompt: Optional[str] = Form("이 파일을 분석해주세요.")
):
    """
    OpenAI Files API에 업로드된 파일 ID를 사용하여 파일을 분석합니다.
    
    Args:
        file_id: OpenAI Files API의 파일 ID
        prompt: 분석 요청 프롬프트 (선택사항)
    
    Returns:
        OpenAI API 분석 결과
    """
    try:
        # OpenAI API 분석 실행
        result = await file_processor.process_pdf_with_file_id(file_id, prompt)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"파일 분석 중 오류가 발생했습니다: {result['error']}")
        
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 분석 중 오류가 발생했습니다: {str(e)}")

@app.post("/extract-tables")
async def extract_tables(
    file: UploadFile = File(...),
    model: Optional[str] = Form(None)
):
    """
    첨부파일에서 표를 추출하여 JSON과 Markdown으로 정리합니다.
    
    Args:
        file: 업로드된 파일 (PDF, DOCX, XLSX, 이미지 등)
        model: 사용할 모델명 (선택사항, 기본값: 환경변수에서 설정된 모델)
    
    Returns:
        JSON 형태의 표 정보와 Markdown
    """
    try:
        # 파일 유효성 검사
        if not file.filename:
            raise HTTPException(status_code=400, detail="파일명이 없습니다.")
        
        # 지원되는 파일 형식 확인
        supported_formats = ['.pdf', '.docx', '.xlsx', '.xls', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.gif']
        file_extension = os.path.splitext(file.filename.lower())[1]
        
        if file_extension not in supported_formats:
            raise HTTPException(
                status_code=400, 
                detail=f"지원되지 않는 파일 형식입니다. 지원 형식: {', '.join(supported_formats)}"
            )
        
        # 파일 내용 읽기
        file_content = await file.read()
        
        # 사용할 모델 결정 (파라미터 > 환경변수 > 기본값)
        selected_model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # 이미지 파일인 경우 Vision API를 직접 사용
        if file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.gif']:
            result = await table_extractor.extract_tables_from_image(file_content, file_extension, selected_model)
        else:
            # 다른 파일 형식의 경우 텍스트 추출 후 표 분석
            extracted_text = await file_processor.process_file(file_content, file_extension)
            
            if not extracted_text:
                raise HTTPException(status_code=400, detail="파일에서 텍스트를 추출할 수 없습니다.")
            
            # 선택된 모델을 사용하여 표 추출 및 정리
            result = await table_extractor.extract_tables_with_gpt5(extracted_text, selected_model)
        
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"표 추출 중 오류가 발생했습니다: {str(e)}")

# ===== 백그라운드 처리 API 엔드포인트 =====

@app.post("/background/analyze-image")
async def background_analyze_image(
    file: UploadFile = File(...),
    prompt: Optional[str] = Form("이 이미지를 분석하고 주요 내용을 설명해주세요."),
    detail: Optional[str] = Form("auto"),
    callback_url: Optional[str] = Form(None)
):
    """
    이미지 분석을 백그라운드에서 실행합니다.
    
    Args:
        file: 업로드된 이미지 파일
        prompt: 분석 요청 프롬프트 (선택사항)
        detail: 이미지 분석 상세도 (low, high, auto) (선택사항)
        callback_url: 완료 시 호출할 콜백 URL (선택사항)
    
    Returns:
        작업 ID와 상태 정보
    """
    try:
        # 파일 유효성 검사
        if not file.filename:
            raise HTTPException(status_code=400, detail="파일명이 없습니다.")
        
        # 이미지 파일 형식 확인
        supported_image_formats = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.gif']
        file_extension = os.path.splitext(file.filename.lower())[1]
        
        if file_extension not in supported_image_formats:
            raise HTTPException(
                status_code=400, 
                detail=f"지원되지 않는 이미지 형식입니다. 지원 형식: {', '.join(supported_image_formats)}"
            )
        
        # 파일 크기 확인 (50MB 제한)
        file_content = await file.read()
        if len(file_content) > 50 * 1024 * 1024:  # 50MB
            raise HTTPException(status_code=400, detail="파일 크기는 50MB를 초과할 수 없습니다.")
        
        # detail 파라미터 검증
        if detail not in ["low", "high", "auto"]:
            detail = "auto"
        
        # 백그라운드 작업 제출
        task_id = await background_processor.submit_image_analysis_task(
            file_content=file_content,
            filename=file.filename,
            prompt=prompt,
            detail=detail,
            callback_url=callback_url
        )
        
        return JSONResponse(content={
            "success": True,
            "message": "이미지 분석이 백그라운드에서 시작되었습니다.",
            "task_id": task_id,
            "status": "pending",
            "check_status_url": f"/background/task-status/{task_id}"
        }, status_code=202)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"백그라운드 작업 제출 중 오류가 발생했습니다: {str(e)}")

@app.post("/background/extract-tables")
async def background_extract_tables(
    file: UploadFile = File(...),
    model: Optional[str] = Form(None),
    callback_url: Optional[str] = Form(None)
):
    """
    표 추출을 백그라운드에서 실행합니다.
    
    Args:
        file: 업로드된 파일
        model: 사용할 모델명 (선택사항)
        callback_url: 완료 시 호출할 콜백 URL (선택사항)
    
    Returns:
        작업 ID와 상태 정보
    """
    try:
        # 파일 유효성 검사
        if not file.filename:
            raise HTTPException(status_code=400, detail="파일명이 없습니다.")
        
        # 지원되는 파일 형식 확인
        supported_formats = ['.pdf', '.docx', '.xlsx', '.xls', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.gif']
        file_extension = os.path.splitext(file.filename.lower())[1]
        
        if file_extension not in supported_formats:
            raise HTTPException(
                status_code=400, 
                detail=f"지원되지 않는 파일 형식입니다. 지원 형식: {', '.join(supported_formats)}"
            )
        
        # 파일 내용 읽기
        file_content = await file.read()
        
        # 사용할 모델 결정
        selected_model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # 백그라운드 작업 제출
        task_id = await background_processor.submit_table_extraction_task(
            file_content=file_content,
            filename=file.filename,
            model=selected_model,
            callback_url=callback_url
        )
        
        return JSONResponse(content={
            "success": True,
            "message": "표 추출이 백그라운드에서 시작되었습니다.",
            "task_id": task_id,
            "status": "pending",
            "check_status_url": f"/background/task-status/{task_id}"
        }, status_code=202)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"백그라운드 작업 제출 중 오류가 발생했습니다: {str(e)}")

@app.get("/background/task-status/{task_id}")
async def get_background_task_status(task_id: str):
    """
    백그라운드 작업의 상태를 조회합니다.
    
    Args:
        task_id: 작업 ID
    
    Returns:
        작업 상태 정보
    """
    try:
        task_status = await background_processor.get_task_status(task_id)
        
        if not task_status:
            raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")
        
        return JSONResponse(content={
            "success": True,
            "task_status": task_status
        }, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"작업 상태 조회 중 오류가 발생했습니다: {str(e)}")

@app.get("/background/all-tasks")
async def get_all_background_tasks():
    """
    모든 백그라운드 작업 목록을 반환합니다.
    
    Returns:
        모든 작업 목록
    """
    try:
        all_tasks = await background_processor.get_all_tasks()
        
        return JSONResponse(content={
            "success": True,
            "total_count": len(all_tasks),
            "tasks": all_tasks
        }, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"작업 목록 조회 중 오류가 발생했습니다: {str(e)}")

@app.delete("/background/cancel-task/{task_id}")
async def cancel_background_task(task_id: str):
    """
    백그라운드 작업을 취소합니다.
    
    Args:
        task_id: 취소할 작업 ID
    
    Returns:
        취소 결과
    """
    try:
        cancelled = await background_processor.cancel_task(task_id)
        
        if not cancelled:
            raise HTTPException(status_code=400, detail="작업을 취소할 수 없습니다. 이미 완료되었거나 취소된 작업일 수 있습니다.")
        
        return JSONResponse(content={
            "success": True,
            "message": f"작업 '{task_id}'이(가) 성공적으로 취소되었습니다."
        }, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"작업 취소 중 오류가 발생했습니다: {str(e)}")

@app.post("/background/cleanup")
async def cleanup_background_tasks(max_age_hours: int = 24):
    """
    완료된 오래된 백그라운드 작업들을 정리합니다.
    
    Args:
        max_age_hours: 정리할 작업의 최대 나이 (시간 단위, 기본값: 24시간)
    
    Returns:
        정리 결과
    """
    try:
        await background_processor.cleanup_completed_tasks(max_age_hours)
        
        return JSONResponse(content={
            "success": True,
            "message": f"{max_age_hours}시간 이상 된 완료된 작업들이 정리되었습니다."
        }, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"작업 정리 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
