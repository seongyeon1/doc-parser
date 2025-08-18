from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import os
import json
from typing import List, Dict, Any, Optional
import openai
from dotenv import load_dotenv
from table_extractor import TableExtractor
from file_processor import FileProcessor

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

app = FastAPI(
    title="Document Analysis API",
    description="GPT-4o 및 Vision API를 사용하여 PDF, 이미지 등 다양한 문서를 분석하고 표를 추출하는 API",
    version="2.1.0"
)

# 파일 처리기 및 표 추출기 초기화
file_processor = FileProcessor()
table_extractor = TableExtractor()

@app.get("/")
async def root():
    return {"message": "Document Analysis API is running", "version": "2.1.0"}

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
async def extract_tables(file: UploadFile = File(...)):
    """
    첨부파일에서 표를 추출하여 JSON과 Markdown으로 정리합니다.
    
    Args:
        file: 업로드된 파일 (PDF, DOCX, XLSX, 이미지 등)
    
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
        
        # 이미지 파일인 경우 Vision API를 직접 사용
        if file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.gif']:
            result = await table_extractor.extract_tables_from_image(file_content, file_extension)
        else:
            # 다른 파일 형식의 경우 텍스트 추출 후 표 분석
            extracted_text = await file_processor.process_file(file_content, file_extension)
            
            if not extracted_text:
                raise HTTPException(status_code=400, detail="파일에서 텍스트를 추출할 수 없습니다.")
            
            # GPT-4o를 사용하여 표 추출 및 정리
            result = await table_extractor.extract_tables_with_gpt5(extracted_text)
        
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"표 추출 중 오류가 발생했습니다: {str(e)}")

@app.get("/health")
async def health_check():
    """API 상태 확인"""
    return {"status": "healthy", "model": OPENAI_MODEL}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
