#!/bin/bash

# Docker 실행 스크립트
# Table Extraction API를 Docker로 실행합니다.

set -e

echo "🐳 Table Extraction API Docker 실행 스크립트"
echo "=========================================="

# Docker 실행 확인
if ! command -v docker &> /dev/null; then
    echo "❌ Docker가 설치되지 않았습니다."
    echo "📝 Docker Desktop을 설치하고 실행하세요."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker가 실행되지 않았습니다."
    echo "📝 Docker Desktop을 시작하세요."
    exit 1
fi

# Docker Compose 확인
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose가 설치되지 않았습니다."
    echo "📝 Docker Compose를 설치하세요."
    exit 1
fi

# 환경 변수 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없습니다."
    echo "📝 .env 파일을 생성하고 OpenAI API 키를 설정하세요:"
    echo "   OPENAI_API_KEY=your_api_key_here"
    echo "   OPENAI_MODEL=gpt-4o"
    exit 1
fi

# 환경 변수 로드
source .env

# API 키 확인
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_api_key_here" ]; then
    echo "❌ OPENAI_API_KEY가 설정되지 않았습니다."
    echo "📝 .env 파일에서 올바른 API 키를 설정하세요."
    exit 1
fi

echo "✅ 환경 변수 확인 완료"
echo "🔑 API 모델: ${OPENAI_MODEL:-gpt-4o}"

# 기존 컨테이너 정리
echo "🧹 기존 컨테이너 정리 중..."
docker-compose down --remove-orphans 2>/dev/null || true

# Docker 이미지 빌드
echo "🔨 Docker 이미지 빌드 중..."
docker-compose build --no-cache

if [ $? -ne 0 ]; then
    echo "❌ Docker 이미지 빌드에 실패했습니다."
    echo "📋 로그를 확인하세요: docker-compose logs"
    exit 1
fi

# 컨테이너 실행
echo "🚀 컨테이너 실행 중..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ 컨테이너 실행에 실패했습니다."
    echo "📋 로그를 확인하세요: docker-compose logs"
    exit 1
fi

# 상태 확인
echo "⏳ 서비스 시작 대기 중..."
sleep 15

# 헬스 체크
echo "🏥 헬스 체크 중..."
max_attempts=10
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ 서비스가 정상적으로 실행되었습니다!"
        echo "🌐 API 문서: http://localhost:8000/docs"
        echo "🔍 헬스 체크: http://localhost:8000/health"
        echo "📊 표 추출 API: http://localhost:8000/extract-tables"
        echo ""
        echo "📝 사용법:"
        echo "   - API 문서: http://localhost:8000/docs"
        echo "   - 파일 업로드: POST /extract-tables"
        echo "   - 로그 확인: docker-compose logs -f"
        echo "   - 서비스 중지: docker-compose down"
        echo ""
        echo "🎯 브라우저에서 http://localhost:8000/docs 를 열어 API를 테스트하세요!"
        exit 0
    else
        echo "⏳ 서비스 시작 대기 중... (시도 $attempt/$max_attempts)"
        sleep 5
        attempt=$((attempt + 1))
    fi
done

echo "❌ 서비스 시작에 실패했습니다."
echo "📋 로그를 확인하세요: docker-compose logs"
exit 1
