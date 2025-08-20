# OpenAI Vision API 및 Image API 사용 가이드

이 가이드는 OpenAI의 Vision API와 Image API를 활용한 Document Analysis API의 사용법을 설명합니다.

## 🆕 새로운 기능: 향상된 표 추출

### ✨ 주요 개선사항
- **PNG 이미지 직접 지원**: Vision API를 통한 이미지 표 추출
- **모델 선택 가능**: 사용자가 원하는 OpenAI 모델 선택
- **자동 모델 검증**: Vision API 지원 여부 자동 확인
- **다양한 파일 형식**: PDF, DOCX, Excel, 모든 이미지 형식 지원

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# OpenAI API 키 설정
export OPENAI_API_KEY="your-openai-api-key-here"

# 의존성 설치
pip install -r requirements.txt
```

### 2. API 서버 실행
```bash
python main.py
```

### 3. 테스트용 샘플 파일 생성
```bash
python create_sample_pdf.py
```

### 4. API 테스트
```bash
# PDF 분석 테스트
python test_pdf_api.py

# 이미지 분석 및 생성 테스트
python test_image_api.py

# 표 추출 API 테스트 (새로운 기능)
python test_extract_tables_api.py
```

## 📚 API 사용법

### 🖼️ 이미지 분석 (Vision API)

#### 방법 1: 이미지 직접 분석
```python
import requests

def analyze_image_direct(image_path, prompt="이 이미지를 분석하고 주요 내용을 설명해주세요.", detail="auto"):
    with open(image_path, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}
        data = {"prompt": prompt, "detail": detail}
        
        response = requests.post(
            "http://localhost:8000/analyze-image",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("분석 결과:", result["output_text"])
            print("사용된 모델:", result["model"])
            if result["usage"]:
                print("토큰 사용량:", result["usage"])
        else:
            print("오류:", response.text)

# 사용 예시
analyze_image_direct("sample_image.jpg", "이 이미지에서 표를 찾아주세요.", "high")
```

### 📊 표 추출 (새로운 기능)

#### 기본 사용법
```python
import requests

def extract_tables(file_path, model=None):
    """
    파일에서 표를 추출합니다.
    
    Args:
        file_path: 분석할 파일 경로
        model: 사용할 모델명 (선택사항)
    """
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/octet-stream")}
        data = {}
        
        if model:
            data["model"] = model
        
        response = requests.post(
            "http://localhost:8000/extract-tables",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"표 추출 성공! {result['table_count']}개의 표 발견")
            print(f"사용 모델: {result['extraction_method']}")
            
            # 표 데이터 출력
            for i, table in enumerate(result['tables']):
                print(f"\n표 {i+1}: {table.get('title', '제목 없음')}")
                print(f"행: {table.get('row_count', 0)}, 열: {table.get('column_count', 0)}")
            
            # Markdown 형식 출력
            print(f"\nMarkdown 형식:\n{result['markdown']}")
            
            return result
        else:
            print("표 추출 실패:", response.text)
            return None

# 사용 예시
# 기본 모델 사용
extract_tables("document.pdf")

# 특정 모델 지정
extract_tables("document.pdf", model="gpt-4o-mini")

# PNG 이미지에서 표 추출
extract_tables("table.png", model="gpt-4o")
```

#### 모델 선택 가이드
```python
# Vision API 지원 모델 (이미지 처리에 권장)
vision_models = [
    "gpt-4o",           # 기본 모델, 고품질
    "gpt-4o-mini",      # 빠른 처리, 비용 효율적
    "gpt-4-vision-preview"  # 최고 품질
]

# 일반 텍스트 처리 모델
text_models = [
    "gpt-4o",
    "gpt-4o-mini", 
    "gpt-3.5-turbo"
]

# 자동 모델 선택 (API가 자동으로 적절한 모델 선택)
def extract_tables_auto(file_path):
    return extract_tables(file_path)  # model 파라미터 생략
```
```

#### 방법 2: 파일 업로드 후 분석
```python
def upload_and_analyze_image(image_path, prompt="이 이미지를 분석해주세요."):
    # 1단계: 이미지 업로드
    with open(image_path, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}
        
        response = requests.post(
            "http://localhost:8000/upload-file",
            files=files
        )
        
        if response.status_code == 200:
            result = response.json()
            file_id = result["file_id"]
            print("파일 업로드 성공! ID:", file_id)
            
            # 2단계: 파일 ID로 분석
            analysis_data = {"file_id": file_id, "prompt": prompt}
            
            analysis_response = requests.post(
                "http://localhost:8000/analyze-image-with-file-id",
                data=analysis_data
            )
            
            if analysis_response.status_code == 200:
                analysis_result = analysis_response.json()
                print("분석 결과:", analysis_result["output_text"])
                return analysis_result
            else:
                print("분석 실패:", analysis_response.text)
                return None
        else:
            print("업로드 실패:", response.text)
            return None

# 사용 예시
upload_and_analyze_image("sample_image.jpg", "이 이미지의 주요 특징을 설명해주세요.")
```

#### cURL 명령어
```bash
# 이미지 직접 분석
curl -X POST "http://localhost:8000/analyze-image" \
  -F "file=@sample_image.jpg" \
  -F "prompt=이 이미지를 분석해주세요." \
  -F "detail=high"

# 이미지 업로드
curl -X POST "http://localhost:8000/upload-file" \
  -F "file=@sample_image.jpg"

# 파일 ID로 분석
curl -X POST "http://localhost:8000/analyze-image-with-file-id" \
  -d "file_id=file-abc123" \
  -d "prompt=이 이미지를 분석해주세요." \
  -d "detail=high"
```

### 🎨 이미지 생성 (Image API)

#### Python 클라이언트
```python
def generate_image(prompt, size="1024x1024", quality="standard"):
    data = {
        "prompt": prompt,
        "size": size,
        "quality": quality
    }
    
    response = requests.post(
        "http://localhost:8000/generate-image",
        data=data
    )
    
    if response.status_code == 200:
        result = response.json()
        print("이미지 생성 성공!")
        print("이미지 URL:", result["image_url"])
        print("수정된 프롬프트:", result["revised_prompt"])
        return result
    else:
        print("이미지 생성 실패:", response.text)
        return None

# 사용 예시
generate_image(
    "회사 로고 디자인, 미니멀하고 현대적인 스타일, 파란색과 흰색 사용",
    size="1024x1024",
    quality="hd"
)
```

#### cURL 명령어
```bash
curl -X POST "http://localhost:8000/generate-image" \
  -d "prompt=회사 로고 디자인, 미니멀하고 현대적인 스타일" \
  -d "size=1024x1024" \
  -d "quality=hd"
```

## 🔍 프롬프트 예시

### 이미지 분석 프롬프트

#### 기본 분석
```
이 이미지를 분석하고 주요 내용을 설명해주세요.
```

#### 표 추출
```
이 이미지에서 모든 표를 찾아서 내용을 정리해주세요.
각 표의 제목, 헤더, 데이터를 구조화해서 보여주세요.
```

#### 특정 정보 추출
```
이 이미지에서 다음 정보를 추출해주세요:
1. 텍스트 내용
2. 숫자 데이터
3. 차트나 그래프 정보
4. 주요 시각적 요소
```

#### 비교 분석
```
이 이미지의 여러 요소들을 비교 분석하여 다음을 알려주세요:
1. 가장 눈에 띄는 요소
2. 색상과 구성의 특징
3. 전체적인 메시지나 의도
```

### 이미지 생성 프롬프트

#### 로고 디자인
```
회사 로고 디자인, [회사명]을 위한 미니멀하고 현대적인 로고, 
[색상]과 [스타일] 사용, [업종]에 적합한 디자인
```

#### 일러스트레이션
```
[주제]에 대한 아름다운 일러스트레이션, 
[스타일] 아트 스타일, [색상] 톤, 
[분위기]한 느낌, 고해상도
```

#### 아이콘 세트
```
[용도]를 위한 아이콘 세트, 
미니멀하고 현대적인 디자인, 
[색상] 사용, 일관된 스타일
```

## 📊 응답 형식

### 이미지 분석 응답
```json
{
  "success": true,
  "output_text": "이미지 분석 결과...",
  "model": "gpt-4.1-mini",
  "usage": {
    "input_tokens": 1500,
    "output_tokens": 800
  }
}
```

### 이미지 생성 응답
```json
{
  "success": true,
  "image_url": "https://oaidalleapiprodscus.blob.core.windows.net/...",
  "revised_prompt": "수정된 프롬프트...",
  "model": "gpt-image-1"
}
```

## ⚠️ 주의사항

### 파일 크기 제한
- **이미지 파일**: 최대 50MB
- **PDF 파일**: 최대 10MB
- **총 용량**: API 요청당 최대 50MB

### 지원 파일 형식
- **이미지**: PNG, JPEG, TIFF, BMP, WebP, GIF (비애니메이션)
- **PDF**: PDF

### 토큰 사용량
이미지 입력 시 OpenAI는 다음을 모델 컨텍스트에 포함합니다:
- 이미지 데이터 (detail 레벨에 따라 토큰 수 달라짐)
- 텍스트 프롬프트

### detail 파라미터
- **low**: 85 토큰 (512x512 해상도, 빠른 처리)
- **high**: 85 + (타일당 170 토큰) (고해상도, 정확한 분석)
- **auto**: 모델이 자동으로 결정

## 🧪 테스트 시나리오

### 1. 이미지 분석 테스트
```bash
# 1. 샘플 이미지 준비
# 2. 이미지 직접 분석
python test_image_api.py

# 3. 다양한 프롬프트로 테스트
prompts = [
    "이 이미지를 간단히 설명해주세요.",
    "이미지에서 텍스트를 추출해주세요.",
    "이미지의 색상과 구성을 분석해주세요.",
    "이미지에서 표나 차트를 찾아주세요."
]
```

### 2. 이미지 생성 테스트
```bash
# 1. 다양한 프롬프트로 이미지 생성
generate_image("미니멀한 회사 로고, 파란색과 흰색", "1024x1024", "standard")
generate_image("자연스러운 풍경화, 수채화 스타일", "1792x1024", "hd")

# 2. 품질 비교
generate_image("고양이 일러스트", "1024x1024", "standard")
generate_image("고양이 일러스트", "1024x1024", "hd")
```

### 3. 파일 업로드 워크플로우 테스트
```python
# 1. 이미지 업로드
file_id = upload_image("sample_image.jpg")

# 2. 파일 ID로 분석
result = analyze_image_with_file_id(file_id, "이 이미지를 분석해주세요.")

# 3. 결과 확인
print("분석 완료:", result["output_text"])
```

## 🔧 문제 해결

### 일반적인 오류

#### 1. OpenAI API 오류
```
OpenAI Vision API 이미지 분석 오류: Invalid API key
```
**해결방법**: `OPENAI_API_KEY` 환경 변수를 확인하고 올바른 API 키를 설정하세요.

#### 2. 파일 크기 오류
```
파일 크기는 50MB를 초과할 수 없습니다.
```
**해결방법**: 더 작은 파일을 사용하거나 이미지를 압축하세요.

#### 3. 파일 형식 오류
```
지원되지 않는 이미지 형식입니다.
```
**해결방법**: 지원되는 이미지 형식인지 확인하세요.

#### 4. 모델 지원 오류
```
OpenAI Vision API 이미지 분석 오류: The model 'gpt-4.1-mini' does not support image inputs
```
**해결방법**: GPT-4.1-mini 모델에 대한 접근 권한이 있는지 확인하세요.

### 디버깅 팁

1. **로그 확인**: API 서버의 콘솔 출력을 확인하세요
2. **파일 검증**: 업로드하려는 파일이 올바른 형식인지 확인하세요
3. **API 키 확인**: OpenAI API 키가 유효한지 확인하세요
4. **네트워크 연결**: 인터넷 연결 상태를 확인하세요

## 📈 성능 최적화

### 1. detail 파라미터 최적화
- **빠른 분석**: `detail="low"` 사용 (85 토큰)
- **정확한 분석**: `detail="high"` 사용 (고해상도)
- **자동 최적화**: `detail="auto"` 사용 (모델이 결정)

### 2. 이미지 크기 최적화
- **필요한 해상도만**: 분석 목적에 맞는 이미지 크기 사용
- **압축 활용**: JPEG 압축으로 파일 크기 줄이기
- **불필요한 메타데이터 제거**: EXIF 데이터 정리

### 3. 배치 처리
- **여러 이미지**: 순차적으로 처리하여 API 제한 고려
- **적절한 간격**: 요청 간격을 두어 안정성 확보

## 🌟 고급 사용법

### 1. 커스텀 이미지 분석 파이프라인
```python
def custom_image_analysis_pipeline(image_path):
    # 1단계: 기본 분석
    basic_result = analyze_image_direct(image_path, "이미지의 주요 내용을 파악해주세요.")
    
    # 2단계: 텍스트 추출
    text_result = analyze_image_direct(image_path, "이미지에서 모든 텍스트를 추출해주세요.")
    
    # 3단계: 구조 분석
    structure_result = analyze_image_direct(image_path, "이미지의 구조와 레이아웃을 분석해주세요.")
    
    return {
        "basic": basic_result,
        "text": text_result,
        "structure": structure_result
    }
```

### 2. 이미지 생성 워크플로우
```python
def image_generation_workflow(prompt, variations=3):
    results = []
    
    for i in range(variations):
        # 다양한 크기와 품질로 이미지 생성
        result = generate_image(
            f"{prompt} - 변형 {i+1}",
            size="1024x1024",
            quality="standard"
        )
        results.append(result)
    
    return results
```

### 3. 결과 저장 및 관리
```python
import json
from datetime import datetime

def save_analysis_result(result, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_analysis_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"분석 결과가 저장되었습니다: {filename}")
    return filename

# 사용 예시
result = analyze_image_direct("sample_image.jpg")
save_analysis_result(result)
```

## 🎯 지원 모델

### Vision API 지원 모델
- **GPT-4.1-mini**: 이미지 분석 지원 ✅
- **GPT-4.1-nano**: 이미지 분석 지원 ✅
- **GPT-4o**: 이미지 분석 지원 ✅
- **GPT-4o-mini**: 이미지 분석 지원 ✅

### Image API 지원 모델
- **GPT Image 1**: 이미지 생성 지원 ✅
- **DALL-E 3**: 이미지 생성 지원 ✅
- **DALL-E 2**: 이미지 생성 지원 ✅

이 가이드를 통해 OpenAI의 Vision API와 Image API를 효과적으로 활용할 수 있습니다! 🎯
