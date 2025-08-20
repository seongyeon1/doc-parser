# 경로 문제 해결 가이드

## 문제 상황
업로드 기능과 API 실행이 작동하지 않는 문제가 발생했습니다. 주요 원인은 경로 설정의 문제였습니다.

## 해결된 문제들

### 1. 상대 경로 문제
**이전 코드:**
```python
IMAGES_DIR = Path("analyze/data")  # 상대 경로
```

**수정된 코드:**
```python
BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "analyze" / "data"  # 절대 경로
RESULTS_DIR = BASE_DIR / "result"
UPLOADS_DIR = BASE_DIR / "uploads"
```

### 2. Docker 볼륨 마운트 불일치
**이전 설정:**
```yaml
volumes:
  - ./uploads:/tmp/uploads  # 일부만 마운트
```

**수정된 설정:**
```yaml
volumes:
  - ./analyze:/app/analyze      # 이미지 저장 디렉토리
  - ./result:/app/result        # 결과 저장 디렉토리
  - ./uploads:/tmp/uploads      # 임시 업로드 디렉토리
```

### 3. 결과 저장 경로 누락
**추가된 기능:**
- 이미지 업로드 시 메타데이터를 `result/` 디렉토리에 JSON으로 저장
- 이미지 분석 결과를 `result/` 디렉토리에 저장
- 각 작업마다 타임스탬프를 포함한 고유한 파일명 생성

## 새로운 API 엔드포인트

### `/paths` - 경로 정보 확인
현재 설정된 모든 경로와 디렉토리 존재 여부를 확인할 수 있습니다.

```bash
GET /paths
```

**응답 예시:**
```json
{
  "base_dir": "/app",
  "images_dir": "/app/analyze/data",
  "results_dir": "/app/result",
  "uploads_dir": "/tmp/uploads",
  "docker_uploads_exists": true,
  "images_dir_exists": true,
  "results_dir_exists": true,
  "uploads_dir_exists": true
}
```

## 디렉토리 구조

```
doc-parser/
├── analyze/
│   └── data/          # 업로드된 이미지 파일
├── result/             # 분석 결과 및 메타데이터
├── uploads/            # 임시 업로드 파일
├── logs/               # 로그 파일
└── main.py             # 메인 API 서버
```

## 테스트 방법

### 1. 경로 테스트
```bash
python test_paths.py
```

### 2. API 테스트
```bash
# 경로 정보 확인
curl http://localhost:8000/paths

# 이미지 업로드
curl -X POST -F "file=@test.png" http://localhost:8000/upload-image

# 이미지 목록 확인
curl http://localhost:8000/list-images
```

## Docker 실행 시 주의사항

1. **볼륨 마운트 확인**: `docker-compose.yml`에서 모든 필요한 디렉토리가 마운트되었는지 확인
2. **권한 문제**: 컨테이너 내부에서 디렉토리 생성 및 파일 쓰기 권한 확인
3. **경로 일관성**: 로컬과 Docker 환경에서 동일한 경로 구조 유지

## 문제 해결 체크리스트

- [ ] `analyze/data` 디렉토리가 존재하는가?
- [ ] `result` 디렉토리가 존재하는가?
- [ ] `uploads` 디렉토리가 존재하는가?
- [ ] Docker 볼륨이 올바르게 마운트되었는가?
- [ ] API 서버가 정상적으로 시작되었는가?
- [ ] `/paths` 엔드포인트가 올바른 경로를 반환하는가?

## 추가 개선사항

1. **로깅 강화**: 파일 작업 시 상세한 로그 기록
2. **에러 핸들링**: 경로 관련 오류에 대한 명확한 에러 메시지
3. **자동 복구**: 필요한 디렉토리가 없을 때 자동 생성
4. **백업 기능**: 중요한 데이터 자동 백업
