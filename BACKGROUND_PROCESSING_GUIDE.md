# 백그라운드 이미지 처리 가이드

이 문서는 Document Analysis API의 백그라운드 이미지 처리 기능에 대한 설명입니다.

## 개요

백그라운드 이미지 처리를 통해 이미지 분석과 표 추출 작업을 비동기적으로 실행할 수 있습니다. 이는 대용량 이미지나 긴 처리 시간이 필요한 작업에 특히 유용합니다.

## 주요 기능

- **비동기 처리**: 이미지 업로드 후 즉시 응답, 백그라운드에서 처리
- **작업 상태 추적**: 실시간 진행률 및 상태 모니터링
- **동시 작업 처리**: 여러 이미지를 동시에 처리
- **작업 취소**: 진행 중인 작업 취소 가능
- **자동 정리**: 완료된 작업 자동 정리

## API 엔드포인트

### 1. 백그라운드 이미지 분석

**POST** `/background/analyze-image`

이미지 분석을 백그라운드에서 실행합니다.

**요청 파라미터:**
- `file`: 이미지 파일 (필수)
- `prompt`: 분석 요청 프롬프트 (선택사항, 기본값: "이 이미지를 분석하고 주요 내용을 설명해주세요.")
- `detail`: 이미지 분석 상세도 (선택사항, "low", "high", "auto", 기본값: "auto")
- `callback_url`: 완료 시 호출할 콜백 URL (선택사항)

**응답 예시:**
```json
{
  "success": true,
  "message": "이미지 분석이 백그라운드에서 시작되었습니다.",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "check_status_url": "/background/task-status/550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. 백그라운드 표 추출

**POST** `/background/extract-tables`

표 추출을 백그라운드에서 실행합니다.

**요청 파라미터:**
- `file`: 파일 (필수)
- `model`: 사용할 모델명 (선택사항, 기본값: 환경변수에서 설정된 모델)
- `callback_url`: 완료 시 호출할 콜백 URL (선택사항)

**응답 예시:**
```json
{
  "success": true,
  "message": "표 추출이 백그라운드에서 시작되었습니다.",
  "task_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "pending",
  "check_status_url": "/background/task-status/550e8400-e29b-41d4-a716-446655440001"
}
```

### 3. 작업 상태 조회

**GET** `/background/task-status/{task_id}`

특정 작업의 상태를 조회합니다.

**응답 예시:**
```json
{
  "success": true,
  "task_status": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "filename": "sample_image.png",
    "prompt": "이 이미지를 분석해주세요.",
    "detail": "high",
    "status": "processing",
    "created_at": "2024-01-01T10:00:00",
    "started_at": "2024-01-01T10:00:01",
    "progress": 30,
    "callback_url": null
  }
}
```

### 4. 모든 작업 목록 조회

**GET** `/background/all-tasks`

모든 백그라운드 작업의 목록을 반환합니다.

**응답 예시:**
```json
{
  "success": true,
  "total_count": 3,
  "tasks": [
    {
      "task_id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "image1.png",
      "status": "completed",
      "progress": 100
    },
    {
      "task_id": "550e8400-e29b-41d4-a716-446655440001",
      "filename": "image2.png",
      "status": "processing",
      "progress": 45
    }
  ]
}
```

### 5. 작업 취소

**DELETE** `/background/cancel-task/{task_id}`

진행 중인 작업을 취소합니다.

**응답 예시:**
```json
{
  "success": true,
  "message": "작업 '550e8400-e29b-41d4-a716-446655440001'이(가) 성공적으로 취소되었습니다."
}
```

### 6. 작업 정리

**POST** `/background/cleanup`

완료된 오래된 작업들을 정리합니다.

**요청 파라미터:**
- `max_age_hours`: 정리할 작업의 최대 나이 (시간 단위, 기본값: 24)

**응답 예시:**
```json
{
  "success": true,
  "message": "24시간 이상 된 완료된 작업들이 정리되었습니다."
}
```

## 작업 상태

백그라운드 작업은 다음과 같은 상태를 가집니다:

- **pending**: 작업이 큐에 대기 중
- **processing**: 작업이 실행 중
- **completed**: 작업이 성공적으로 완료됨
- **failed**: 작업 실행 중 오류 발생
- **cancelled**: 작업이 취소됨

## 진행률

각 작업은 0-100% 사이의 진행률을 제공합니다:

- **0%**: 작업 시작
- **10%**: 작업 처리 시작
- **30%**: 실제 분석/추출 시작
- **80%**: 분석/추출 완료, 결과 저장 중
- **100%**: 작업 완료

## 사용 예시

### Python 클라이언트 예시

```python
import requests

# 1. 백그라운드 이미지 분석 제출
with open('image.png', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/background/analyze-image',
        files={'file': f},
        data={'prompt': '이 이미지의 내용을 자세히 분석해주세요.', 'detail': 'high'}
    )

if response.status_code == 202:
    task_data = response.json()
    task_id = task_data['task_id']
    print(f"작업이 제출되었습니다. Task ID: {task_id}")

# 2. 작업 상태 주기적 확인
import time
while True:
    status_response = requests.get(f'http://localhost:8000/background/task-status/{task_id}')
    if status_response.status_code == 200:
        task_status = status_response.json()['task_status']
        print(f"상태: {task_status['status']}, 진행률: {task_status['progress']}%")
        
        if task_status['status'] in ['completed', 'failed', 'cancelled']:
            break
    
    time.sleep(2)  # 2초마다 상태 확인

# 3. 결과 확인
if task_status['status'] == 'completed':
    print("작업이 완료되었습니다!")
    print(f"결과 파일: {task_status.get('result_file', 'N/A')}")
```

### cURL 예시

```bash
# 1. 백그라운드 이미지 분석 제출
curl -X POST "http://localhost:8000/background/analyze-image" \
  -F "file=@image.png" \
  -F "prompt=이 이미지를 분석해주세요." \
  -F "detail=high"

# 2. 작업 상태 확인
curl "http://localhost:8000/background/task-status/{task_id}"

# 3. 모든 작업 목록 조회
curl "http://localhost:8000/background/all-tasks"

# 4. 작업 취소
curl -X DELETE "http://localhost:8000/background/cancel-task/{task_id}"
```

## 설정

백그라운드 프로세서는 다음과 같은 설정을 지원합니다:

- **max_workers**: 동시에 처리할 수 있는 최대 작업 수 (기본값: 3)
- **results_dir**: 결과 파일이 저장될 디렉토리
- **cleanup_interval**: 자동 정리 주기 (시간 단위)

## 주의사항

1. **메모리 사용량**: 동시 작업 수가 많을수록 메모리 사용량이 증가할 수 있습니다.
2. **파일 크기**: 50MB 이하의 이미지 파일만 지원됩니다.
3. **작업 보존**: 작업 상태는 메모리에 저장되므로 서버 재시작 시 손실됩니다.
4. **타임아웃**: 각 작업은 적절한 타임아웃 설정이 필요할 수 있습니다.

## 모니터링 및 로깅

백그라운드 프로세서는 상세한 로그를 제공합니다:

- 작업 제출/시작/완료/실패 이벤트
- 진행률 업데이트
- 오류 발생 시 상세 정보
- 작업 정리 활동

로그는 `analyze/result` 디렉토리에 JSON 형태로 저장됩니다.

## 문제 해결

### 일반적인 문제들

1. **작업이 시작되지 않는 경우**
   - 백그라운드 프로세서가 실행 중인지 확인
   - 작업 큐가 가득 찬 경우 대기

2. **작업이 실패하는 경우**
   - 로그 파일에서 오류 상세 정보 확인
   - 파일 형식 및 크기 제한 확인

3. **메모리 부족 오류**
   - 동시 작업 수 줄이기
   - 서버 리소스 증가

### 디버깅

```python
# 모든 작업 상태 확인
response = requests.get('http://localhost:8000/background/all-tasks')
print(response.json())

# 특정 작업 상세 정보 확인
response = requests.get(f'http://localhost:8000/background/task-status/{task_id}')
print(response.json())
```

## 성능 최적화

1. **적절한 워커 수 설정**: CPU 코어 수와 메모리를 고려하여 설정
2. **작업 우선순위**: 중요한 작업을 먼저 처리하도록 큐 관리
3. **정기적인 정리**: 완료된 작업을 주기적으로 정리하여 메모리 효율성 향상
4. **배치 처리**: 여러 이미지를 한 번에 제출하여 오버헤드 감소
