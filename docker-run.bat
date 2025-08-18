@echo off
REM Document Analysis API Docker 실행 스크립트 (Windows)
REM OpenAI의 새로운 PDF 입력 기능을 지원하는 API를 실행합니다.

echo 🚀 Document Analysis API Docker 실행을 시작합니다...

REM 환경 변수 파일 확인
if not exist .env (
    echo ⚠️  .env 파일이 없습니다. 환경 변수를 설정해주세요.
    echo 예시:
    echo OPENAI_API_KEY=your_openai_api_key_here
    echo OPENAI_MODEL=gpt-5
    pause
    exit /b 1
)

REM 필요한 디렉토리 생성
echo 📁 필요한 디렉토리를 생성합니다...
if not exist logs mkdir logs
if not exist uploads mkdir uploads
if not exist test_files mkdir test_files
if not exist test_results mkdir test_results

REM Docker 이미지 빌드
echo 🔨 Docker 이미지를 빌드합니다...
docker-compose build

if %errorlevel% neq 0 (
    echo ❌ Docker 이미지 빌드에 실패했습니다.
    pause
    exit /b 1
)

REM 서비스 실행
echo 🚀 Document Analysis API를 실행합니다...
docker-compose up -d

if %errorlevel% neq 0 (
    echo ❌ 서비스 실행에 실패했습니다.
    pause
    exit /b 1
)

REM 서비스 상태 확인
echo ⏳ 서비스 상태를 확인합니다...
timeout /t 10 /nobreak > nul

REM 헬스 체크
echo 🏥 API 헬스 체크를 수행합니다...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/health' -UseBasicParsing; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"

if %errorlevel% equ 0 (
    echo ✅ Document Analysis API가 성공적으로 실행되었습니다!
    echo.
    echo 📊 서비스 정보:
    echo    - 메인 API: http://localhost:8000
    echo    - API 문서: http://localhost:8000/docs
    echo    - 헬스 체크: http://localhost:8000/health
    echo.
    echo 🔧 관리 명령어:
    echo    - 로그 확인: docker-compose logs -f
    echo    - 서비스 중지: docker-compose down
    echo    - 서비스 재시작: docker-compose restart
    echo.
    echo 🧪 테스트:
    echo    - 샘플 PDF 생성: python create_sample_pdf.py
    echo    - API 테스트: python test_pdf_api.py
    echo.
    echo 🎯 브라우저에서 http://localhost:8000/docs 를 열어 API를 테스트하세요!
) else (
    echo ❌ API 헬스 체크에 실패했습니다.
    echo 로그를 확인해주세요: docker-compose logs
)

pause
