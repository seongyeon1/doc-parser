# Docker 실행 가이드

이 가이드는 Docker를 사용하여 Document Analysis API를 실행하는 방법을 설명합니다.

## 🚀 빠른 시작

### 1. 사전 요구사항

- **Docker Desktop** 설치 및 실행
- **Docker Compose** 지원
- **OpenAI API 키** 발급

### 2. 환경 설정

```bash
# 1. 환경 변수 파일 생성
cp env_example.txt .env

# 2. .env 파일 편집하여 OpenAI API 키 설정
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Docker 실행

#### Linux/macOS
```bash
# 실행 권한 부여
chmod +x docker-run.sh
chmod +x docker-test.sh

# API 실행
./docker-run.sh

# 테스트 실행
./docker-test.sh
```

#### Windows
```cmd
# API 실행
docker-run.bat

# 테스트 실행
docker-test.bat
```

## 🐳 Docker 서비스 구성

### 메인 서비스
- **Port**: 8000
- **Container**: document-analysis-api
- **용도**: 프로덕션 환경

### 개발 서비스
- **Port**: 8001
- **Container**: document-analysis-api-dev
- **용도**: 개발 환경 (핫 리로드)
- **실행**: `docker-compose --profile dev up -d`

### 테스트 서비스
- **Port**: 8002
- **Container**: document-analysis-api-test
- **용도**: 자동화된 테스트
- **실행**: `docker-compose --profile test up`

## 📁 볼륨 마운트

```yaml
volumes:
  - ./logs:/app/logs          # 로그 파일
  - ./uploads:/tmp/uploads     # 파일 업로드
  - ./test_files:/app/test_files      # 테스트 파일
  - ./test_results:/app/test_results  # 테스트 결과
```

## 🔧 수동 Docker 명령어

### 1. 이미지 빌드
```bash
docker-compose build
```

### 2. 서비스 실행
```bash
# 모든 서비스 실행
docker-compose up -d

# 특정 프로파일로 실행
docker-compose --profile dev up -d
docker-compose --profile test up
```

### 3. 서비스 상태 확인
```bash
# 컨테이너 상태
docker-compose ps

# 로그 확인
docker-compose logs -f
docker-compose logs document-analysis-api

# 헬스 체크
curl http://localhost:8000/health
```

### 4. 서비스 관리
```bash
# 서비스 중지
docker-compose down

# 서비스 재시작
docker-compose restart

# 특정 서비스만 재시작
docker-compose restart document-analysis-api
```

### 5. 컨테이너 접속
```bash
# 컨테이너 내부 접속
docker-compose exec document-analysis-api bash

# 로그 실시간 확인
docker-compose exec document-analysis-api tail -f /app/logs/app.log
```

## 🧪 테스트 방법

### 1. 자동 테스트
```bash
# 전체 테스트 실행
./docker-test.sh  # Linux/macOS
docker-test.bat   # Windows
```

### 2. 수동 테스트
```bash
# 1. 샘플 PDF 생성
python create_sample_pdf.py

# 2. API 테스트
python test_pdf_api.py

# 3. 브라우저 테스트
# http://localhost:8000/docs 접속
```

### 3. cURL 테스트
```bash
# 헬스 체크
curl http://localhost:8000/health

# PDF 분석
curl -X POST "http://localhost:8000/analyze-pdf" \
  -F "file=@sample_document.pdf" \
  -F "prompt=이 PDF를 분석해주세요."

# 파일 업로드
curl -X POST "http://localhost:8000/upload-file" \
  -F "file=@sample_document.pdf"
```

## 🔍 문제 해결

### 일반적인 문제

#### 1. 포트 충돌
```bash
# 포트 사용 확인
netstat -tulpn | grep :8000

# 다른 포트로 실행
docker-compose up -d -p 8001
```

#### 2. 메모리 부족
```bash
# Docker 메모리 제한 확인
docker stats

# 메모리 제한 설정 (docker-compose.yml)
deploy:
  resources:
    limits:
      memory: 2G
```

#### 3. 권한 문제
```bash
# 볼륨 권한 확인
ls -la logs/ uploads/

# 권한 수정
chmod 755 logs uploads
```

#### 4. API 키 오류
```bash
# 환경 변수 확인
docker-compose exec document-analysis-api env | grep OPENAI

# .env 파일 재로드
docker-compose down
docker-compose up -d
```

### 로그 분석

#### 1. 애플리케이션 로그
```bash
# 실시간 로그
docker-compose logs -f document-analysis-api

# 특정 시간 로그
docker-compose logs --since="2024-01-01T00:00:00" document-analysis-api

# 에러 로그만
docker-compose logs document-analysis-api | grep ERROR
```

#### 2. 시스템 로그
```bash
# 컨테이너 리소스 사용량
docker stats document-analysis-api

# 컨테이너 상세 정보
docker inspect document-analysis-api
```

## 📊 모니터링

### 1. 헬스 체크
```bash
# 자동 헬스 체크
curl -f http://localhost:8000/health

# 상세 정보
curl http://localhost:8000/health | jq '.'
```

### 2. 성능 모니터링
```bash
# 컨테이너 리소스
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# API 응답 시간
time curl -s http://localhost:8000/health
```

### 3. 로그 분석
```bash
# 요청 수 카운트
docker-compose logs document-analysis-api | grep "POST" | wc -l

# 에러율 계산
docker-compose logs document-analysis-api | grep -c "ERROR"
```

## 🚀 프로덕션 배포

### 1. 환경별 설정
```bash
# 프로덕션 환경
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 스테이징 환경
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
```

### 2. 로드 밸런싱
```bash
# 여러 인스턴스 실행
docker-compose up -d --scale document-analysis-api=3
```

### 3. 백업 및 복구
```bash
# 볼륨 백업
docker run --rm -v document-analysis-api_logs:/data -v $(pwd):/backup alpine tar czf /backup/logs-backup.tar.gz -C /data .

# 백업 복구
docker run --rm -v document-analysis-api_logs:/data -v $(pwd):/backup alpine tar xzf /backup/logs-backup.tar.gz -C /data
```

## 📝 유용한 명령어

### Docker Compose
```bash
# 서비스 상태
docker-compose ps

# 로그 확인
docker-compose logs -f

# 서비스 재시작
docker-compose restart

# 전체 정리
docker-compose down --volumes --remove-orphans
```

### Docker
```bash
# 이미지 정리
docker image prune -f

# 컨테이너 정리
docker container prune -f

# 시스템 정리
docker system prune -f
```

### 네트워크
```bash
# 네트워크 확인
docker network ls

# 포트 확인
netstat -tulpn | grep docker
```

## 🔧 환경 변수 설정

### 필수 환경 변수
```bash
# OpenAI API 키 (필수)
OPENAI_API_KEY=your_openai_api_key_here

# OpenAI 모델 (기본값: gpt-4o)
OPENAI_MODEL=gpt-4o
```

### 선택적 환경 변수
```bash
# API 서버 설정
HOST=0.0.0.0
PORT=8000

# 로그 레벨
LOG_LEVEL=INFO

# 파일 업로드 설정
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=/tmp/uploads

# 개발 모드
DEBUG=true
RELOAD=true
```

## 🎯 지원 모델

OpenAI 공식 문서에 따르면 PDF 입력을 지원하는 모델은 다음과 같습니다:

- **GPT-4o**: PDF 입력 지원 ✅
- **GPT-4o-mini**: PDF 입력 지원 ✅  
- **o1**: PDF 입력 지원 ✅

**참고**: GPT-5는 현재 PDF 입력을 지원하지 않습니다.

이 가이드를 통해 Docker 환경에서 Document Analysis API를 효과적으로 실행하고 관리할 수 있습니다! 🎯
