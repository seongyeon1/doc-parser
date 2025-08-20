#!/usr/bin/env python3
"""
analyze 폴더의 데이터를 처리하는 스크립트
PNG 이미지에서 표를 추출하고 결과를 JSON으로 저장
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
import time
from datetime import datetime

class AnalyzeDataProcessor:
    """analyze 폴더의 데이터를 처리하는 클래스"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.data_dir = Path("data")
        self.result_dir = Path("result")
        
        # 디렉토리 생성
        self.data_dir.mkdir(exist_ok=True)
        self.result_dir.mkdir(exist_ok=True)
    
    def process_single_image(self, image_path: Path, model: str = None) -> Dict[str, Any]:
        """
        단일 이미지를 처리하여 표를 추출합니다.
        
        Args:
            image_path: 처리할 이미지 파일 경로
            model: 사용할 모델명 (선택사항)
            
        Returns:
            API 응답 결과
        """
        try:
            print(f"처리 중: {image_path.name}")
            
            # 이미지 파일 읽기
            with open(image_path, 'rb') as f:
                files = {'file': (image_path.name, f, 'image/png')}
                data = {}
                
                if model:
                    data['model'] = model
                
                # API 호출
                response = requests.post(
                    f"{self.api_url}/extract-tables",
                    files=files,
                    data=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ 성공: {result.get('table_count', 0)}개 표 발견")
                    return result
                else:
                    print(f"❌ 오류: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": f"API 오류: {response.status_code}",
                        "tables": [],
                        "markdown": "",
                        "summary": ""
                    }
                    
        except Exception as e:
            print(f"❌ 처리 중 오류 발생: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tables": [],
                "markdown": "",
                "summary": ""
            }
    
    def save_result(self, result: Dict[str, Any], image_name: str) -> Path:
        """
        결과를 JSON 파일로 저장합니다.
        
        Args:
            result: 저장할 결과 데이터
            image_name: 원본 이미지 파일명
            
        Returns:
            저장된 파일 경로
        """
        # 파일명에서 확장자 제거
        base_name = Path(image_name).stem
        
        # 결과 파일명 생성
        result_filename = f"{base_name}_result.json"
        result_path = self.result_dir / result_filename
        
        # 결과에 메타데이터 추가
        result_with_meta = {
            **result,
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "source_image": image_name,
                "api_url": self.api_url
            }
        }
        
        # JSON 파일로 저장
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result_with_meta, f, ensure_ascii=False, indent=2)
        
        print(f"💾 결과 저장: {result_path}")
        return result_path
    
    def process_all_images(self, model: str = None, delay: float = 1.0) -> List[Dict[str, Any]]:
        """
        data 폴더의 모든 PNG 이미지를 처리합니다.
        
        Args:
            model: 사용할 모델명 (선택사항)
            delay: API 호출 간 지연 시간 (초)
            
        Returns:
            모든 처리 결과 리스트
        """
        # PNG 이미지 파일 찾기
        png_files = list(self.data_dir.glob("*.png"))
        
        if not png_files:
            print("⚠️ data 폴더에 PNG 파일이 없습니다.")
            return []
        
        print(f"🔍 {len(png_files)}개의 PNG 파일 발견")
        print("=" * 50)
        
        results = []
        
        for i, png_file in enumerate(png_files, 1):
            print(f"\n[{i}/{len(png_files)}] {png_file.name}")
            
            # 이미지 처리
            result = self.process_single_image(png_file, model)
            
            # 결과 저장
            if result.get("success"):
                self.save_result(result, png_file.name)
            
            results.append(result)
            
            # API 호출 간 지연 (rate limiting 방지)
            if i < len(png_files) and delay > 0:
                print(f"⏳ {delay}초 대기...")
                time.sleep(delay)
        
        return results
    
    def generate_summary_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        모든 처리 결과를 요약한 리포트를 생성합니다.
        
        Args:
            results: 처리 결과 리스트
            
        Returns:
            요약 리포트
        """
        total_images = len(results)
        successful_images = sum(1 for r in results if r.get("success"))
        failed_images = total_images - successful_images
        
        total_tables = sum(r.get("table_count", 0) for r in results if r.get("success"))
        
        # 성공한 이미지들의 표 정보 수집
        table_info = []
        for result in results:
            if result.get("success") and result.get("tables"):
                for table in result.get("tables", []):
                    table_info.append({
                        "source": result.get("metadata", {}).get("source_image", "unknown"),
                        "title": table.get("title", "제목 없음"),
                        "rows": table.get("row_count", 0),
                        "columns": table.get("column_count", 0)
                    })
        
        summary = {
            "summary": {
                "total_images": total_images,
                "successful_images": successful_images,
                "failed_images": failed_images,
                "total_tables": total_tables,
                "success_rate": f"{(successful_images/total_images*100):.1f}%" if total_images > 0 else "0%"
            },
            "table_details": table_info,
            "processed_at": datetime.now().isoformat()
        }
        
        return summary
    
    def save_summary_report(self, summary: Dict[str, Any]) -> Path:
        """
        요약 리포트를 JSON 파일로 저장합니다.
        
        Args:
            summary: 저장할 요약 리포트
            
        Returns:
            저장된 파일 경로
        """
        report_path = self.result_dir / "summary_report.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"📊 요약 리포트 저장: {report_path}")
        return report_path
    
    def check_api_health(self) -> bool:
        """
        API 서버의 상태를 확인합니다.
        
        Returns:
            API가 정상인지 여부
        """
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ API 서버 정상: {result.get('status', 'unknown')}")
                print(f"📋 기본 모델: {result.get('model', 'unknown')}")
                return True
            else:
                print(f"❌ API 서버 오류: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API 서버 연결 실패: {str(e)}")
            return False
    
    def process_with_retry(self, max_retries: int = 3, delay: float = 1.0) -> List[Dict[str, Any]]:
        """
        재시도 로직을 포함하여 이미지를 처리합니다.
        
        Args:
            max_retries: 최대 재시도 횟수
            delay: 재시도 간 지연 시간 (초)
            
        Returns:
            모든 처리 결과 리스트
        """
        print("🚀 analyze 폴더 데이터 처리 시작")
        print("=" * 50)
        
        # API 상태 확인
        if not self.check_api_health():
            print("❌ API 서버가 정상이 아닙니다. 서버를 시작해주세요.")
            return []
        
        # 모든 이미지 처리
        results = self.process_all_images(delay=delay)
        
        # 요약 리포트 생성 및 저장
        if results:
            summary = self.generate_summary_report(results)
            self.save_summary_report(summary)
            
            # 콘솔에 요약 출력
            print("\n" + "=" * 50)
            print("📊 처리 완료 요약")
            print(f"총 이미지: {summary['summary']['total_images']}")
            print(f"성공: {summary['summary']['successful_images']}")
            print(f"실패: {summary['summary']['failed_images']}")
            print(f"총 표: {summary['summary']['total_tables']}")
            print(f"성공률: {summary['summary']['success_rate']}")
        
        return results


def main():
    """메인 실행 함수"""
    # 현재 작업 디렉토리를 analyze 폴더로 변경
    analyze_dir = Path("analyze")
    if analyze_dir.exists():
        os.chdir(analyze_dir)
        print(f"📁 작업 디렉토리 변경: {os.getcwd()}")
    else:
        print("⚠️ analyze 폴더를 찾을 수 없습니다.")
        return
    
    # 프로세서 초기화
    processor = AnalyzeDataProcessor()
    
    # 이미지 처리 실행
    results = processor.process_with_retry(delay=1.0)
    
    if results:
        print(f"\n🎉 모든 처리 완료! {len(results)}개 파일 처리됨")
    else:
        print("\n❌ 처리할 파일이 없거나 오류가 발생했습니다.")


if __name__ == "__main__":
    main()
