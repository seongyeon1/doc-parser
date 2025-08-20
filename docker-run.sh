#!/bin/bash

# 🐳 Document Parser API Docker 실행 스크립트
# 백그라운드 이미지 처리를 포함한 전체 시스템을 실행합니다.

set -e

echo "🚀 Document Parser API Docker 실행 시작..."

# 환경 변수 파일 확인
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다. 기본값으로 실행합니다."
    echo "OPENAI_API_KEY=your_api_key_here" > .env
    echo "OPENAI_MODEL=gpt-4o" >> .env
    echo "📝 .env 파일을 생성했습니다. OpenAI API 키를 설정해주세요."
    echo "   OPENAI_API_KEY=your_actual_api_key"
    exit 1
fi

# 환경 변수 로드
source .env

# OpenAI API 키 확인
if [ "$OPENAI_API_KEY" = "your_api_key_here" ] || [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OpenAI API 키가 설정되지 않았습니다."
    echo "   .env 파일에서 OPENAI_API_KEY를 설정해주세요."
    exit 1
fi

echo "✅ 환경 변수 확인 완료"
echo "   OpenAI Model: ${OPENAI_MODEL:-gpt-4o}"

# 필요한 디렉토리 생성
echo "📁 필요한 디렉토리를 생성합니다..."
mkdir -p logs
mkdir -p uploads
mkdir -p test_files
mkdir -p test_results
mkdir -p analyze/data
mkdir -p analyze/result

# Docker 이미지 빌드
echo "🔨 Docker 이미지 빌드 중..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Docker 이미지 빌드에 실패했습니다."
    exit 1
fi

# 서비스 시작
echo "🚀 서비스 시작 중..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ 서비스 실행에 실패했습니다."
    exit 1
fi

# 서비스 상태 확인
echo "📊 서비스 상태 확인 중..."
sleep 10

# API 서버 헬스체크
echo "🏥 API 서버 헬스체크 중..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$response" = "200" ]; then
    echo "✅ API 서버가 정상적으로 실행되고 있습니다."
    echo "   📍 API 엔드포인트: http://localhost:8000"
    echo "   📍 API 문서: http://localhost:8000/docs"
    echo "   📍 백그라운드 처리: http://localhost:8000/background/extract-tables"
    echo "   📍 작업 상태 확인: http://localhost:8000/background/task-status/{task_id}"
else
    echo "❌ API 서버가 정상적으로 실행되지 않았습니다."
    echo "   로그를 확인해주세요: docker-compose logs api-server"
    exit 1
fi

# 시각화 서버 확인
echo "🎨 시각화 서버 확인 중..."
if curl -f http://localhost:8080 >/dev/null 2>&1; then
    echo "✅ 시각화 서버가 정상적으로 실행되고 있습니다."
    echo "   📍 시각화 페이지: http://localhost:8080/visualize_results.html"
else
    echo "⚠️  시각화 서버가 아직 시작되지 않았습니다. 잠시 후 다시 시도해주세요."
fi

echo ""
echo "🎉 Document Parser API가 성공적으로 실행되었습니다!"
echo ""
echo "📋 사용 방법:"
echo "   1. 이미지 업로드: http://localhost:8000/upload-image"
echo "   2. 백그라운드 처리: http://localhost:8000/background/extract-tables"
echo "   3. 시각화: http://localhost:8080/visualize_results.html"
echo ""
echo "🧪 테스트:"
echo "   - 샘플 PDF 생성: python create_sample_pdf.py"
echo "   - API 테스트: python test_pdf_api.py"
echo ""
echo "🔍 로그 확인:"
echo "   API 서버: docker-compose logs -f api-server"
echo "   전체 로그: docker-compose logs -f"
echo ""
echo "🔧 관리 명령어:"
echo "   - 서비스 중지: docker-compose down"
echo "   - 서비스 재시작: docker-compose restart"
