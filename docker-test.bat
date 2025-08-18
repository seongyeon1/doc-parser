@echo off
chcp 65001 >nul

echo 🧪 Table Extraction API Docker 테스트
echo ====================================

REM API 상태 확인
echo 🔍 API 상태 확인 중...
curl -f http://localhost:8000/health >nul 2>&1

if %errorlevel% equ 0 (
    echo ✅ API가 정상적으로 실행 중입니다.
) else (
    echo ❌ API가 실행되지 않았습니다.
    echo 📝 먼저 docker-run.bat을 실행하여 서비스를 시작하세요.
    pause
    exit /b 1
)

REM 헬스 체크 응답 확인
echo 📊 헬스 체크 응답:
curl -s http://localhost:8000/health

echo.
echo 🎯 테스트 방법:
echo 1. 브라우저에서 http://localhost:8000/docs 접속
echo 2. POST /extract-tables 엔드포인트 선택
echo 3. 파일 업로드하여 테스트
echo.
echo 📁 테스트 파일 준비:
echo    - PDF, DOCX, XLSX, 이미지 파일 등
echo    - 표가 포함된 문서가 좋습니다
echo.
echo 🔧 추가 테스트 명령어:
echo    - 로그 확인: docker-compose logs -f
echo    - 컨테이너 상태: docker-compose ps
echo    - 서비스 중지: docker-compose down
echo.
echo 🌐 브라우저에서 http://localhost:8000/docs 를 열어 API를 테스트하세요!

pause
