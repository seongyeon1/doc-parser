# 📊 Document Parser Project Makefile
# 전체 프로젝트를 한번에 관리할 수 있는 Makefile

.PHONY: help install start stop clean test visualize process-all

# 기본 설정
PYTHON = python
PIP = pip
PORT_API = 8000
PORT_VIZ = 8080

# 도움말
help:
	@echo "📊 Document Parser Project - Makefile 도움말"
	@echo "=========================================="
	@echo ""
	@echo "🔧 기본 명령어:"
	@echo "  make install      - 필요한 패키지 설치"
	@echo "  make start        - API 서버와 시각화 서버 동시 시작"
	@echo "  make start-api    - API 서버만 시작"
	@echo "  make start-viz    - 시각화 서버만 시작"
	@echo "  make stop         - 모든 서버 중지"
	@echo "  make clean        - 임시 파일 정리"
	@echo "  make test         - 테스트 실행"
	@echo "  make visualize    - 시각화 도구 실행"
	@echo "  make process-all  - 모든 이미지 처리"
	@echo "  make status       - 서버 상태 확인"
	@echo ""
	@echo "📁 폴더별 명령어:"
	@echo "  make doc-parser   - doc-parser 폴더 관련 작업"
	@echo "  make analyze      - analyze 폴더 관련 작업"
	@echo ""
	@echo "🚀 빠른 시작:"
	@echo "  make quick-start  - 전체 시스템 빠른 시작"

# 패키지 설치
install:
	@echo "📦 필요한 패키지 설치 중..."
	$(PIP) install -r doc-parser/requirements.txt
	$(PIP) install -r analyze/requirements.txt
	@echo "✅ 패키지 설치 완료!"

# 전체 시스템 시작
start: start-api start-viz
	@echo "🚀 전체 시스템이 시작되었습니다!"
	@echo "📊 API 서버: http://0.0.0.0:$(PORT_API) (외부 접근 가능)"
	@echo "🌐 시각화 도구: http://0.0.0.0:$(PORT_VIZ)/visualize_results.html (외부 접근 가능)"
	@echo ""
	@echo "💡 사용법:"
	@echo "  1. 브라우저에서 시각화 도구 열기"
	@echo "  2. 외부 접근: http://[서버IP]:$(PORT_VIZ)/visualize_results.html"
	@echo "  3. 이미지 선택 및 처리"
	@echo "  4. Ctrl+C로 서버 중지"

# API 서버 시작
start-api:
	@echo "🔧 API 서버 시작 중... (포트: $(PORT_API))"
	@cd doc-parser && $(PYTHON) main.py &
	@echo "✅ API 서버가 백그라운드에서 실행 중입니다."

# 시각화 서버 시작
start-viz:
	@echo "🌐 시각화 서버 시작 중... (포트: $(PORT_VIZ))"
	@cd analyze && $(PYTHON) serve_files.py &
	@echo "✅ 시각화 서버가 백그라운드에서 실행 중입니다."

# 모든 서버 중지
stop:
	@echo "🛑 서버 중지 중..."
	@-pkill -f "python main.py"
	@-pkill -f "python serve_files.py"
	@echo "✅ 모든 서버가 중지되었습니다."

# 임시 파일 정리
clean:
	@echo "🧹 임시 파일 정리 중..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name "*.log" -delete
	@echo "✅ 정리 완료!"

# 테스트 실행
test:
	@echo "🧪 테스트 실행 중..."
	@cd doc-parser && $(PYTHON) -m pytest test_*.py -v
	@cd analyze && $(PYTHON) test_processor.py
	@echo "✅ 테스트 완료!"

# 시각화 도구 실행
visualize:
	@echo "🌐 시각화 도구 실행 중..."
	@cd analyze && $(PYTHON) visualize_results.py

# 모든 이미지 처리
process-all:
	@echo "🖼️ 모든 이미지 처리 중..."
	@cd analyze && $(PYTHON) process_analyze_data.py

# 서버 상태 확인
status:
	@echo "📊 서버 상태 확인 중..."
	@echo "API 서버 상태:"
	@-curl -s http://localhost:$(PORT_API)/health || echo "❌ API 서버가 실행되지 않음"
	@echo ""
	@echo "시각화 서버 상태:"
	@-curl -s http://localhost:$(PORT_VIZ) > /dev/null && echo "✅ 시각화 서버 실행 중" || echo "❌ 시각화 서버가 실행되지 않음"

# 빠른 시작
quick-start: install start
	@echo ""
	@echo "🎉 빠른 시작 완료!"
	@echo "브라우저에서 http://localhost:$(PORT_VIZ)/visualize_results.html 열기"

# doc-parser 폴더 관련 작업
doc-parser:
	@echo "📁 doc-parser 폴더 작업:"
	@echo "  make doc-parser/install    - 패키지 설치"
	@echo "  make doc-parser/start      - API 서버 시작"
	@echo "  make doc-parser/test       - 테스트 실행"
	@echo "  make doc-parser/clean      - 정리"

# analyze 폴더 관련 작업
analyze:
	@echo "📁 analyze 폴더 작업:"
	@echo "  make analyze/install       - 패키지 설치"
	@echo "  make analyze/start         - 시각화 서버 시작"
	@echo "  make analyze/process       - 이미지 처리"
	@echo "  make analyze/visualize     - GUI 도구 실행"
	@echo "  make analyze/test          - 테스트 실행"

# Windows용 명령어
ifeq ($(OS),Windows_NT)
start-api:
	@echo "🔧 API 서버 시작 중... (포트: $(PORT_API))"
	@cd doc-parser && start /B $(PYTHON) main.py
	@echo "✅ API 서버가 백그라운드에서 실행 중입니다."

start-viz:
	@echo "🌐 시각화 서버 시작 중... (포트: $(PORT_VIZ))"
	@cd analyze && start /B $(PYTHON) serve_files.py
	@echo "✅ 시각화 서버가 백그라운드에서 실행 중입니다."

stop:
	@echo "🛑 서버 중지 중..."
	@taskkill /F /IM python.exe /T 2>nul || echo "서버가 이미 중지됨"
	@echo "✅ 모든 서버가 중지되었습니다."
endif
