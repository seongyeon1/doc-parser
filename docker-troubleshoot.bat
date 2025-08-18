@echo off
chcp 65001 >nul

echo 🔧 Docker 문제 해결 스크립트
echo ============================

echo.
echo 1. Docker 상태 확인
echo -------------------
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker 설치됨
) else (
    echo ❌ Docker가 설치되지 않음
    pause
    exit /b 1
)

docker info >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker 실행 중
) else (
    echo ❌ Docker가 실행되지 않음
    echo    Docker Desktop을 시작하세요
    pause
    exit /b 1
)

echo.
echo 2. Docker Compose 확인
echo ----------------------
docker-compose --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker Compose 설치됨
) else (
    echo ❌ Docker Compose가 설치되지 않음
    pause
    exit /b 1
)

echo.
echo 3. 컨테이너 상태 확인
echo ---------------------
docker-compose ps

echo.
echo 4. 최근 로그 확인
echo -----------------
docker-compose logs --tail=20

echo.
echo 5. 문제 해결 명령어
echo -------------------
echo 전체 로그 확인: docker-compose logs -f
echo 컨테이너 재시작: docker-compose restart
echo 컨테이너 재빌드: docker-compose build --no-cache
echo 모든 컨테이너 정리: docker-compose down --remove-orphans
echo Docker 시스템 정리: docker system prune -f
echo 이미지 정리: docker image prune -f

echo.
echo 🎯 문제가 지속되면 위의 명령어들을 순서대로 실행해보세요.
pause
