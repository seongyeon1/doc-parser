#!/bin/bash

# Document Analysis API Docker 실행 스크립트
# OpenAI의 새로운 PDF 입력 기능을 지원하는 API를 실행합니다.

echo "🚀 Document Analysis API Docker 실행을 시작합니다..."

# 환경 변수 파일 확인
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다. 환경 변수를 설정해주세요."
    echo "예시:"
    echo "OPENAI_API_KEY=your_openai_api_key_here"
    echo "OPENAI_MODEL=gpt-5"
    exit 1
fi

# 환경 변수 로드
source .env

# OpenAI API 키 확인
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY가 설정되지 않았습니다."
    echo ".env 파일에 OpenAI API 키를 설정해주세요."
    exit 1
fi

echo "✅ 환경 변수 확인 완료"
echo "📋 OpenAI Model: ${OPENAI_MODEL:-gpt-5}"

# 필요한 디렉토리 생성
echo "📁 필요한 디렉토리를 생성합니다..."
mkdir -p logs
mkdir -p uploads
mkdir -p test_files
mkdir -p test_results

# Docker 이미지 빌드
echo "🔨 Docker 이미지를 빌드합니다..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Docker 이미지 빌드에 실패했습니다."
    exit 1
fi

# 서비스 실행
echo "🚀 Document Analysis API를 실행합니다..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ 서비스 실행에 실패했습니다."
    exit 1
fi

# 서비스 상태 확인
echo "⏳ 서비스 상태를 확인합니다..."
sleep 10

# 헬스 체크
echo "🏥 API 헬스 체크를 수행합니다..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$response" = "200" ]; then
    echo "✅ Document Analysis API가 성공적으로 실행되었습니다!"
    echo ""
    echo "📊 서비스 정보:"
    echo "   - 메인 API: http://localhost:8000"
    echo "   - API 문서: http://localhost:8000/docs"
    echo "   - 헬스 체크: http://localhost:8000/health"
    echo ""
    echo "🔧 관리 명령어:"
    echo "   - 로그 확인: docker-compose logs -f"
    echo "   - 서비스 중지: docker-compose down"
    echo "   - 서비스 재시작: docker-compose restart"
    echo ""
    echo "🧪 테스트:"
    echo "   - 샘플 PDF 생성: python create_sample_pdf.py"
    echo "   - API 테스트: python test_pdf_api.py"
else
    echo "❌ API 헬스 체크에 실패했습니다. (HTTP: $response)"
    echo "로그를 확인해주세요: docker-compose logs"
    exit 1
fi
