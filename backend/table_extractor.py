import json
import openai
from typing import Dict, List, Any, Optional
import os
import base64

class TableExtractor:
    """GPT-4o Vision을 사용하여 텍스트와 이미지에서 표를 추출하고 정리하는 클래스"""
    
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def extract_tables_with_gpt5(self, text: str, model: str = None) -> Dict[str, Any]:
        """
        지정된 모델을 사용하여 텍스트에서 표를 추출하고 JSON과 Markdown으로 정리합니다.
        
        Args:
            text: 추출된 텍스트
            model: 사용할 모델명 (선택사항, 기본값: 클래스 초기화 시 설정된 모델)
            
        Returns:
            표 정보가 포함된 JSON 응답
        """
        try:
            # 사용할 모델 결정
            selected_model = model or self.model
            
            # 프롬프트 구성
            prompt = self._create_extraction_prompt(text)
            
            # OpenAI API 호출
            response = await self._call_openai_api(prompt, selected_model)
            
            # 응답 파싱 및 정리
            result = self._parse_and_clean_response(response, selected_model)
            
            return result
            
        except Exception as e:
            print(f"표 추출 중 오류 발생: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tables": [],
                "markdown": "",
                "summary": ""
            }
    
    async def extract_tables_from_image(self, image_content: bytes, file_extension: str, model: str = None) -> Dict[str, Any]:
        """
        지정된 Vision 모델을 사용하여 이미지에서 직접 표를 추출합니다.
        
        Args:
            image_content: 이미지 바이트 내용
            file_extension: 파일 확장자
            model: 사용할 Vision 모델명 (선택사항, 기본값: 클래스 초기화 시 설정된 모델)
            
        Returns:
            표 정보가 포함된 JSON 응답
        """
        try:
            # 사용할 모델 결정 (Vision API 지원 모델만 사용)
            selected_model = model or self.model
            
            # Vision API 지원 모델인지 확인
            vision_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-vision-preview"]
            if selected_model not in vision_models:
                print(f"경고: {selected_model}은 Vision API를 지원하지 않습니다. gpt-4o를 사용합니다.")
                selected_model = "gpt-4o"
            
            # 이미지를 Base64로 인코딩
            base64_image = base64.b64encode(image_content).decode('utf-8')
            
            # Vision API를 사용한 표 추출
            response = self.client.chat.completions.create(
                model=selected_model,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 이미지에서 표를 정확하게 추출하고 정리하는 전문가입니다. JSON 형식을 엄격하게 지켜주세요."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self._create_image_extraction_prompt()
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{file_extension[1:]};base64,{base64_image}",
                                    "detail": "high"  # 고해상도 분석으로 표 구조 정확히 파악
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4000,
                temperature=0.1
            )
            
            # 응답 파싱 및 정리
            result = self._parse_and_clean_response(response.choices[0].message.content, selected_model)
            
            return result
            
        except Exception as e:
            print(f"이미지 표 추출 중 오류 발생: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tables": [],
                "markdown": "",
                "summary": ""
            }
    
    def _create_extraction_prompt(self, text: str) -> str:
        """텍스트에서 표 추출을 위한 프롬프트를 생성합니다."""
        prompt = f"""
다음 텍스트에서 표를 찾아서 추출하고 정리해주세요.

텍스트:
{text[:4000]}  # 텍스트가 너무 길면 처음 4000자만 사용

다음 형식으로 JSON 응답을 제공해주세요:

{{
    "tables": [
        {{
            "table_id": "table_1",
            "title": "표 제목 또는 설명",
            "headers": ["열1", "열2", "열3"],
            "rows": [
                ["행1열1", "행1열2", "행1열3"],
                ["행2열1", "행2열2", "행2열3"]
            ],
            "row_count": 2,
            "column_count": 3
        }}
    ],
    "markdown": "표를 Markdown 형식으로 정리한 내용",
    "summary": "발견된 표들의 요약 정보 (개수, 주요 내용 등)"
}}

주의사항:
1. 표가 없는 경우 빈 배열을 반환하세요
2. 표의 구조를 정확히 파악하여 헤더와 데이터를 구분하세요
3. Markdown 형식은 표준 테이블 문법을 사용하세요
4. 한국어와 영어가 혼재되어 있을 수 있습니다
5. JSON 형식을 정확히 지켜주세요
"""
        return prompt
    
    def _create_image_extraction_prompt(self) -> str:
        """이미지에서 표 추출을 위한 프롬프트를 생성합니다."""
        prompt = """
이 이미지를 분석하여 표를 찾아서 추출하고 정리해주세요.

다음 형식으로 JSON 응답을 제공해주세요:

{
    "tables": [
        {
            "table_id": "table_1",
            "title": "표 제목 또는 설명",
            "headers": ["열1", "열2", "열3"],
            "rows": [
                ["행1열1", "행1열2", "행1열3"],
                ["행2열1", "행2열2", "행2열3"]
            ],
            "row_count": 2,
            "column_count": 3
        }
    ],
    "markdown": "표를 Markdown 형식으로 정리한 내용",
    "summary": "발견된 표들의 요약 정보 (개수, 주요 내용 등)"
}

주의사항:
1. 이미지에서 표가 보이지 않는 경우 빈 배열을 반환하세요
2. 표의 구조를 정확히 파악하여 헤더와 데이터를 구분하세요
3. 표의 경계선, 셀 구분을 주의 깊게 분석하세요
4. Markdown 형식은 표준 테이블 문법을 사용하세요
5. 한국어와 영어가 혼재되어 있을 수 있습니다
6. JSON 형식을 정확히 지켜주세요
7. 이미지의 해상도와 품질을 고려하여 가능한 한 정확하게 추출하세요
"""
        return prompt
    
    async def _call_openai_api(self, prompt: str, model: str = None) -> str:
        """OpenAI API를 호출합니다."""
        try:
            # 사용할 모델 결정
            selected_model = model or self.model
            
            response = self.client.chat.completions.create(
                model=selected_model,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 문서에서 표를 정확하게 추출하고 정리하는 전문가입니다. JSON 형식을 엄격하게 지켜주세요."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # 일관된 결과를 위해 낮은 temperature 사용
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"OpenAI API 호출 실패: {str(e)}")
    
    def _parse_and_clean_response(self, response: str, model: str = None) -> Dict[str, Any]:
        """GPT 응답을 파싱하고 정리합니다."""
        try:
            # 사용할 모델 결정
            selected_model = model or self.model
            
            # JSON 부분 추출 (```json``` 블록이 있는 경우)
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                json_str = response[start:end].strip()
            else:
                # JSON 블록이 없는 경우 전체 응답에서 JSON 찾기
                json_str = response.strip()
            
            # JSON 파싱
            parsed_data = json.loads(json_str)
            
            # 응답 구조 검증 및 정리
            result = {
                "success": True,
                "tables": parsed_data.get("tables", []),
                "markdown": parsed_data.get("markdown", ""),
                "summary": parsed_data.get("summary", ""),
                "table_count": len(parsed_data.get("tables", [])),
                "extraction_method": f"OpenAI API ({selected_model})"
            }
            
            # 표 데이터 검증
            for table in result["tables"]:
                if "rows" in table and table["rows"]:
                    table["row_count"] = len(table["rows"])
                    if table["rows"]:
                        table["column_count"] = len(table["rows"][0])
                
                # 표 ID가 없는 경우 생성
                if "table_id" not in table:
                    table["table_id"] = f"table_{len(result['tables'])}"
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {str(e)}")
            # JSON 파싱 실패 시 기본 응답 반환
            return {
                "success": False,
                "error": f"JSON 파싱 실패: {str(e)}",
                "raw_response": response,
                "tables": [],
                "markdown": "",
                "summary": ""
            }
        except Exception as e:
            print(f"응답 정리 중 오류: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "raw_response": response,
                "tables": [],
                "markdown": "",
                "summary": ""
            }
    
    def generate_markdown_from_tables(self, tables: List[Dict[str, Any]]) -> str:
        """표 데이터를 Markdown 형식으로 변환합니다."""
        if not tables:
            return "표가 발견되지 않았습니다."
        
        markdown = "# 추출된 표 목록\n\n"
        
        for i, table in enumerate(tables):
            markdown += f"## 표 {i+1}: {table.get('title', '제목 없음')}\n\n"
            
            if "headers" in table and table["headers"]:
                # 헤더 행
                markdown += "| " + " | ".join(table["headers"]) + " |\n"
                markdown += "| " + " | ".join(["---"] * len(table["headers"])) + " |\n"
                
                # 데이터 행
                if "rows" in table and table["rows"]:
                    for row in table["rows"]:
                        markdown += "| " + " | ".join(str(cell) for cell in row) + " |\n"
                
                markdown += f"\n**행 수**: {table.get('row_count', 'N/A')} | **열 수**: {table.get('column_count', 'N/A')}\n\n"
            else:
                markdown += "표 구조를 파악할 수 없습니다.\n\n"
            
            markdown += "---\n\n"
        
        return markdown
