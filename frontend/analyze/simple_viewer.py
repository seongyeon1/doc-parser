#!/usr/bin/env python3
"""
간단한 명령행 결과 뷰어
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

def print_separator(char="=", length=80):
    """구분선 출력"""
    print(char * length)

def print_header(text: str):
    """헤더 출력"""
    print_separator()
    print(f" {text} ".center(80, "="))
    print_separator()

def print_subheader(text: str):
    """서브헤더 출력"""
    print(f"\n{text}")
    print("-" * len(text))

def display_table(table: Dict[str, Any], index: int):
    """표 정보 출력"""
    print(f"\n📊 표 {index + 1}: {table.get('title', '제목 없음')}")
    print(f"   행: {table.get('row_count', 0)}, 열: {table.get('column_count', 0)}")
    
    # 헤더 출력
    headers = table.get("headers", [])
    if headers:
        print("   헤더:")
        for i, header in enumerate(headers):
            print(f"     {i+1}. {header}")
    
    # 데이터 행 출력
    rows = table.get("rows", [])
    if rows:
        print("   데이터:")
        for i, row in enumerate(rows):
            row_str = " | ".join(str(cell) for cell in row)
            print(f"     {i+1}. {row_str}")

def display_result(result: Dict[str, Any]):
    """결과 출력"""
    print_header("📋 표 추출 결과")
    
    # 기본 정보
    if result.get("success"):
        print("✅ 처리 성공")
    else:
        print(f"❌ 처리 실패: {result.get('error', '알 수 없는 오류')}")
        return
    
    print(f"📊 표 개수: {result.get('table_count', 0)}개")
    print(f"🤖 사용 모델: {result.get('extraction_method', 'N/A')}")
    
    # 메타데이터
    if 'metadata' in result:
        print(f"⏰ 처리 시간: {result['metadata'].get('processed_at', 'N/A')}")
        print(f"🖼️ 소스 이미지: {result['metadata'].get('source_image', 'N/A')}")
    
    # 표들 표시
    tables = result.get("tables", [])
    if tables:
        print_subheader("📊 발견된 표")
        for i, table in enumerate(tables):
            display_table(table, i)
    
    # Markdown 형식
    markdown = result.get("markdown", "")
    if markdown:
        print_subheader("📝 Markdown 형식")
        print(markdown)
    
    # 요약 텍스트
    summary = result.get("summary", "")
    if summary:
        print_subheader("📄 요약")
        print(summary)

def list_available_files():
    """사용 가능한 파일 목록 출력"""
    data_dir = Path("data")
    result_dir = Path("result")
    
    print_header("📁 사용 가능한 파일")
    
    # 이미지 파일
    if data_dir.exists():
        png_files = list(data_dir.glob("*.png"))
        print(f"🖼️ 이미지 파일 ({len(png_files)}개):")
        for file in png_files:
            print(f"   • {file.name}")
    else:
        print("❌ data 폴더를 찾을 수 없습니다")
    
    print()
    
    # 결과 파일
    if result_dir.exists():
        result_files = list(result_dir.glob("*_result.json"))
        print(f"📋 결과 파일 ({len(result_files)}개):")
        for file in result_files:
            print(f"   • {file.name}")
    else:
        print("❌ result 폴더를 찾을 수 없습니다")

def view_result(image_name: str):
    """특정 이미지의 결과 보기"""
    if not image_name.endswith('.png'):
        image_name += '.png'
    
    result_filename = image_name.replace('.png', '_result.json')
    result_path = Path("result") / result_filename
    
    if not result_path.exists():
        print(f"❌ 결과 파일을 찾을 수 없습니다: {result_filename}")
        print("   이미지를 먼저 처리해주세요.")
        return
    
    try:
        with open(result_path, 'r', encoding='utf-8') as f:
            result = json.load(f)
        
        display_result(result)
        
    except Exception as e:
        print(f"❌ 결과 파일 읽기 오류: {e}")

def interactive_mode():
    """대화형 모드"""
    print_header("🎯 대화형 결과 뷰어")
    print("사용 가능한 명령:")
    print("  list    - 파일 목록 보기")
    print("  view    - 특정 이미지 결과 보기")
    print("  quit    - 종료")
    print()
    
    while True:
        try:
            command = input("명령 입력> ").strip().lower()
            
            if command == "quit" or command == "q":
                print("👋 안녕히 가세요!")
                break
            elif command == "list" or command == "l":
                list_available_files()
            elif command == "view" or command == "v":
                image_name = input("이미지 이름 입력 (예: sample1): ").strip()
                if image_name:
                    view_result(image_name)
                else:
                    print("❌ 이미지 이름을 입력해주세요")
            else:
                print("❌ 알 수 없는 명령입니다. 'list', 'view', 'quit' 중 하나를 입력하세요.")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 안녕히 가세요!")
            break
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def main():
    """메인 함수"""
    import sys
    
    if len(sys.argv) > 1:
        # 명령행 인수로 이미지 이름이 주어진 경우
        image_name = sys.argv[1]
        view_result(image_name)
    else:
        # 대화형 모드
        interactive_mode()

if __name__ == "__main__":
    main()
