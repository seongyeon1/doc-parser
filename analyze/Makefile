# 📊 Analyze Data Processing Makefile
# analyze 폴더 전용 작업을 위한 Makefile

.PHONY: help install start stop test clean process visualize quick-process

# 기본 설정
PYTHON = python
PIP = pip
PORT = 8080

# 도움말
help:
	@echo "📊 Analyze Data Processing - Makefile 도움말"
	@echo "=========================================="
	@echo ""
	@echo "📋 사용 가능한 명령어:"
	@echo "  make install       - 필요한 패키지 설치"
	@echo "  make start         - 시각화 서버 시작"
	@echo "  make stop          - 시각화 서버 중지"
	@echo "  make process       - 모든 이미지 처리"
	@echo "  make quick         - 빠른 이미지 처리"
	@echo "  make visualize     - GUI 시각화 도구 실행"
	@echo "  make test          - 테스트 실행"
	@echo "  make clean         - 임시 파일 정리"
	@echo "  make status        - 서버 상태 확인"
	@echo "  make list          - 사용 가능한 파일 목록"
	@echo ""

# 패키지 설치
install:
	@echo "📦 패키지 설치 중..."
	$(PIP) install -r requirements.txt
	@echo "✅ 패키지 설치 완료!"

# 시각화 서버 시작
start:
	@echo "🌐 시각화 서버 시작 중... (포트: $(PORT))"
	@echo "📊 서버 URL: http://localhost:$(PORT)"
	@echo "🖼️ 시각화 도구: http://localhost:$(PORT)/visualize_results.html"
	@echo "💡 중지하려면 Ctrl+C를 누르세요"
	@echo ""
	$(PYTHON) serve_files.py

# 백그라운드에서 서버 시작
start-bg:
	@echo "🌐 시각화 서버를 백그라운드에서 시작 중... (포트: $(PORT))"
	@$(PYTHON) serve_files.py &
	@echo "✅ 시각화 서버가 백그라운드에서 실행 중입니다."
	@echo "📊 서버 URL: http://localhost:$(PORT)"

# 서버 중지
stop:
	@echo "🛑 시각화 서버 중지 중..."
	@-pkill -f "python serve_files.py" || echo "서버가 이미 중지됨"
	@echo "✅ 시각화 서버가 중지되었습니다."

# 모든 이미지 처리
process:
	@echo "🖼️ 모든 이미지 처리 중..."
	$(PYTHON) process_analyze_data.py

# 빠른 이미지 처리
quick:
	@echo "⚡ 빠른 이미지 처리 중..."
	$(PYTHON) quick_process.py

# 특정 모델로 이미지 처리
process-model:
	@echo "🤖 특정 모델로 이미지 처리 중..."
	@read -p "모델명을 입력하세요 (예: gpt-4o-mini): " model; \
	$(PYTHON) quick_process.py $$model

# GUI 시각화 도구 실행
visualize:
	@echo "🖥️ GUI 시각화 도구 실행 중..."
	$(PYTHON) visualize_results.py

# 명령행 뷰어 실행
viewer:
	@echo "💻 명령행 뷰어 실행 중..."
	$(PYTHON) simple_viewer.py

# 테스트 실행
test:
	@echo "🧪 테스트 실행 중..."
	$(PYTHON) test_processor.py
	@echo "✅ 테스트 완료!"

# 임시 파일 정리
clean:
	@echo "🧹 임시 파일 정리 중..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name "*.log" -delete
	@echo "✅ 정리 완료!"

# 서버 상태 확인
status:
	@echo "📊 시각화 서버 상태 확인 중..."
	@curl -s http://localhost:$(PORT) > /dev/null && echo "✅ 서버 실행 중" || echo "❌ 서버가 실행되지 않음"

# 사용 가능한 파일 목록
list:
	@echo "📁 사용 가능한 파일 목록:"
	@echo ""
	@echo "🖼️ 이미지 파일 (data/ 폴더):"
	@if [ -d "data" ]; then ls -la data/*.png 2>/dev/null || echo "  PNG 파일이 없습니다"; else echo "  data 폴더가 없습니다"; fi
	@echo ""
	@echo "📋 결과 파일 (result/ 폴더):"
	@if [ -d "result" ]; then ls -la result/*.json 2>/dev/null || echo "  JSON 파일이 없습니다"; else echo "  result 폴더가 없습니다"; fi

# Windows용 명령어
ifeq ($(OS),Windows_NT)
start-bg:
	@echo "🌐 시각화 서버를 백그라운드에서 시작 중... (포트: $(PORT))"
	@start /B $(PYTHON) serve_files.py
	@echo "✅ 시각화 서버가 백그라운드에서 실행 중입니다."
	@echo "📊 서버 URL: http://localhost:$(PORT)"

stop:
	@echo "🛑 시각화 서버 중지 중..."
	@taskkill /F /IM python.exe /T 2>nul || echo "서버가 이미 중지됨"
	@echo "✅ 시각화 서버가 중지되었습니다."

process-model:
	@echo "🤖 특정 모델로 이미지 처리 중..."
	@set /p model="모델명을 입력하세요 (예: gpt-4o-mini): "
	@$(PYTHON) quick_process.py %model%
endif
