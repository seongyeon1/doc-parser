from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import json
from typing import List, Dict, Any
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
    title="Table Extraction API",
    description="GPT-4o Vision을 사용하여 첨부파일에서 표를 추출하고 JSON과 Markdown으로 정리하는 API",
    version="1.0.0"
)

# 파일 처리기 및 표 추출기 초기화
file_processor = FileProcessor()
table_extractor = TableExtractor()

@app.get("/")
async def root():
    return {"message": "Table Extraction API is running"}

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
