#!/usr/bin/env python3
"""
이미지 업로드 API 테스트 스크립트
"""

import requests
import os
from pathlib import Path

def test_image_upload():
    """이미지 업로드 API 테스트"""
    
    # API 서버 URL
    api_url = "http://localhost:8000"
    
    print("🖼️ 이미지 업로드 API 테스트")
    print("=" * 50)
    
    # 1. 헬스체크
    print("\n1️⃣ API 서버 상태 확인...")
    try:
        response = requests.get(f"{api_url}/health")
        if response.status_code == 200:
            print("✅ API 서버가 정상적으로 실행 중입니다")
            print(f"📊 응답: {response.json()}")
        else:
            print(f"❌ API 서버 오류: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ API 서버 연결 실패: {e}")
        return
    
    # 2. 이미지 목록 조회
    print("\n2️⃣ 현재 이미지 목록 조회...")
    try:
        response = requests.get(f"{api_url}/list-images")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 이미지 목록 조회 성공")
            print(f"📊 총 {result['total_count']}개 이미지")
            for img in result['images']:
                print(f"   - {img['filename']} ({img['size']} bytes)")
        else:
            print(f"❌ 이미지 목록 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 이미지 목록 조회 오류: {e}")
    
    # 3. 샘플 이미지 생성 및 업로드
    print("\n3️⃣ 샘플 이미지 생성 및 업로드...")
    
    # data 폴더 확인
    data_dir = Path("data")
    if not data_dir.exists():
        print("❌ data 폴더가 없습니다")
        return
    
    # PNG 파일 찾기
    png_files = list(data_dir.glob("*.png"))
    if not png_files:
        print("❌ data 폴더에 PNG 파일이 없습니다")
        return
    
    # 첫 번째 PNG 파일로 테스트
    test_image = png_files[0]
    print(f"📁 테스트 이미지: {test_image}")
    
    try:
        with open(test_image, 'rb') as f:
            files = {'file': (test_image.name, f, 'image/png')}
            response = requests.post(f"{api_url}/upload-image", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 이미지 업로드 성공!")
            print(f"📊 업로드된 파일: {result['filename']}")
            print(f"📏 파일 크기: {result['file_size']} bytes")
        else:
            print(f"❌ 이미지 업로드 실패: {response.status_code}")
            print(f"📋 오류 내용: {response.text}")
    except Exception as e:
        print(f"❌ 이미지 업로드 오류: {e}")
    
    # 4. 업로드 후 이미지 목록 재확인
    print("\n4️⃣ 업로드 후 이미지 목록 재확인...")
    try:
        response = requests.get(f"{api_url}/list-images")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 이미지 목록 조회 성공")
            print(f"📊 총 {result['total_count']}개 이미지")
            for img in result['images']:
                print(f"   - {img['filename']} ({img['size']} bytes)")
        else:
            print(f"❌ 이미지 목록 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 이미지 목록 조회 오류: {e}")

def test_image_processing():
    """이미지 처리 API 테스트"""
    
    api_url = "http://localhost:8000"
    
    print("\n🔄 이미지 처리 API 테스트")
    print("=" * 50)
    
    # 1. 이미지 목록에서 첫 번째 이미지 선택
    try:
        response = requests.get(f"{api_url}/list-images")
        if response.status_code != 200:
            print("❌ 이미지 목록을 가져올 수 없습니다")
            return
        
        result = response.json()
        if result['total_count'] == 0:
            print("❌ 처리할 이미지가 없습니다")
            return
        
        # 첫 번째 이미지 선택
        test_image = result['images'][0]['filename']
        print(f"📁 처리할 이미지: {test_image}")
        
        # 2. 이미지 파일 읽기
        image_path = Path("data") / test_image
        if not image_path.exists():
            print(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
            return
        
        with open(image_path, 'rb') as f:
            files = {'file': (test_image, f, 'image/png')}
            data = {'model': 'gpt-4o-mini'}  # 빠른 모델로 테스트
            
            print("🔄 이미지 처리 중...")
            response = requests.post(f"{api_url}/extract-tables", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 이미지 처리 성공!")
            print(f"📊 처리 결과: {result.get('table_count', 'N/A')}개 표 발견")
            print(f"🤖 사용 모델: {result.get('extraction_method', 'N/A')}")
        else:
            print(f"❌ 이미지 처리 실패: {response.status_code}")
            print(f"📋 오류 내용: {response.text}")
            
    except Exception as e:
        print(f"❌ 이미지 처리 테스트 오류: {e}")

if __name__ == "__main__":
    print("🚀 Document Parser API 테스트 시작")
    print("=" * 60)
    
    # 이미지 업로드 테스트
    test_image_upload()
    
    # 이미지 처리 테스트
    test_image_processing()
    
    print("\n🎉 테스트 완료!")
    print("\n💡 다음 단계:")
    print("   1. 브라우저에서 http://localhost:8080/visualize_results.html 열기")
    print("   2. 업로드된 이미지 확인")
    print("   3. 이미지 처리 테스트")
