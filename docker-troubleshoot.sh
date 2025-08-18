#!/bin/bash

# Docker 문제 해결 스크립트

echo "🔧 Docker 문제 해결 스크립트"
echo "============================"

echo ""
echo "1. Docker 상태 확인"
echo "-------------------"
if command -v docker &> /dev/null; then
    echo "✅ Docker 설치됨: $(docker --version)"
else
    echo "❌ Docker가 설치되지 않음"
    exit 1
fi

if docker info &> /dev/null; then
    echo "✅ Docker 실행 중"
else
    echo "❌ Docker가 실행되지 않음"
    echo "   Docker Desktop을 시작하세요"
    exit 1
fi

echo ""
echo "2. Docker Compose 확인"
echo "----------------------"
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose 설치됨: $(docker-compose --version)"
else
    echo "❌ Docker Compose가 설치되지 않음"
    exit 1
fi

echo ""
echo "3. 컨테이너 상태 확인"
echo "---------------------"
docker-compose ps

echo ""
echo "4. 최근 로그 확인"
echo "-----------------"
docker-compose logs --tail=20

echo ""
echo "5. 시스템 리소스 확인"
echo "---------------------"
echo "메모리 사용량:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

echo ""
echo "6. 문제 해결 명령어"
echo "-------------------"
echo "전체 로그 확인: docker-compose logs -f"
echo "컨테이너 재시작: docker-compose restart"
echo "컨테이너 재빌드: docker-compose build --no-cache"
echo "모든 컨테이너 정리: docker-compose down --remove-orphans"
echo "Docker 시스템 정리: docker system prune -f"
echo "이미지 정리: docker image prune -f"
