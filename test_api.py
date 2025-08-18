import requests
import json
import os

def test_api_health():
    """API 상태 확인 테스트"""
    try:
        response = requests.get("http://localhost:8000/health")
        print("Health Check 결과:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return True
    except Exception as e:
        print(f"Health Check 실패: {e}")
        return False

def test_table_extraction(file_path):
    """표 추출 API 테스트"""
    if not os.path.exists(file_path):
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return False
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'application/octet-stream')}
            
            print(f"파일 업로드 중: {file_path}")
            print(f"파일 크기: {os.path.getsize(file_path) / 1024:.2f} KB")
            
            response = requests.post("http://localhost:8000/extract-tables", files=files)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("표 추출 성공!")
                print(f"추출 방법: {result.get('extraction_method', 'N/A')}")
                print(f"발견된 표 개수: {result.get('table_count', 0)}")
                print(f"요약: {result.get('summary', 'N/A')}")
                
                # 표 데이터 출력
                tables = result.get('tables', [])
                for i, table in enumerate(tables):
                    print(f"\n표 {i+1}:")
                    print(f"  제목: {table.get('title', 'N/A')}")
                    print(f"  행 수: {table.get('row_count', 'N/A')}")
                    print(f"  열 수: {table.get('column_count', 'N/A')}")
                    
                    # 헤더 출력
                    if "headers" in table and table["headers"]:
                        print(f"  헤더: {table['headers']}")
                    
                    # 첫 몇 행 출력 (데이터가 많을 경우)
                    if "rows" in table and table["rows"]:
                        print(f"  첫 3행 데이터:")
                        for j, row in enumerate(table["rows"][:3]):
                            print(f"    행 {j+1}: {row}")
                        if len(table["rows"]) > 3:
                            print(f"    ... (총 {len(table['rows'])}행)")
                
                # Markdown 출력 (첫 500자만)
                markdown = result.get('markdown', '')
                if markdown:
                    print(f"\nMarkdown (첫 500자):")
                    print(markdown[:500] + "..." if len(markdown) > 500 else markdown)
                
                return True
            else:
                print(f"API 오류: {response.text}")
                return False
                
    except Exception as e:
        print(f"표 추출 테스트 실패: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("Table Extraction API 테스트 시작")
    print("GPT-4o Vision API를 사용한 표 추출 테스트")
    print("=" * 60)
    
    # 1. API 상태 확인
    if not test_api_health():
        print("API 서버가 실행되지 않았습니다. 먼저 서버를 실행하세요.")
        print("실행 명령어: python main.py")
        return
    
    # 2. 표 추출 테스트
    print("\n표 추출 테스트를 위해 테스트 파일 경로를 입력하세요:")
    print("지원 형식: PDF, DOCX, XLSX, XLS, PNG, JPG, JPEG, TIFF, BMP, WebP, GIF")
    print("(예: test_document.pdf, sample.xlsx, table_image.png 등)")
    
    file_path = input("\n파일 경로: ").strip()
    
    if file_path:
        print(f"\n{'='*60}")
        test_table_extraction(file_path)
    else:
        print("파일 경로가 입력되지 않았습니다.")

if __name__ == "__main__":
    main()
