@echo off
chcp 65001 >nul

echo 🐳 Table Extraction API Docker 실행 스크립트
echo ==========================================

REM Docker 실행 확인
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker가 실행되지 않았습니다.
    echo 📝 Docker Desktop을 시작하세요.
    pause
    exit /b 1
)

REM 환경 변수 파일 확인
if not exist .env (
    echo ❌ .env 파일이 없습니다.
    echo 📝 .env 파일을 생성하고 OpenAI API 키를 설정하세요:
    echo    OPENAI_API_KEY=your_api_key_here
    echo    OPENAI_MODEL=gpt-4o
    pause
    exit /b 1
)

echo ✅ 환경 변수 파일 확인 완료

REM 기존 컨테이너 정리
echo 🧹 기존 컨테이너 정리 중...
docker-compose down --remove-orphans >nul 2>&1

REM Docker 이미지 빌드
echo 🔨 Docker 이미지 빌드 중...
docker-compose build --no-cache

if %errorlevel% neq 0 (
    echo ❌ Docker 이미지 빌드에 실패했습니다.
    echo 📋 로그를 확인하세요: docker-compose logs
    pause
    exit /b 1
)

REM 컨테이너 실행
echo 🚀 컨테이너 실행 중...
docker-compose up -d

if %errorlevel% neq 0 (
    echo ❌ 컨테이너 실행에 실패했습니다.
    echo 📋 로그를 확인하세요: docker-compose logs
    pause
    exit /b 1
)

REM 상태 확인
echo ⏳ 서비스 시작 대기 중...
timeout /t 15 /nobreak >nul

REM 헬스 체크
echo 🏥 헬스 체크 중...
set max_attempts=10
set attempt=1

:health_check_loop
curl -f http://localhost:8000/health >nul 2>&1

if %errorlevel% equ 0 (
    echo ✅ 서비스가 정상적으로 실행되었습니다!
    echo 🌐 API 문서: http://localhost:8000/docs
    echo 🔍 헬스 체크: http://localhost:8000/health
    echo 📊 표 추출 API: http://localhost:8000/extract-tables
    echo.
    echo 📝 사용법:
    echo    - API 문서: http://localhost:8000/docs
    echo    - 파일 업로드: POST /extract-tables
    echo    - 로그 확인: docker-compose logs -f
    echo    - 서비스 중지: docker-compose down
    echo.
    echo 🎯 브라우저에서 http://localhost:8000/docs 를 열어 API를 테스트하세요!
    goto :end
)

if %attempt% lss %max_attempts% (
    echo ⏳ 서비스 시작 대기 중... (시도 %attempt%/%max_attempts%)
    set /a attempt+=1
    timeout /t 5 /nobreak >nul
    goto :health_check_loop
)

echo ❌ 서비스 시작에 실패했습니다.
echo 📋 로그를 확인하세요: docker-compose logs

:end
pause
