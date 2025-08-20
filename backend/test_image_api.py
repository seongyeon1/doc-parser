#!/usr/bin/env python3
"""
이미지 분석 및 생성 API 테스트 클라이언트
OpenAI의 최신 Vision API와 Image API를 테스트합니다.
"""

import requests
import json
import os
from typing import Dict, Any

class ImageAPIClient:
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
    
    def analyze_image_direct(self, image_path: str, prompt: str = None, detail: str = "auto") -> Dict[str, Any]:
        """
        이미지를 직접 업로드하여 분석
        
        Args:
            image_path: 이미지 파일 경로
            prompt: 분석 요청 프롬프트 (선택사항)
            detail: 이미지 분석 상세도 (low, high, auto)
        """
        try:
            if not os.path.exists(image_path):
                return {"success": False, "error": f"파일을 찾을 수 없습니다: {image_path}"}
            
            # 파일 크기 확인 (50MB 제한)
            file_size = os.path.getsize(image_path)
            if file_size > 50 * 1024 * 1024:
                return {"success": False, "error": "파일 크기가 50MB를 초과합니다."}
            
            # 이미지 업로드 및 분석
            with open(image_path, "rb") as f:
                files = {"file": (os.path.basename(image_path), f, "image/jpeg")}
                data = {}
                if prompt:
                    data["prompt"] = prompt
                if detail:
                    data["detail"] = detail
                
                response = self.session.post(
                    f"{self.base_url}/analyze-image",
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
    
    def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> Dict[str, Any]:
        """
        GPT Image 1을 사용하여 이미지 생성
        
        Args:
            prompt: 이미지 생성 프롬프트
            size: 이미지 크기
            quality: 이미지 품질
        """
        try:
            data = {
                "prompt": prompt,
                "size": size,
                "quality": quality
            }
            
            response = self.session.post(
                f"{self.base_url}/generate-image",
                data=data
            )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "data": response.json() if response.status_code == 200 else response.text
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def upload_image(self, image_path: str) -> Dict[str, Any]:
        """
        이미지를 OpenAI Files API에 업로드
        
        Args:
            image_path: 업로드할 이미지 파일 경로
        """
        try:
            if not os.path.exists(image_path):
                return {"success": False, "error": f"파일을 찾을 수 없습니다: {image_path}"}
            
            # 파일 크기 확인 (50MB 제한)
            file_size = os.path.getsize(image_path)
            if file_size > 50 * 1024 * 1024:
                return {"success": False, "error": "파일 크기가 50MB를 초과합니다."}
            
            # 이미지 업로드
            with open(image_path, "rb") as f:
                files = {"file": (os.path.basename(image_path), f, "image/jpeg")}
                
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
    
    def analyze_image_with_file_id(self, file_id: str, prompt: str = None, detail: str = "auto") -> Dict[str, Any]:
        """
        파일 ID를 사용하여 이미지 분석
        
        Args:
            file_id: OpenAI Files API의 파일 ID
            prompt: 분석 요청 프롬프트 (선택사항)
            detail: 이미지 분석 상세도 (low, high, auto)
        """
        try:
            data = {"file_id": file_id}
            if prompt:
                data["prompt"] = prompt
            if detail:
                data["detail"] = detail
            
            response = self.session.post(
                f"{self.base_url}/analyze-image-with-file-id",
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
    client = ImageAPIClient()
    
    print("=== 이미지 분석 및 생성 API 테스트 ===\n")
    
    # 1. API 상태 확인
    print("1. API 상태 확인...")
    health_result = client.test_health()
    if health_result["success"]:
        print(f"✅ API 상태: {health_result['data']}")
    else:
        print(f"❌ API 상태 확인 실패: {health_result['error']}")
        return
    
    print()
    
    # 2. 이미지 파일 경로 입력 받기
    image_path = input("분석할 이미지 파일 경로를 입력하세요: ").strip()
    
    if not image_path:
        print("이미지 파일 경로가 입력되지 않았습니다.")
        return
    
    if not os.path.exists(image_path):
        print(f"파일을 찾을 수 없습니다: {image_path}")
        return
    
    print()
    
    # 3. 이미지 직접 분석 테스트
    print("2. 이미지 직접 분석 테스트...")
    prompt = input("분석 프롬프트를 입력하세요 (기본값 사용하려면 Enter): ").strip()
    if not prompt:
        prompt = "이 이미지를 분석하고 주요 내용을 설명해주세요."
    
    detail = input("분석 상세도를 입력하세요 (low/high/auto, 기본값: auto): ").strip()
    if detail not in ["low", "high", "auto"]:
        detail = "auto"
    
    direct_result = client.analyze_image_direct(image_path, prompt, detail)
    if direct_result["success"]:
        print("✅ 이미지 직접 분석 성공!")
        print(f"모델: {direct_result['data']['model']}")
        print(f"결과: {direct_result['data']['output_text']}")
        if direct_result['data']['usage']:
            print(f"토큰 사용량: {direct_result['data']['usage']}")
    else:
        print(f"❌ 이미지 직접 분석 실패: {direct_result['error']}")
    
    print()
    
    # 4. 이미지 업로드 후 분석 테스트
    print("3. 이미지 업로드 후 분석 테스트...")
    upload_result = client.upload_image(image_path)
    
    if upload_result["success"]:
        print("✅ 이미지 업로드 성공!")
        file_id = upload_result["data"]["file_id"]
        print(f"파일 ID: {file_id}")
        
        # 업로드된 이미지로 분석
        analysis_result = client.analyze_image_with_file_id(file_id, prompt, detail)
        if analysis_result["success"]:
            print("✅ 파일 ID를 사용한 이미지 분석 성공!")
            print(f"모델: {analysis_result['data']['model']}")
            print(f"결과: {analysis_result['data']['output_text']}")
            if analysis_result['data']['usage']:
                print(f"토큰 사용량: {analysis_result['data']['usage']}")
        else:
            print(f"❌ 파일 ID를 사용한 이미지 분석 실패: {analysis_result['error']}")
    else:
        print(f"❌ 이미지 업로드 실패: {upload_result['error']}")
    
    print()
    
    # 5. 이미지 생성 테스트
    print("4. 이미지 생성 테스트...")
    generate_prompt = input("생성할 이미지에 대한 프롬프트를 입력하세요: ").strip()
    
    if generate_prompt:
        size = input("이미지 크기를 입력하세요 (1024x1024/1792x1024/1024x1792, 기본값: 1024x1024): ").strip()
        if size not in ["1024x1024", "1792x1024", "1024x1792"]:
            size = "1024x1024"
        
        quality = input("이미지 품질을 입력하세요 (standard/hd, 기본값: standard): ").strip()
        if quality not in ["standard", "hd"]:
            quality = "standard"
        
        generate_result = client.generate_image(generate_prompt, size, quality)
        if generate_result["success"]:
            print("✅ 이미지 생성 성공!")
            print(f"모델: {generate_result['data']['model']}")
            print(f"이미지 URL: {generate_result['data']['image_url']}")
            if generate_result['data']['revised_prompt']:
                print(f"수정된 프롬프트: {generate_result['data']['revised_prompt']}")
        else:
            print(f"❌ 이미지 생성 실패: {generate_result['error']}")
    else:
        print("이미지 생성 테스트를 건너뜁니다.")
    
    print("\n=== 테스트 완료 ===")

if __name__ == "__main__":
    main()
