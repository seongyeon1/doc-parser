# 🔧 Document Parser API Makefile
# doc-parser 폴더 전용 작업을 위한 Makefile

.PHONY: help install start stop test clean health check

# 기본 설정
PYTHON = python
PIP = pip
PORT = 8000

# 도움말
help:
	@echo "🔧 Document Parser API - Makefile 도움말"
	@echo "====================================="
	@echo ""
	@echo "📋 사용 가능한 명령어:"
	@echo "  make install      - 필요한 패키지 설치"
	@echo "  make start        - API 서버 시작"
	@echo "  make stop         - API 서버 중지"
	@echo "  make test         - 테스트 실행"
	@echo "  make clean        - 임시 파일 정리"
	@echo "  make health       - 서버 상태 확인"
	@echo "  make check        - 코드 검사"
	@echo ""

# 패키지 설치
install:
	@echo "📦 패키지 설치 중..."
	$(PIP) install -r requirements.txt
	@echo "✅ 패키지 설치 완료!"

# API 서버 시작
start:
	@echo "🚀 API 서버 시작 중... (포트: $(PORT))"
	@echo "📊 서버 URL: http://localhost:$(PORT)"
	@echo "📚 API 문서: http://localhost:$(PORT)/docs"
	@echo "💡 중지하려면 Ctrl+C를 누르세요"
	@echo ""
	$(PYTHON) main.py

# 백그라운드에서 서버 시작
start-bg:
	@echo "🚀 API 서버를 백그라운드에서 시작 중... (포트: $(PORT))"
	@$(PYTHON) main.py &
	@echo "✅ API 서버가 백그라운드에서 실행 중입니다."
	@echo "📊 서버 URL: http://localhost:$(PORT)"

# 서버 중지
stop:
	@echo "🛑 API 서버 중지 중..."
	@-pkill -f "python main.py" || echo "서버가 이미 중지됨"
	@echo "✅ API 서버가 중지되었습니다."

# 테스트 실행
test:
	@echo "🧪 테스트 실행 중..."
	@if [ -f "test_api.py" ]; then $(PYTHON) test_api.py; fi
	@if [ -f "test_extract_tables_api.py" ]; then $(PYTHON) test_extract_tables_api.py; fi
	@if [ -f "test_pdf_api.py" ]; then $(PYTHON) test_pdf_api.py; fi
	@if [ -f "test_image_api.py" ]; then $(PYTHON) test_image_api.py; fi
	@echo "✅ 테스트 완료!"

# 임시 파일 정리
clean:
	@echo "🧹 임시 파일 정리 중..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name "*.log" -delete
	@echo "✅ 정리 완료!"

# 서버 상태 확인
health:
	@echo "📊 API 서버 상태 확인 중..."
	@curl -s http://localhost:$(PORT)/health || echo "❌ 서버가 실행되지 않음"

# 코드 검사
check:
	@echo "🔍 코드 검사 중..."
	@if command -v flake8 > /dev/null; then flake8 .; else echo "flake8이 설치되지 않음"; fi
	@if command -v black > /dev/null; then black --check .; else echo "black이 설치되지 않음"; fi

# Windows용 명령어
ifeq ($(OS),Windows_NT)
start-bg:
	@echo "🚀 API 서버를 백그라운드에서 시작 중... (포트: $(PORT))"
	@start /B $(PYTHON) main.py
	@echo "✅ API 서버가 백그라운드에서 실행 중입니다."
	@echo "📊 서버 URL: http://localhost:$(PORT)"

stop:
	@echo "🛑 API 서버 중지 중..."
	@taskkill /F /IM python.exe /T 2>nul || echo "서버가 이미 중지됨"
	@echo "✅ API 서버가 중지되었습니다."
endif
