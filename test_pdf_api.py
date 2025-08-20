#!/usr/bin/env python3
"""
PDF 분석 API 테스트 클라이언트
OpenAI의 새로운 PDF 입력 기능을 테스트합니다.
"""

import requests
import json
import os
from typing import Dict, Any

class PDFAnalysisClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health(self) -> Dict[str, Any]:
        """API 상태 확인"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "data": response.json() if response.status_code == 200 else response.text
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_pdf_direct(self, pdf_path: str, prompt: str = None) -> Dict[str, Any]:
        """
        PDF를 직접 Base64로 인코딩하여 분석
        
        Args:
            pdf_path: PDF 파일 경로
            prompt: 분석 요청 프롬프트 (선택사항)
        """
        try:
            if not os.path.exists(pdf_path):
                return {"success": False, "error": f"파일을 찾을 수 없습니다: {pdf_path}"}
            
            # 파일 크기 확인 (10MB 제한)
            file_size = os.path.getsize(pdf_path)
            if file_size > 10 * 1024 * 1024:
                return {"success": False, "error": "파일 크기가 10MB를 초과합니다."}
            
            # 파일 업로드
            with open(pdf_path, "rb") as f:
                files = {"file": (os.path.basename(pdf_path), f, "application/pdf")}
                data = {"prompt": prompt} if prompt else {}
                
                response = self.session.post(
                    f"{self.base_url}/analyze-pdf",
                    files=files,
                    data=data
                )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "data": response.json() if response.status_code == 200 else response.text
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        파일을 OpenAI Files API에 업로드
        
        Args:
            file_path: 업로드할 파일 경로
        """
        try:
            if not os.path.exists(file_path):
                return {"success": False, "error": f"파일을 찾을 수 없습니다: {file_path}"}
            
            # 파일 크기 확인 (10MB 제한)
            file_size = os.path.getsize(file_path)
            if file_size > 10 * 1024 * 1024:
                return {"success": False, "error": "파일 크기가 10MB를 초과합니다."}
            
            # 파일 업로드
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
                
                response = self.session.post(
                    f"{self.base_url}/upload-file",
                    files=files
                )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "data": response.json() if response.status_code == 200 else response.text
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_with_file_id(self, file_id: str, prompt: str = None) -> Dict[str, Any]:
        """
        파일 ID를 사용하여 파일 분석
        
        Args:
            file_id: OpenAI Files API의 파일 ID
            prompt: 분석 요청 프롬프트 (선택사항)
        """
        try:
            data = {"file_id": file_id}
            if prompt:
                data["prompt"] = prompt
            
            response = self.session.post(
                f"{self.base_url}/analyze-with-file-id",
                data=data
            )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "data": response.json() if response.status_code == 200 else response.text
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

def main():
    """메인 테스트 함수"""
    client = PDFAnalysisClient()
    
    print("=== PDF 분석 API 테스트 ===\n")
    
    # 1. API 상태 확인
    print("1. API 상태 확인...")
    health_result = client.test_health()
    if health_result["success"]:
        print(f"✅ API 상태: {health_result['data']}")
    else:
        print(f"❌ API 상태 확인 실패: {health_result['error']}")
        return
    
    print()
    
    # 2. PDF 파일 경로 입력 받기
    pdf_path = input("분석할 PDF 파일 경로를 입력하세요: ").strip()
    
    if not pdf_path:
        print("PDF 파일 경로가 입력되지 않았습니다.")
        return
    
    if not os.path.exists(pdf_path):
        print(f"파일을 찾을 수 없습니다: {pdf_path}")
        return
    
    print()
    
    # 3. 직접 분석 테스트
    print("2. PDF 직접 분석 테스트...")
    prompt = input("분석 프롬프트를 입력하세요 (기본값 사용하려면 Enter): ").strip()
    if not prompt:
        prompt = "이 PDF를 분석하고 주요 내용을 요약해주세요."
    
    direct_result = client.analyze_pdf_direct(pdf_path, prompt)
    if direct_result["success"]:
        print("✅ PDF 직접 분석 성공!")
        print(f"모델: {direct_result['data']['model']}")
        print(f"결과: {direct_result['data']['output_text'][:200]}...")
        if direct_result['data']['usage']:
            print(f"토큰 사용량: {direct_result['data']['usage']}")
    else:
        print(f"❌ PDF 직접 분석 실패: {direct_result['error']}")
    
    print()
    
    # 4. 파일 업로드 후 분석 테스트
    print("3. 파일 업로드 후 분석 테스트...")
    upload_result = client.upload_file(pdf_path)
    
    if upload_result["success"]:
        print("✅ 파일 업로드 성공!")
        file_id = upload_result["data"]["file_id"]
        print(f"파일 ID: {file_id}")
        
        # 업로드된 파일로 분석
        analysis_result = client.analyze_with_file_id(file_id, prompt)
        if analysis_result["success"]:
            print("✅ 파일 ID를 사용한 분석 성공!")
            print(f"모델: {analysis_result['data']['model']}")
            print(f"결과: {analysis_result['data']['output_text'][:200]}...")
            if analysis_result['data']['usage']:
                print(f"토큰 사용량: {analysis_result['data']['usage']}")
        else:
            print(f"❌ 파일 ID를 사용한 분석 실패: {analysis_result['error']}")
    else:
        print(f"❌ 파일 업로드 실패: {upload_result['error']}")
    
    print("\n=== 테스트 완료 ===")

if __name__ == "__main__":
    main()
