#!/bin/bash

# 🧹 Docker 캐시 완전 삭제 및 재빌드 스크립트

echo "🧹 Docker 캐시 완전 삭제 및 재빌드 시작..."
echo "================================================"

# 1. 기존 서비스 중지
echo "1️⃣ 기존 서비스 중지 중..."
docker-compose down --volumes --remove-orphans 2>/dev/null || true

# 2. 모든 컨테이너 삭제
echo "2️⃣ 모든 컨테이너 삭제 중..."
docker container prune -f 2>/dev/null || true

# 3. 모든 이미지 삭제
echo "3️⃣ 모든 이미지 삭제 중..."
docker image prune -a -f 2>/dev/null || true

# 4. 모든 볼륨 삭제
echo "4️⃣ 모든 볼륨 삭제 중..."
docker volume prune -f 2>/dev/null || true

# 5. 모든 네트워크 삭제
echo "5️⃣ 모든 네트워크 삭제 중..."
docker network prune -f 2>/dev/null || true

# 6. 빌드 캐시 삭제
echo "6️⃣ 빌드 캐시 삭제 중..."
docker builder prune -a -f 2>/dev/null || true

# 7. 시스템 전체 정리 (선택사항)
echo "7️⃣ 시스템 전체 정리 중..."
read -p "시스템 전체 정리를 진행하시겠습니까? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker system prune -a --volumes -f
    echo "✅ 시스템 전체 정리 완료"
else
    echo "⏭️ 시스템 전체 정리 건너뜀"
fi

# 8. 필요한 디렉토리 재생성
echo "8️⃣ 필요한 디렉토리 재생성 중..."
mkdir -p analyze/data analyze/result
chmod -R 755 analyze/

# 9. 강제로 새로 빌드
echo "9️⃣ Docker 이미지 강제 재빌드 중..."
docker-compose build --no-cache

# 10. 서비스 시작
echo "🔟 서비스 시작 중..."
docker-compose up -d

# 11. 상태 확인
echo "📊 서비스 상태 확인 중..."
sleep 5
docker-compose ps

echo ""
echo "🎉 Docker 캐시 삭제 및 재빌드 완료!"
echo ""
echo "📋 다음 단계:"
echo "   1. 로그 확인: docker-compose logs -f"
echo "   2. API 테스트: curl http://localhost:8000/health"
echo "   3. 시각화 확인: http://localhost:8080/visualize_results.html"
echo ""
echo "🔍 문제가 있다면:"
echo "   docker-compose logs -f api-server"
