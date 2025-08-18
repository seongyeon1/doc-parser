# Document Analysis API

OpenAI의 최신 기술을 활용하여 PDF, 이미지 등 다양한 문서를 분석하고 표를 추출하는 API입니다.

## 주요 기능

### 1. OpenAI PDF 입력 기능 (GPT-4o)
- **Base64 인코딩 방식**: PDF를 직접 Base64로 인코딩하여 OpenAI API에 전송
- **파일 업로드 방식**: OpenAI Files API에 파일을 업로드한 후 파일 ID로 분석
- **고급 분석**: 텍스트와 이미지를 모두 활용한 종합적인 문서 분석

### 2. 기존 기능
- **표 추출**: PDF, DOCX, Excel, 이미지에서 표 추출
- **다양한 형식 지원**: PDF, DOCX, XLSX, 이미지 파일 지원
- **Vision API**: OpenAI Vision API를 활용한 이미지 분석

## API 엔드포인트

### PDF 분석 (새로운 기능)

#### `/analyze-pdf` - PDF 직접 분석
```bash
POST /analyze-pdf
Content-Type: multipart/form-data

file: PDF 파일
prompt: 분석 요청 프롬프트 (선택사항)
```

**응답 예시:**
```json
{
  "success": true,
  "output_text": "PDF 분석 결과...",
  "model": "gpt-4o",
  "usage": {
    "input_tokens": 1000,
    "output_tokens": 500
  }
}
```

#### `/upload-file` - 파일 업로드
```bash
POST /upload-file
Content-Type: multipart/form-data

file: 업로드할 파일
```

**응답 예시:**
```json
{
  "success": true,
  "file_id": "file-6F2ksmvXxt4VdoqmHRw6kL",
  "filename": "document.pdf",
  "purpose": "user_data",
  "bytes": 1024000
}
```

#### `/analyze-with-file-id` - 파일 ID로 분석
```bash
POST /analyze-with-file-id
Content-Type: application/x-www-form-urlencoded

file_id: OpenAI 파일 ID
prompt: 분석 요청 프롬프트 (선택사항)
```

### 기존 기능

#### `/extract-tables` - 표 추출
```bash
POST /extract-tables
Content-Type: multipart/form-data

file: 분석할 파일
```

#### `/health` - API 상태 확인
```bash
GET /health
```

## 사용 방법

### 1. 환경 설정
```bash
# 환경 변수 설정
export OPENAI_API_KEY="your-openai-api-key"

# 의존성 설치
pip install -r requirements.txt
```

### 2. API 서버 실행
```bash
python main.py
```

### 3. 테스트
```bash
python test_pdf_api.py
```

## 사용 예시

### Python 클라이언트
```python
import requests

# PDF 직접 분석
with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    data = {"prompt": "이 PDF를 분석하고 주요 내용을 요약해주세요."}
    
    response = requests.post(
        "http://localhost:8000/analyze-pdf",
        files=files,
        data=data
    )
    
    result = response.json()
    print(result["output_text"])
```

### cURL 예시
```bash
# PDF 직접 분석
curl -X POST "http://localhost:8000/analyze-pdf" \
  -F "file=@document.pdf" \
  -F "prompt=이 PDF를 분석하고 주요 내용을 요약해주세요."

# 파일 업로드
curl -X POST "http://localhost:8000/upload-file" \
  -F "file=@document.pdf"

# 파일 ID로 분석
curl -X POST "http://localhost:8000/analyze-with-file-id" \
  -d "file_id=file-6F2ksmvXxt4VdoqmHRw6kL" \
  -d "prompt=이 파일을 분석해주세요."
```

## 제한사항

- **파일 크기**: 개별 파일당 최대 10MB
- **총 용량**: API 요청당 최대 32MB
- **지원 모델**: GPT-4o (PDF 입력 지원)
- **지원 형식**: PDF, PNG, JPG, JPEG, TIFF, BMP, WebP, GIF

## 토큰 사용량

PDF 입력 시 OpenAI는 다음을 모델 컨텍스트에 포함합니다:
- 추출된 텍스트
- 각 페이지의 이미지

이는 토큰 사용량에 영향을 미치므로, 대규모 배포 전에 가격과 토큰 사용량을 고려하세요.

## Docker 실행

```bash
# Docker Compose로 실행
docker-compose up -d

# 또는 Docker 직접 실행
docker build -t doc-parser .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key doc-parser
```

## 라이선스

MIT License
