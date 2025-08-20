# Analyze 폴더 데이터 처리 가이드

이 폴더는 PNG 이미지에서 표를 추출하고 결과를 저장하는 기능을 제공합니다.

## 📁 폴더 구조

```
analyze/
├── data/           # 처리할 PNG 이미지 파일들
├── result/         # 처리 결과 JSON 파일들
├── process_analyze_data.py  # 메인 처리 스크립트
├── quick_process.py         # 빠른 처리 스크립트
└── README.md       # 이 파일
```

## 🚀 사용 방법

### 1. API 서버 시작

먼저 doc-parser 폴더에서 API 서버를 시작해야 합니다:

```bash
cd doc-parser
python main.py
```

### 2. 시각화 도구 시작

시각화 도구를 시작하려면:

```bash
cd analyze
python serve_files.py
```

**외부 접근 설정**:
- 시각화 도구는 포트 8080에서 모든 IP에서 접근 가능 (`0.0.0.0:8080`)
- 외부 접근 시: `http://[서버IP]:8080/visualize_results.html`
- 로컬 접근 시: `http://localhost:8080/visualize_results.html`

### 3. 이미지 처리

#### 방법 1: 기본 처리 (권장)
```bash
cd analyze
python process_analyze_data.py
```

#### 방법 2: 빠른 처리
```bash
cd analyze
python quick_process.py
```

#### 방법 3: 특정 모델 지정
```bash
cd analyze
python quick_process.py gpt-4o-mini
```

#### 방법 4: 웹 인터페이스 사용
```bash
cd analyze
python serve_files.py
```
그 후 브라우저에서 `http://[서버IP]:8080/visualize_results.html` 접속

## 📊 처리 결과

### 개별 결과 파일
- `sample1_result.json`: sample1.png 처리 결과
- `sample2_result.json`: sample2.png 처리 결과
- `sample3_result.json`: sample3.png 처리 결과
- ...

### 요약 리포트
- `summary_report.json`: 모든 처리 결과 요약

## ⚙️ 고급 옵션

### 모델 선택
```python
from process_analyze_data import AnalyzeDataProcessor

# 특정 모델 사용
processor = AnalyzeDataProcessor()
results = processor.process_all_images(model="gpt-4o-mini")

# 지연 시간 조정
results = processor.process_all_images(delay=2.0)  # 2초 간격
```

### 개별 이미지 처리
```python
from pathlib import Path

processor = AnalyzeDataProcessor()
image_path = Path("data/sample1.png")
result = processor.process_single_image(image_path, model="gpt-4o")
```

## 🔧 문제 해결

### API 서버 연결 오류
```
❌ API 서버 연결 실패: Connection refused
```
**해결방법**: doc-parser 폴더에서 `python main.py` 실행

### 파일 처리 오류
```
❌ 처리 중 오류 발생: [Errno 2] No such file or directory
```
**해결방법**: analyze 폴더에서 스크립트 실행

### 모델 오류
```
❌ API 오류: 400 - The model 'invalid-model' does not exist
```
**해결방법**: 올바른 모델명 사용 (gpt-4o, gpt-4o-mini 등)

## 📋 지원 모델

### Vision API 지원 모델
- `gpt-4o`: 기본 모델, 고품질
- `gpt-4o-mini`: 빠른 처리, 비용 효율적
- `gpt-4-vision-preview`: 최고 품질

## 📈 성능 팁

1. **빠른 처리**: `quick_process.py` 사용
2. **안정성**: `process_analyze_data.py` 사용 (지연 시간 포함)
3. **비용 절약**: `gpt-4o-mini` 모델 사용
4. **고품질**: `gpt-4o` 모델 사용

## 🎯 사용 예시

### 배치 처리
```bash
# 모든 이미지를 기본 모델로 처리
python process_analyze_data.py

# 빠른 처리 (지연 없음)
python quick_process.py

# 특정 모델로 처리
python quick_process.py gpt-4o-mini
```

### Python에서 직접 사용
```python
from process_analyze_data import AnalyzeDataProcessor

processor = AnalyzeDataProcessor(api_url="http://localhost:8000")
results = processor.process_with_retry()

# 결과 확인
for result in results:
    if result.get("success"):
        print(f"표 개수: {result.get('table_count', 0)}")
```

## 📝 결과 형식

### 표 추출 결과
```json
{
  "success": true,
  "tables": [
    {
      "table_id": "table_1",
      "title": "표 제목",
      "headers": ["열1", "열2", "열3"],
      "rows": [["행1열1", "행1열2", "행1열3"]],
      "row_count": 1,
      "column_count": 3
    }
  ],
  "markdown": "| 열1 | 열2 | 열3 |\n|-----|-----|-----|",
  "summary": "표 설명",
  "table_count": 1,
  "extraction_method": "OpenAI API (gpt-4o)",
  "metadata": {
    "processed_at": "2024-01-01T12:00:00",
    "source_image": "sample1.png",
    "api_url": "http://localhost:8000"
  }
}
```

### 요약 리포트
```json
{
  "summary": {
    "total_images": 5,
    "successful_images": 5,
    "failed_images": 0,
    "total_tables": 5,
    "success_rate": "100.0%"
  },
  "table_details": [...],
  "processed_at": "2024-01-01T12:00:00"
}
```

## 🎉 완료!

이제 analyze 폴더의 PNG 이미지들을 쉽게 처리할 수 있습니다!
