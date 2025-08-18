@echo off
REM Document Analysis API Docker 테스트 스크립트 (Windows)
REM OpenAI의 새로운 PDF 입력 기능을 테스트합니다.

echo 🧪 Document Analysis API Docker 테스트를 시작합니다...

REM 환경 변수 파일 확인
if not exist .env (
    echo ⚠️  .env 파일이 없습니다. 환경 변수를 설정해주세요.
    echo 예시:
    echo OPENAI_API_KEY=your_openai_api_key_here
    echo OPENAI_MODEL=gpt-5
    pause
    exit /b 1
)

REM API 서비스가 실행 중인지 확인
echo 🔍 API 서비스 상태를 확인합니다...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/health' -UseBasicParsing; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"

if %errorlevel% neq 0 (
    echo ❌ API 서비스가 실행되지 않았습니다.
    echo 먼저 docker-run.bat를 실행하여 서비스를 시작하세요.
    pause
    exit /b 1
)

echo ✅ API 서비스가 실행 중입니다.

REM 테스트용 샘플 PDF 생성
echo 📄 테스트용 샘플 PDF를 생성합니다...
python create_sample_pdf.py

if %errorlevel% neq 0 (
    echo ❌ 샘플 PDF 생성에 실패했습니다.
    pause
    exit /b 1
)

echo ✅ 샘플 PDF 생성 완료: sample_document.pdf

REM API 테스트 실행
echo 🧪 API 테스트를 실행합니다...
python test_pdf_api.py

if %errorlevel% neq 0 (
    echo ❌ API 테스트에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo 🎉 모든 테스트가 완료되었습니다!
echo.
echo 📊 테스트 결과 요약:
echo    - 샘플 PDF 생성: ✅
echo    - API 연결 테스트: ✅
echo    - PDF 분석 테스트: ✅
echo.
echo 🔧 추가 테스트:
echo    - 브라우저에서 http://localhost:8000/docs 열기
echo    - 다양한 PDF 파일로 테스트
echo    - 다양한 프롬프트로 테스트
echo.
echo 📝 로그 확인:
echo    - Docker 로그: docker-compose logs -f
echo    - API 로그: docker-compose logs document-analysis-api

pause
