# Table Extraction API

GPT-4o Vision 모델을 사용하여 첨부파일에서 표를 추출하고 JSON과 Markdown으로 정리하는 API입니다.

## 지원 파일 형식

- **PDF** (.pdf)
- **Word 문서** (.docx)
- **Excel 파일** (.xlsx, .xls)
- **이미지 파일** (.png, .jpg, .jpeg, .tiff, .bmp, .webp, .gif)

## 기능

- 다양한 파일 형식에서 텍스트 추출
- **GPT-4o Vision API**를 사용한 지능형 표 인식 및 추출
- 이미지 파일에서 직접 표 구조 분석 (OCR 불필요)
- JSON 형태의 구조화된 표 데이터
- Markdown 형식의 표 정리
- 고해상도 이미지 분석으로 정확한 표 추출
- **Docker 지원**으로 간편한 배포 및 실행

## 🐳 Docker로 실행하기 (권장)

### 1. 사전 요구사항

- Docker Desktop 설치 및 실행
- Docker Compose 지원

### 2. 환경 변수 설정

`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

### 3. 실행 방법

#### Windows
```cmd
docker-run.bat
```

#### Linux/macOS
```bash
chmod +x docker-run.sh
./docker-run.sh
```

#### 수동 실행
```bash
# 이미지 빌드
docker-compose build

# 서비스 실행
docker-compose up -d

# 상태 확인
docker-compose ps
```

### 4. 테스트

#### Windows
```cmd
docker-test.bat
```

#### Linux/macOS
```bash
chmod +x docker-test.sh
./docker-test.sh
```

#### 브라우저 테스트
- API 문서: http://localhost:8000/docs
- 헬스 체크: http://localhost:8000/health

### 5. 서비스 관리

```bash
# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down

# 개발 모드 (핫 리로드)
docker-compose --profile dev up -d
```

## 🔧 로컬 환경에서 실행하기

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

### 3. OpenAI API 키 설정

1. [OpenAI Platform](https://platform.openai.com/)에서 API 키를 발급받으세요
2. `.env` 파일에 API 키를 설정하세요
3. GPT-4o 모델에 대한 접근 권한이 있는지 확인하세요

### 4. API 서버 실행

```bash
python main.py
```

또는

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 테스트

```bash
python test_api.py
```

## 📚 API 사용법

### 1. API 엔드포인트

- **GET /** - API 상태 확인
- **POST /extract-tables** - 파일에서 표 추출
- **GET /health** - API 상태 및 모델 정보

### 2. 표 추출 API 사용 예시

```bash
curl -X POST "http://localhost:8000/extract-tables" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_document.pdf"
```

### 3. 응답 형식

```json
{
  "success": true,
  "tables": [
    {
      "table_id": "table_1",
      "title": "표 제목",
      "headers": ["열1", "열2", "열3"],
      "rows": [
        ["데이터1", "데이터2", "데이터3"],
        ["데이터4", "데이터5", "데이터6"]
      ],
      "row_count": 2,
      "column_count": 3
    }
  ],
  "markdown": "| 열1 | 열2 | 열3 |\n|-----|-----|-----|...",
  "summary": "총 1개의 표가 발견되었습니다.",
  "table_count": 1,
  "extraction_method": "GPT-4o Vision (gpt-4o)"
}
```

## 🏗️ 프로젝트 구조

```
doc_parser/
├── main.py                 # FastAPI 메인 애플리케이션
├── file_processor.py       # 파일 처리 및 텍스트 추출
├── table_extractor.py      # GPT-4o Vision을 사용한 표 추출
├── requirements.txt        # Python 의존성
├── .env                    # 환경 변수 (사용자 생성)
├── env_example.txt         # 환경 변수 예시
├── test_api.py            # API 테스트 스크립트
├── Dockerfile             # Docker 이미지 정의
├── docker-compose.yml     # Docker Compose 설정
├── docker-run.sh          # Linux/macOS 실행 스크립트
├── docker-run.bat         # Windows 실행 스크립트
├── docker-test.sh         # Linux/macOS 테스트 스크립트
├── docker-test.bat        # Windows 테스트 스크립트
├── docker-troubleshoot.sh # Linux/macOS 문제 해결 스크립트
├── docker-troubleshoot.bat # Windows 문제 해결 스크립트
├── .dockerignore          # Docker 빌드 제외 파일
└── README.md              # 프로젝트 문서
```

## 🚀 Docker 환경의 장점

### 1. **간편한 배포**
- 환경 설정 불필요
- 의존성 충돌 방지
- 일관된 실행 환경

### 2. **확장성**
- 여러 인스턴스 실행 가능
- 로드 밸런싱 지원
- 컨테이너 오케스트레이션

### 3. **개발 편의성**
- 핫 리로드 지원 (개발 모드)
- 로그 집중 관리
- 환경 격리

## Vision API의 장점

### 기존 OCR 대비 개선사항

1. **정확도 향상**: Tesseract OCR보다 훨씬 정확한 텍스트 인식
2. **표 구조 이해**: 단순 텍스트 추출이 아닌 표의 논리적 구조 파악
3. **다국어 지원**: 한국어, 영어 등 다양한 언어 혼재 문서 처리
4. **이미지 품질**: 저해상도 이미지에서도 높은 인식률
5. **컨텍스트 이해**: 이미지 전체 맥락을 고려한 분석

### 지원 이미지 형식

- **PNG** (.png) - 투명도 지원
- **JPEG** (.jpg, .jpeg) - 압축 이미지
- **TIFF** (.tiff) - 고품질 이미지
- **BMP** (.bmp) - 비트맵 이미지
- **WebP** (.webp) - 최신 웹 이미지 형식
- **GIF** (.gif) - 정적 GIF (애니메이션 제외)

## 주의사항

1. **OpenAI API 키**: 유효한 OpenAI API 키가 필요합니다
2. **API 비용**: GPT-4o Vision 모델 사용 시 OpenAI API 비용이 발생합니다
3. **파일 크기**: 이미지 파일은 최대 50MB까지 지원됩니다
4. **이미지 품질**: 고해상도 이미지에서 더 정확한 결과를 얻을 수 있습니다
5. **API 제한**: OpenAI API 사용량 제한을 확인하세요
6. **Docker 메모리**: 최소 2GB RAM 권장

## 비용 계산

### Vision API 토큰 계산

이미지 입력은 토큰으로 측정되며, 모델에 따라 비용이 다릅니다:

- **GPT-4o**: 기본 85 토큰 + 타일당 170 토큰
- **GPT-4o-mini**: 기본 2833 토큰 + 타일당 5667 토큰
- **GPT-4.1**: 기본 85 토큰 + 타일당 170 토큰

### 비용 최적화 팁

1. **detail 파라미터**: `"low"`로 설정하여 토큰 비용 절약
2. **이미지 크기**: 필요에 따라 이미지 크기 조정
3. **배치 처리**: 여러 이미지를 한 번에 처리하여 효율성 향상

## 🚨 문제 해결

### 일반적인 오류

1. **OpenAI API 오류**: API 키와 모델명을 확인하세요
2. **이미지 형식 오류**: 지원되는 이미지 형식인지 확인하세요
3. **파일 크기 오류**: 50MB 이하의 파일인지 확인하세요
4. **API 제한**: OpenAI API 사용량 제한을 확인하세요
5. **Docker 오류**: Docker Desktop이 실행 중인지 확인하세요

### httpx 호환성 문제 해결

`TypeError: Client.__init__() got an unexpected keyword argument 'proxies'` 오류가 발생하는 경우:

```bash
# Docker 컨테이너 재빌드
docker-compose build --no-cache

# 또는 로컬에서 의존성 재설치
pip uninstall httpx openai
pip install -r requirements.txt
```

### Docker 문제 해결

#### 문제 해결 스크립트 실행

**Windows**:
```cmd
docker-troubleshoot.bat
```

**Linux/macOS**:
```bash
chmod +x docker-troubleshoot.sh
./docker-troubleshoot.sh
```

#### 수동 문제 해결

```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f

# 컨테이너 재시작
docker-compose restart

# 컨테이너 재빌드
docker-compose build --no-cache

# 모든 컨테이너 정리
docker-compose down --remove-orphans

# Docker 시스템 정리
docker system prune -f
docker image prune -f
```

### 로그 확인

```bash
# Docker 로그
docker-compose logs -f

# 특정 서비스 로그
docker-compose logs -f table-extraction-api
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
