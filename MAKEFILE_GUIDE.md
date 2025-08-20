# 🚀 Makefile 사용 가이드

`analyze`와 `doc-parser` 폴더를 한번에 잘 작동할 수 있도록 Makefile 시스템을 구축했습니다!

## 📁 생성된 파일들

- **`Makefile`** - 루트 디렉토리 메인 Makefile
- **`doc-parser/Makefile`** - API 서버 전용 Makefile
- **`analyze/Makefile`** - 시각화 도구 전용 Makefile
- **`start_system.sh`** - Linux/macOS용 시작 스크립트

## 🎯 주요 기능

### 1. 전체 시스템 관리
```bash
# 전체 시스템 시작 (API + 시각화 서버)
make start

# 전체 시스템 중지
make stop

# 서버 상태 확인
make status

# 빠른 시작 (설치 + 시작)
make quick-start
```

### 2. 개별 서버 관리
```bash
# API 서버만 시작
make start-api

# 시각화 서버만 시작
make start-viz

# 백그라운드에서 시작
make start-api-bg
make start-viz-bg
```

### 3. 개발 및 테스트
```bash
# 패키지 설치
make install

# 테스트 실행
make test

# 임시 파일 정리
make clean

# 코드 검사
make check
```

## 🚀 사용 방법

### 방법 1: Makefile 사용 (권장)

#### 전체 시스템 시작
```bash
# 1. 루트 디렉토리에서
make start

# 2. 브라우저에서 접속
# http://localhost:8080/visualize_results.html
```

#### 개별 작업
```bash
# API 서버만
make start-api

# 시각화 서버만
make start-viz

# 이미지 처리
make process-all

# GUI 도구
make visualize
```

### 방법 2: 스크립트 사용

#### Windows
```cmd
# 배치 파일 실행
start_system.bat
```

#### Linux/macOS
```bash
# 실행 권한 부여
chmod +x start_system.sh

# 스크립트 실행
./start_system.sh
```

### 방법 3: 폴더별 Makefile 사용

#### doc-parser 폴더
```bash
cd doc-parser
make help        # 도움말
make install     # 패키지 설치
make start       # API 서버 시작
make test        # 테스트 실행
```

#### analyze 폴더
```bash
cd analyze
make help        # 도움말
make install     # 패키지 설치
make start       # 시각화 서버 시작
make process     # 이미지 처리
make visualize   # GUI 도구
```

## 📋 명령어 요약

### 루트 Makefile
| 명령어 | 설명 |
|--------|------|
| `make help` | 도움말 표시 |
| `make install` | 모든 패키지 설치 |
| `make start` | 전체 시스템 시작 |
| `make stop` | 모든 서버 중지 |
| `make status` | 서버 상태 확인 |
| `make test` | 전체 테스트 실행 |
| `make clean` | 임시 파일 정리 |
| `make quick-start` | 설치 + 시작 |

### doc-parser Makefile
| 명령어 | 설명 |
|--------|------|
| `make start` | API 서버 시작 |
| `make start-bg` | 백그라운드에서 시작 |
| `make stop` | 서버 중지 |
| `make test` | 테스트 실행 |
| `make health` | 서버 상태 확인 |

### analyze Makefile
| 명령어 | 설명 |
|--------|------|
| `make start` | 시각화 서버 시작 |
| `make process` | 모든 이미지 처리 |
| `make quick` | 빠른 이미지 처리 |
| `make visualize` | GUI 도구 실행 |
| `make list` | 파일 목록 표시 |

## 🔧 고급 사용법

### 1. 백그라운드 실행
```bash
# API 서버를 백그라운드에서 시작
make start-api-bg

# 시각화 서버를 백그라운드에서 시작
make start-viz-bg

# 상태 확인
make status
```

### 2. 특정 모델로 처리
```bash
cd analyze
make process-model
# 모델명 입력 (예: gpt-4o-mini)
```

### 3. 서버 모니터링
```bash
# Linux/macOS에서 실시간 모니터링
./start_system.sh

# 10초마다 서버 상태 자동 확인
```

## 🐛 문제 해결

### Makefile이 작동하지 않음
```bash
# Windows에서
# 1. Git Bash 또는 WSL 사용
# 2. 또는 start_system.bat 사용

# Linux/macOS에서
# 1. 실행 권한 확인: ls -la Makefile
# 2. 권한 부여: chmod +x Makefile
```

### 포트 충돌
```bash
# 사용 중인 포트 확인
netstat -an | grep :8000
netstat -an | grep :8080

# 서버 중지
make stop
```

### 권한 문제
```bash
# Windows: 관리자 권한으로 실행
# Linux/macOS: sudo 사용
sudo make start
```

## 💡 팁

1. **첫 실행**: `make quick-start`로 모든 설정을 한번에
2. **개발 중**: `make start-api-bg`로 API 서버를 백그라운드에서 실행
3. **테스트**: `make test`로 모든 기능 확인
4. **정리**: `make clean`으로 임시 파일 정리
5. **상태 확인**: `make status`로 서버 상태 모니터링

## 🎉 완료!

이제 `make start` 한 번으로 전체 시스템을 시작할 수 있습니다!

### 추천 워크플로우
1. **첫 설정**: `make quick-start`
2. **일상 사용**: `make start`
3. **개발 중**: `make start-api-bg` + `make start-viz-bg`
4. **정리**: `make stop` + `make clean`

Makefile을 사용하면 복잡한 명령어를 기억할 필요 없이 간단하게 프로젝트를 관리할 수 있습니다! 🚀
