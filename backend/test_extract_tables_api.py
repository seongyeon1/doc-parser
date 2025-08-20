#!/usr/bin/env python3
"""
extract-tables API 테스트 스크립트
PNG 이미지 지원 및 모델 선택 기능 테스트
"""

import requests
import json
import os
from pathlib import Path

# API 기본 URL
BASE_URL = "http://localhost:8000"

def test_extract_tables_pdf():
    """PDF 파일에서 표 추출 테스트"""
    print("=== PDF 파일 표 추출 테스트 ===")
    
    # 테스트용 PDF 파일 경로 (실제 파일이 있어야 함)
    pdf_file = "sample.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"테스트 파일 {pdf_file}이 존재하지 않습니다. 테스트를 건너뜁니다.")
        return
    
    try:
        with open(pdf_file, 'rb') as f:
            files = {'file': (pdf_file, f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/extract-tables", files=files)
        
        print(f"상태 코드: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"성공: {result['success']}")
            print(f"표 개수: {result.get('table_count', 0)}")
            print(f"사용 모델: {result.get('extraction_method', 'N/A')}")
        else:
            print(f"오류: {response.text}")
            
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")

def test_extract_tables_png():
    """PNG 이미지에서 표 추출 테스트"""
    print("\n=== PNG 이미지 표 추출 테스트 ===")
    
    # 테스트용 PNG 파일 경로 (실제 파일이 있어야 함)
    png_file = "sample.png"
    
    if not os.path.exists(png_file):
        print(f"테스트 파일 {png_file}이 존재하지 않습니다. 테스트를 건너뜁니다.")
        return
    
    try:
        with open(png_file, 'rb') as f:
            files = {'file': (png_file, f, 'image/png')}
            response = requests.post(f"{BASE_URL}/extract-tables", files=files)
        
        print(f"상태 코드: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"성공: {result['success']}")
            print(f"표 개수: {result.get('table_count', 0)}")
            print(f"사용 모델: {result.get('extraction_method', 'N/A')}")
        else:
            print(f"오류: {response.text}")
            
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")

def test_extract_tables_with_model():
    """특정 모델을 지정하여 표 추출 테스트"""
    print("\n=== 특정 모델 지정 테스트 ===")
    
    # 테스트용 파일 경로 (실제 파일이 있어야 함)
    test_file = "sample.pdf"
    
    if not os.path.exists(test_file):
        print(f"테스트 파일 {test_file}이 존재하지 않습니다. 테스트를 건너뜁니다.")
        return
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': (test_file, f, 'application/pdf')}
            data = {'model': 'gpt-4o-mini'}  # 특정 모델 지정
            response = requests.post(f"{BASE_URL}/extract-tables", files=files, data=data)
        
        print(f"상태 코드: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"성공: {result['success']}")
            print(f"표 개수: {result.get('table_count', 0)}")
            print(f"사용 모델: {result.get('extraction_method', 'N/A')}")
        else:
            print(f"오류: {response.text}")
            
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")

def test_health_check():
    """API 상태 확인"""
    print("\n=== API 상태 확인 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"상태 코드: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"상태: {result['status']}")
            print(f"기본 모델: {result.get('model', 'N/A')}")
        else:
            print(f"오류: {response.text}")
            
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")

def create_sample_files():
    """테스트용 샘플 파일 생성 (간단한 예시)"""
    print("\n=== 테스트용 샘플 파일 생성 ===")
    
    # 간단한 테스트용 텍스트 파일 생성
    sample_text = """이것은 테스트 문서입니다.

표 1: 매출 현황
| 월 | 매출 | 비용 | 순이익 |
|----|------|------|--------|
| 1월 | 1000 | 600 | 400 |
| 2월 | 1200 | 700 | 500 |

표 2: 제품별 판매량
| 제품 | 1월 | 2월 |
|------|------|------|
| A제품 | 50 | 60 |
| B제품 | 30 | 35 |
"""
    
    with open("sample.txt", "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    print("sample.txt 파일이 생성되었습니다.")
    print("실제 PDF나 PNG 파일을 준비하여 테스트하세요.")

def main():
    """메인 테스트 함수"""
    print("extract-tables API 테스트 시작")
    print("=" * 50)
    
    # API 상태 확인
    test_health_check()
    
    # 테스트용 파일이 없으면 생성 안내
    if not any(os.path.exists(f) for f in ["sample.pdf", "sample.png", "sample.txt"]):
        create_sample_files()
    
    # PDF 테스트
    test_extract_tables_pdf()
    
    # PNG 테스트
    test_extract_tables_png()
    
    # 모델 지정 테스트
    test_extract_tables_with_model()
    
    print("\n" + "=" * 50)
    print("테스트 완료")

if __name__ == "__main__":
    main()
