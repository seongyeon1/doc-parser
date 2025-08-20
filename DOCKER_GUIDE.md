# 🐳 Docker 환경에서 Document Parser 실행 가이드

`analyze`와 `doc-parser` 폴더를 Docker 환경에서 실행할 수 있도록 완벽한 Docker 시스템을 구축했습니다!

## 📁 생성된 Docker 파일들

- **`docker-compose.yml`** - 메인 Docker Compose 설정
- **`docker-compose.dev.yml`** - 개발 환경 오버라이드
- **`Makefile.docker`** - Docker 전용 Makefile
- **`doc-parser/Dockerfile`** - API 서버 Docker 이미지
- **`doc-parser/Dockerfile.dev`** - 개발용 API 서버 이미지
- **`analyze/Dockerfile`** - 시각화 도구 Docker 이미지
- **`analyze/Dockerfile.dev`** - 개발용 시각화 도구 이미지
- **`nginx.conf`** - Nginx 리버스 프록시 설정
- **`env.example`** - 환경 변수 예시 파일
- **`docker-run.sh`** - Linux/macOS용 실행 스크립트
- **`docker-run.bat`** - Windows용 실행 스크립트

## 🚀 빠른 시작

### 1. Docker 환경 확인
```bash
# Docker 설치 확인
docker --version
docker-compose --version

# 설치되지 않은 경우: https://docs.docker.com/get-docker/
```

### 2. 환경 변수 설정
```bash
# 환경 변수 파일 생성
cp env.example .env

# .env 파일 편집하여 OpenAI API 키 설정
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Docker로 실행
```bash
# 방법 1: 스크립트 사용 (권장)
./docker-run.sh          # Linux/macOS
docker-run.bat           # Windows

# 방법 2: Makefile 사용
make -f Makefile.docker docker-quick-start

# 방법 3: 직접 실행
docker-compose up -d
```

## 🎯 주요 기능

### 📊 서비스 구성
- **API 서버**: 포트 8000 (FastAPI)
- **시각화 서버**: 포트 8080 (Python HTTP 서버)
- **Nginx**: 포트 80 (리버스 프록시, 선택사항)

### 🔧 환경별 실행
- **프로덕션**: `docker-compose up -d`
- **개발**: `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d`

## 📋 Docker 명령어

### 기본 관리
```bash
# 컨테이너 시작
docker-compose up -d

# 컨테이너 중지
docker-compose down

# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f
```

### Makefile 사용
```bash
# Docker 전용 Makefile 사용
make -f Makefile.docker help

# 이미지 빌드
make -f Makefile.docker docker-build

# 컨테이너 시작
make -f Makefile.docker docker-start

# 컨테이너 중지
make -f Makefile.docker docker-stop

# 로그 확인
make -f Makefile.docker docker-logs

# 컨테이너 쉘 접속
make -f Makefile.docker docker-shell-api
make -f Makefile.docker docker-shell-viz
```

## 🔧 고급 설정

### 1. 개발 모드
```bash
# 개발 모드로 실행 (코드 변경 시 자동 반영)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# 또는 Makefile 사용
make -f Makefile.docker docker-dev
```

### 2. 프로덕션 모드
```bash
# 프로덕션 모드로 실행
make -f Makefile.docker docker-prod
```

### 3. 환경 변수 커스터마이징
```bash
# .env 파일에서 설정
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
API_PORT=8000
VIZ_PORT=8080
```

## 🐛 문제 해결

### Docker 설치 문제
```bash
# Docker Desktop 설치 확인
# Windows: Docker Desktop 실행
# Linux: sudo systemctl start docker
# macOS: Docker Desktop 실행
```

### 포트 충돌
```bash
# 사용 중인 포트 확인
netstat -an | grep :8000
netstat -an | grep :8080

# docker-compose.yml에서 포트 변경
```

### 권한 문제
```bash
# Linux에서 Docker 권한 문제
sudo usermod -aG docker $USER
# 재로그인 필요
```

### 컨테이너 로그 확인
```bash
# 전체 로그
docker-compose logs

# 특정 서비스 로그
docker-compose logs api-server
docker-compose logs viz-server

# 실시간 로그
docker-compose logs -f
```

## 💡 사용 팁

### 1. 개발 워크플로우
```bash
# 1. 개발 모드로 시작
make -f Makefile.docker docker-dev

# 2. 코드 수정 (볼륨 마운트로 자동 반영)

# 3. 로그 확인
make -f Makefile.docker docker-logs

# 4. 테스트 실행
make -f Makefile.docker docker-test
```

### 2. 데이터 백업
```bash
# 데이터 백업
make -f Makefile.docker docker-backup

# 백업 파일은 backups/ 폴더에 저장
```

### 3. 이미지 업데이트
```bash
# 최신 이미지로 업데이트
make -f Makefile.docker docker-update
```

## 🔍 모니터링

### 컨테이너 상태 확인
```bash
# 상태 확인
make -f Makefile.docker docker-status

# 리소스 사용량
docker stats
```

### 헬스체크
```bash
# API 서버 헬스체크
curl http://localhost:8000/health

# 시각화 서버 헬스체크
curl http://localhost:8080
```

## 🌐 접속 정보

### 서비스 URL
- **API 서버**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **시각화 도구**: http://localhost:8080/visualize_results.html
- **통합 접속**: http://localhost (Nginx)

### API 엔드포인트
- **테이블 추출**: POST http://localhost:8000/extract-tables
- **파일 업로드**: POST http://localhost:8000/upload
- **이미지 목록**: GET http://localhost:8080/api/images

## 🎉 완료!

이제 Docker 환경에서 `docker-compose up -d` 한 번으로 전체 시스템을 실행할 수 있습니다!

### 추천 워크플로우
1. **첫 설정**: `./docker-run.sh` 또는 `docker-run.bat`
2. **일상 사용**: `docker-compose up -d`
3. **개발 중**: `make -f Makefile.docker docker-dev`
4. **정리**: `docker-compose down`

Docker를 사용하면 환경 의존성 없이 어디서든 동일하게 실행할 수 있습니다! 🐳✨
