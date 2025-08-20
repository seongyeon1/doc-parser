#!/usr/bin/env python3
"""
경로 설정 테스트 스크립트
"""

from pathlib import Path
import os

def test_paths():
    """경로 설정을 테스트합니다."""
    
    print("=== 경로 설정 테스트 ===\n")
    
    # 현재 스크립트 위치
    SCRIPT_DIR = Path(__file__).parent
    print(f"스크립트 디렉토리: {SCRIPT_DIR}")
    
    # 프로젝트 루트 (doc_parser 폴더)
    PROJECT_ROOT = SCRIPT_DIR.parent
    print(f"프로젝트 루트: {PROJECT_ROOT}")
    
    # analyze 폴더 확인
    analyze_dir = PROJECT_ROOT / "analyze"
    print(f"analyze 폴더: {analyze_dir}")
    print(f"analyze 폴더 존재: {analyze_dir.exists()}")
    
    if analyze_dir.exists():
        # analyze 폴더가 있는 경우
        BASE_DIR = PROJECT_ROOT
        IMAGES_DIR = analyze_dir / "data"
        RESULTS_DIR = analyze_dir / "result"
        UPLOADS_DIR = PROJECT_ROOT / "uploads"
        
        print(f"\n✅ analyze 폴더 사용:")
        print(f"   BASE_DIR: {BASE_DIR}")
        print(f"   IMAGES_DIR: {IMAGES_DIR}")
        print(f"   RESULTS_DIR: {RESULTS_DIR}")
        print(f"   UPLOADS_DIR: {UPLOADS_DIR}")
        
        # 각 디렉토리 존재 여부 확인
        print(f"\n📁 디렉토리 존재 여부:")
        print(f"   IMAGES_DIR 존재: {IMAGES_DIR.exists()}")
        print(f"   RESULTS_DIR 존재: {RESULTS_DIR.exists()}")
        print(f"   UPLOADS_DIR 존재: {UPLOADS_DIR.exists()}")
        
        # 절대 경로로 변환
        print(f"\n🔗 절대 경로:")
        print(f"   IMAGES_DIR 절대: {IMAGES_DIR.absolute()}")
        print(f"   RESULTS_DIR 절대: {RESULTS_DIR.absolute()}")
        
    else:
        # analyze 폴더가 없는 경우
        BASE_DIR = SCRIPT_DIR
        IMAGES_DIR = BASE_DIR / "analyze" / "data"
        RESULTS_DIR = BASE_DIR / "analyze" / "result"
        UPLOADS_DIR = BASE_DIR / "uploads"
        
        print(f"\n⚠️ 기본 경로 사용:")
        print(f"   BASE_DIR: {BASE_DIR}")
        print(f"   IMAGES_DIR: {IMAGES_DIR}")
        print(f"   RESULTS_DIR: {RESULTS_DIR}")
        print(f"   UPLOADS_DIR: {UPLOADS_DIR}")
    
    # 현재 작업 디렉토리
    print(f"\n📂 현재 작업 디렉토리: {os.getcwd()}")
    
    # 환경 변수 확인
    print(f"\n🌍 환경 변수:")
    print(f"   PWD: {os.environ.get('PWD', 'N/A')}")
    print(f"   CWD: {os.getcwd()}")

if __name__ == "__main__":
    test_paths()
