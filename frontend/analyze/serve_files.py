#!/usr/bin/env python3
"""
간단한 파일 서버 - 이미지와 결과 파일을 웹에서 접근할 수 있게 함
"""

import http.server
import socketserver
import os
from pathlib import Path
import json

class FileHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # API 엔드포인트 처리
        if self.path == '/api/images':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # 모든 이미지 파일 목록 반환
            data_dir = Path("data")
            if data_dir.exists():
                supported_formats = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp', '.gif']
                image_files = []
                for f in data_dir.iterdir():
                    if f.is_file() and f.suffix.lower() in supported_formats:
                        image_files.append({
                            "filename": f.name,
                            "size": f.stat().st_size,
                            "modified": f.stat().st_mtime
                        })
                # 수정 시간 기준으로 정렬 (최신순)
                image_files.sort(key=lambda x: x["modified"], reverse=True)
            else:
                image_files = []
            
            self.wfile.write(json.dumps(image_files).encode())
            return
        
        # 기본 파일 서빙
        super().do_GET()

def main():
    """메인 함수"""
    PORT = 8080
    
    # 현재 디렉토리를 analyze 폴더로 변경
    os.chdir(Path(__file__).parent)
    
    print(f"🚀 파일 서버 시작: http://0.0.0.0:{PORT}")
    print(f"📁 작업 디렉토리: {os.getcwd()}")
    print(f"🖼️ data 폴더: {Path('data').absolute()}")
    print(f"📋 result 폴더: {Path('result').absolute()}")
    print()
    print("사용법:")
    print(f"1. 브라우저에서 http://0.0.0.0:{PORT}/visualize_results.html 열기")
    print(f"2. 외부 접근: http://[서버IP]:{PORT}/visualize_results.html")
    print("3. Ctrl+C로 서버 종료")
    print()
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), FileHandler) as httpd:
            print(f"✅ 서버가 포트 {PORT}에서 실행 중입니다...")
            print(f"🌐 외부 접근: http://0.0.0.0:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 서버를 종료합니다.")
    except Exception as e:
        print(f"❌ 서버 오류: {e}")

if __name__ == "__main__":
    main()
