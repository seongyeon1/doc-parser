# 🐳 Docker 백그라운드 이미지 처리 실행 가이드

이 문서는 Docker 환경에서 Document Analysis API의 백그라운드 이미지 처리 기능을 실행하는 방법을 설명합니다.

## 🚀 빠른 시작

### 1. 환경 변수 설정

먼저 `.env` 파일을 생성하고 OpenAI API 키를 설정합니다:

```bash
# doc_parser 폴더에서
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
echo "OPENAI_MODEL=gpt-4o" >> .env
```

### 2. Docker 실행

```bash
# 실행 권한 부여
chmod +x docker-run.sh

# Docker로 실행
./docker-run.sh
```

### 3. 서비스 확인

- **API 서버**: http://localhost:8000
- **시각화 도구**: http://localhost:8080/visualize_results.html
- **API 문서**: http://localhost:8000/docs

## 📁 경로 구조

Docker 환경에서는 다음과 같은 경로 구조를 사용합니다:

```
호스트 시스템                    Docker 컨테이너
doc_parser/                    /app/
├── analyze/                   ├── data/          (이미지 파일)
│   ├── data/                 ├── result/        (결과 파일)
│   └── result/               └── uploads/       (업로드 파일)
└── doc-parser/
    └── main.py
```

## 🔧 Docker 설정 상세

### docker-compose.yml

```yaml
volumes:
  - ./doc-parser:/app                    # 소스 코드
  - ./analyze/data:/app/data            # 이미지 데이터
  - ./analyze/result:/app/result        # 결과 파일
```

### main.py 경로 설정

```python
if Path("/app").exists():
    # Docker 환경
    BASE_DIR = Path("/app")
    IMAGES_DIR = BASE_DIR / "data"      # /app/data
    RESULTS_DIR = BASE_DIR / "result"   # /app/result
```

## 📋 사용 방법

### 1. 이미지 업로드

```bash
curl -X POST "http://localhost:8000/upload-image" \
  -F "file=@your_image.png"
```

### 2. 백그라운드 표 추출

```bash
curl -X POST "http://localhost:8000/background/extract-tables" \
  -F "file=@your_image.png" \
  -F "model=gpt-4o"
```

### 3. 작업 상태 확인

```bash
# 작업 ID로 상태 확인
curl "http://localhost:8000/background/task-status/{task_id}"

# 모든 작업 목록
curl "http://localhost:8000/background/all-tasks"
```

### 4. 작업 취소

```bash
curl -X DELETE "http://localhost:8000/background/cancel-task/{task_id}"
```

## 🧪 테스트

### 자동 테스트 스크립트

```bash
# 테스트 실행
python test_docker_background.py
```

### 수동 테스트

1. **헬스체크**
   ```bash
   curl http://localhost:8000/health
   ```

2. **경로 정보 확인**
   ```bash
   curl http://localhost:8000/paths
   ```

3. **백그라운드 처리 테스트**
   - 이미지 파일 준비
   - 백그라운드 작업 제출
   - 상태 모니터링
   - 결과 확인

## 🔍 문제 해결

### 일반적인 문제들

#### 1. 포트 충돌

```bash
# 포트 사용 확인
lsof -i :8000
lsof -i :8080

# 기존 컨테이너 정리
docker-compose down
```

#### 2. 권한 문제

```bash
# Docker 볼륨 권한 수정
sudo chown -R $USER:$USER analyze/
chmod -R 755 analyze/
```

#### 3. 메모리 부족

```bash
# Docker 메모리 제한 확인
docker stats

# 컨테이너 재시작
docker-compose restart
```

### 로그 확인

```bash
# API 서버 로그
docker-compose logs -f api-server

# 전체 로그
docker-compose logs -f

# 특정 시간 이후 로그
docker-compose logs --since="2024-01-01T00:00:00" api-server
```

## 📊 모니터링

### 컨테이너 상태

```bash
# 실행 중인 컨테이너 확인
docker-compose ps

# 리소스 사용량
docker stats

# 컨테이너 상세 정보
docker inspect doc-parser-api
```

### API 상태

```bash
# 헬스체크
curl -f http://localhost:8000/health

# 경로 정보
curl http://localhost:8000/paths

# 백그라운드 작업 수
curl http://localhost:8000/background/all-tasks
```

## 🛑 서비스 관리

### 서비스 중지

```bash
# 모든 서비스 중지
docker-compose down

# 특정 서비스만 중지
docker-compose stop api-server
```

### 서비스 재시작

```bash
# 전체 재시작
docker-compose restart

# 특정 서비스만 재시작
docker-compose restart api-server
```

### 서비스 업데이트

```bash
# 코드 변경 후 재빌드
docker-compose build
docker-compose up -d
```

## 🔄 개발 모드

### 개발용 Docker Compose

```bash
# 개발 모드로 실행
docker-compose -f docker-compose.dev.yml up -d
```

### 실시간 로그

```bash
# 실시간 로그 모니터링
docker-compose logs -f --tail=100
```

## 📈 성능 최적화

### Docker 설정 최적화

```yaml
# docker-compose.yml
services:
  api-server:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
        reservations:
          memory: 1G
          cpus: '1.0'
```

### 백그라운드 프로세서 설정

```python
# main.py
background_processor = BackgroundProcessor(RESULTS_DIR, max_workers=5)  # 워커 수 증가
```

## 🎯 다음 단계

1. **로드 밸런싱**: 여러 API 인스턴스 실행
2. **Redis 큐**: 작업 큐를 Redis로 외부화
3. **모니터링**: Prometheus + Grafana 설정
4. **로깅**: ELK 스택 연동
5. **CI/CD**: 자동 배포 파이프라인 구축

## 📞 지원

문제가 발생하면 다음을 확인하세요:

1. Docker 로그: `docker-compose logs`
2. API 상태: `curl http://localhost:8000/health`
3. 경로 설정: `curl http://localhost:8000/paths`
4. 시스템 리소스: `docker stats`

---

**🎉 이제 Docker 환경에서 백그라운드 이미지 처리를 사용할 수 있습니다!**
