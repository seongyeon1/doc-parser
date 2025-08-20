#!/usr/bin/env python3
"""
Docker 환경에서 백그라운드 이미지 처리를 테스트하는 스크립트
"""

import requests
import time
import json
from pathlib import Path

# API 서버 설정
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """API 서버 헬스체크"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API 서버가 정상적으로 실행되고 있습니다.")
            return True
        else:
            print(f"❌ API 서버 응답 오류: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API 서버 연결 실패: {e}")
        return False

def test_paths():
    """경로 정보 확인"""
    try:
        response = requests.get(f"{API_BASE_URL}/paths")
        if response.status_code == 200:
            paths = response.json()
            print("\n📁 현재 경로 설정:")
            print(f"   BASE_DIR: {paths.get('base_dir')}")
            print(f"   IMAGES_DIR: {paths.get('images_dir')}")
            print(f"   RESULTS_DIR: {paths.get('results_dir')}")
            print(f"   UPLOADS_DIR: {paths.get('uploads_dir')}")
            return paths
        else:
            print(f"❌ 경로 정보 조회 실패: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 경로 정보 조회 중 오류: {e}")
        return None

def test_background_processing():
    """백그라운드 처리 테스트"""
    print("\n🔄 백그라운드 처리 테스트 시작...")
    
    # 테스트용 더미 이미지 파일 생성
    test_image_path = Path("test_image.png")
    if not test_image_path.exists():
        # 간단한 PNG 파일 생성 (1x1 픽셀)
        png_data = bytes.fromhex('89504e470d0a1a0a0000000d4948445200000001000000010802000000907753de0000000b4944415478da6364f8cf000000020001e5c7c0c00000000049454e44ae426082')
        with open(test_image_path, 'wb') as f:
            f.write(png_data)
        print("📝 테스트 이미지 파일을 생성했습니다.")
    
    try:
        # 백그라운드 표 추출 작업 제출
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test_image.png', f, 'image/png')}
            data = {'model': 'gpt-4o'}
            
            print("📤 백그라운드 작업 제출 중...")
            response = requests.post(
                f"{API_BASE_URL}/background/extract-tables",
                files=files,
                data=data
            )
        
        if response.status_code == 202:
            result = response.json()
            task_id = result.get('task_id')
            print(f"✅ 백그라운드 작업이 제출되었습니다.")
            print(f"   작업 ID: {task_id}")
            print(f"   상태: {result.get('status')}")
            
            # 작업 상태 모니터링
            print("\n📊 작업 상태 모니터링 중...")
            max_attempts = 30  # 최대 30번 시도 (1분)
            attempt = 0
            
            while attempt < max_attempts:
                time.sleep(2)  # 2초마다 상태 확인
                attempt += 1
                
                try:
                    status_response = requests.get(f"{API_BASE_URL}/background/task-status/{task_id}")
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        task_status = status_data.get('task_status', {})
                        
                        status = task_status.get('status')
                        progress = task_status.get('progress', 0)
                        
                        print(f"   시도 {attempt}: 상태={status}, 진행률={progress}%")
                        
                        if status in ['completed', 'failed', 'cancelled']:
                            print(f"\n🏁 작업 완료: {status}")
                            if status == 'completed':
                                print(f"   결과 파일: {task_status.get('result_file', 'N/A')}")
                            elif status == 'failed':
                                print(f"   오류: {task_status.get('error', 'N/A')}")
                            break
                    else:
                        print(f"   시도 {attempt}: 상태 조회 실패 ({status_response.status_code})")
                except requests.exceptions.RequestException as e:
                    print(f"   시도 {attempt}: 상태 조회 중 오류: {e}")
            
            if attempt >= max_attempts:
                print("⏰ 타임아웃: 작업이 완료되지 않았습니다.")
            
            return task_id
        else:
            print(f"❌ 백그라운드 작업 제출 실패: {response.status_code}")
            print(f"   응답: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 백그라운드 처리 테스트 중 오류: {e}")
        return None

def test_all_background_tasks():
    """모든 백그라운드 작업 목록 조회"""
    try:
        response = requests.get(f"{API_BASE_URL}/background/all-tasks")
        if response.status_code == 200:
            result = response.json()
            tasks = result.get('tasks', [])
            print(f"\n📋 현재 백그라운드 작업 수: {len(tasks)}")
            
            for i, task in enumerate(tasks):
                print(f"   작업 {i+1}: {task.get('filename', 'N/A')} - {task.get('status', 'N/A')}")
            
            return tasks
        else:
            print(f"❌ 작업 목록 조회 실패: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ 작업 목록 조회 중 오류: {e}")
        return []

def cleanup_test_files():
    """테스트 파일 정리"""
    test_image_path = Path("test_image.png")
    if test_image_path.exists():
        test_image_path.unlink()
        print("🧹 테스트 이미지 파일을 정리했습니다.")

def main():
    """메인 테스트 함수"""
    print("🚀 Docker 백그라운드 이미지 처리 테스트")
    print("=" * 50)
    
    # 1. 헬스체크
    if not test_health_check():
        print("❌ API 서버가 실행되지 않았습니다. Docker를 먼저 실행해주세요.")
        return
    
    # 2. 경로 정보 확인
    paths = test_paths()
    if not paths:
        print("❌ 경로 정보를 가져올 수 없습니다.")
        return
    
    # 3. 백그라운드 처리 테스트
    task_id = test_background_processing()
    
    # 4. 모든 작업 목록 확인
    test_all_background_tasks()
    
    # 5. 테스트 파일 정리
    cleanup_test_files()
    
    print("\n🎉 테스트 완료!")
    if task_id:
        print(f"   생성된 작업 ID: {task_id}")
        print(f"   상태 확인: {API_BASE_URL}/background/task-status/{task_id}")

if __name__ == "__main__":
    main()
