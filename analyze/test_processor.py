#!/usr/bin/env python3
"""
프로세서 기능 테스트 스크립트
"""

import os
import sys
from pathlib import Path
from process_analyze_data import AnalyzeDataProcessor

def test_api_connection():
    """API 연결 테스트"""
    print("🔍 API 연결 테스트...")
    
    processor = AnalyzeDataProcessor()
    if processor.check_api_health():
        print("✅ API 연결 성공!")
        return True
    else:
        print("❌ API 연결 실패!")
        return False

def test_file_discovery():
    """파일 발견 테스트"""
    print("\n🔍 파일 발견 테스트...")
    
    processor = AnalyzeDataProcessor()
    png_files = list(processor.data_dir.glob("*.png"))
    
    if png_files:
        print(f"✅ {len(png_files)}개의 PNG 파일 발견:")
        for file in png_files:
            print(f"   - {file.name}")
        return True
    else:
        print("❌ PNG 파일을 찾을 수 없습니다.")
        return False

def test_single_image_processing():
    """단일 이미지 처리 테스트"""
    print("\n🖼️ 단일 이미지 처리 테스트...")
    
    processor = AnalyzeDataProcessor()
    png_files = list(processor.data_dir.glob("*.png"))
    
    if not png_files:
        print("❌ 테스트할 PNG 파일이 없습니다.")
        return False
    
    # 첫 번째 파일로 테스트
    test_file = png_files[0]
    print(f"테스트 파일: {test_file.name}")
    
    try:
        result = processor.process_single_image(test_file)
        
        if result.get("success"):
            print(f"✅ 처리 성공: {result.get('table_count', 0)}개 표 발견")
            return True
        else:
            print(f"❌ 처리 실패: {result.get('error', 'unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ 테스트 중 오류: {e}")
        return False

def test_summary_generation():
    """요약 생성 테스트"""
    print("\n📊 요약 생성 테스트...")
    
    processor = AnalyzeDataProcessor()
    
    # 가상의 결과 데이터로 테스트
    test_results = [
        {
            "success": True,
            "table_count": 2,
            "tables": [
                {"title": "테스트 표 1", "row_count": 3, "column_count": 4},
                {"title": "테스트 표 2", "row_count": 2, "column_count": 3}
            ],
            "metadata": {"source_image": "test1.png"}
        },
        {
            "success": False,
            "error": "테스트 오류",
            "tables": [],
            "metadata": {"source_image": "test2.png"}
        }
    ]
    
    try:
        summary = processor.generate_summary_report(test_results)
        
        print(f"✅ 요약 생성 성공:")
        print(f"   총 이미지: {summary['summary']['total_images']}")
        print(f"   성공: {summary['summary']['successful_images']}")
        print(f"   실패: {summary['summary']['failed_images']}")
        print(f"   총 표: {summary['summary']['total_tables']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 요약 생성 실패: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🧪 프로세서 기능 테스트 시작")
    print("=" * 50)
    
    tests = [
        ("API 연결", test_api_connection),
        ("파일 발견", test_file_discovery),
        ("단일 이미지 처리", test_single_image_processing),
        ("요약 생성", test_summary_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} 테스트 중 예외 발생: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("🎉 모든 테스트 통과!")
        return True
    else:
        print("⚠️ 일부 테스트 실패")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
