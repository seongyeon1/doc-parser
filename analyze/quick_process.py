#!/usr/bin/env python3
"""
간단한 이미지 처리 스크립트
analyze 폴더의 PNG 이미지들을 빠르게 처리
"""

import sys
from pathlib import Path
from process_analyze_data import AnalyzeDataProcessor

def quick_process(model: str = None):
    """
    이미지를 빠르게 처리합니다.
    
    Args:
        model: 사용할 모델명 (예: "gpt-4o-mini", "gpt-4o")
    """
    try:
        # 프로세서 초기화
        processor = AnalyzeDataProcessor()
        
        # API 상태 확인
        if not processor.check_api_health():
            print("❌ API 서버를 먼저 시작해주세요!")
            print("   python main.py (doc-parser 폴더에서)")
            return
        
        # 이미지 처리 (지연 시간 없음)
        results = processor.process_all_images(model=model, delay=0)
        
        if results:
            print(f"\n🎉 완료! {len(results)}개 파일 처리됨")
        else:
            print("\n❌ 처리할 파일이 없습니다.")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def main():
    """메인 함수"""
    print("🚀 빠른 이미지 처리 시작")
    
    # 명령행 인수로 모델 지정 가능
    model = None
    if len(sys.argv) > 1:
        model = sys.argv[1]
        print(f"📋 사용 모델: {model}")
    
    # 처리 실행
    quick_process(model)

if __name__ == "__main__":
    main()
