#!/usr/bin/env python3
"""
결과와 이미지를 양쪽으로 비교할 수 있는 Python 시각화 스크립트
"""

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from pathlib import Path
import webbrowser
from typing import Dict, List, Any, Optional

class ResultsVisualizer:
    """결과와 이미지를 비교하는 시각화 도구"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📊 표 추출 결과 시각화")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        # 데이터 경로
        self.data_dir = Path("data")
        self.result_dir = Path("result")
        
        # 현재 선택된 이미지와 결과
        self.current_image = None
        self.current_result = None
        
        # 이미지 파일 목록
        self.image_files = []
        self.result_files = []
        
        self.setup_ui()
        self.load_file_lists()
        
    def setup_ui(self):
        """UI 구성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 제목
        title_label = ttk.Label(
            main_frame, 
            text="📊 표 추출 결과 시각화", 
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # 컨트롤 프레임
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 이미지 선택
        ttk.Label(control_frame, text="이미지 선택:").pack(side=tk.LEFT, padx=(0, 10))
        self.image_var = tk.StringVar()
        self.image_combo = ttk.Combobox(
            control_frame, 
            textvariable=self.image_var,
            width=30,
            state="readonly"
        )
        self.image_combo.pack(side=tk.LEFT, padx=(0, 20))
        self.image_combo.bind('<<ComboboxSelected>>', self.on_image_selected)
        
        # 결과 로드 버튼
        ttk.Button(
            control_frame, 
            text="결과 로드", 
            command=self.load_result
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        # HTML 열기 버튼
        ttk.Button(
            control_frame, 
            text="HTML 뷰어 열기", 
            command=self.open_html_viewer
        ).pack(side=tk.LEFT)
        
        # 메인 비교 프레임
        comparison_frame = ttk.Frame(main_frame)
        comparison_frame.pack(fill=tk.BOTH, expand=True)
        
        # 왼쪽 패널 (이미지)
        left_frame = ttk.LabelFrame(comparison_frame, text="🖼️ 원본 이미지", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.image_label = ttk.Label(left_frame, text="이미지를 선택하세요")
        self.image_label.pack(expand=True)
        
        # 오른쪽 패널 (결과)
        right_frame = ttk.LabelFrame(comparison_frame, text="📋 추출된 표", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 결과 표시를 위한 텍스트 위젯
        self.result_text = tk.Text(right_frame, wrap=tk.WORD, font=("Consolas", 10))
        result_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 상태바
        self.status_var = tk.StringVar()
        self.status_var.set("준비됨")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def load_file_lists(self):
        """파일 목록 로드"""
        try:
            # 이미지 파일 목록
            if self.data_dir.exists():
                self.image_files = [f.name for f in self.data_dir.glob("*.png")]
            else:
                self.image_files = []
            
            # 결과 파일 목록
            if self.result_dir.exists():
                self.result_files = [f.name for f in self.result_dir.glob("*_result.json")]
            else:
                self.result_files = []
            
            # 이미지 콤보박스 업데이트
            self.image_combo['values'] = [''] + self.image_files
            
            self.status_var.set(f"로드됨: {len(self.image_files)}개 이미지, {len(self.result_files)}개 결과")
            
        except Exception as e:
            self.status_var.set(f"파일 로드 오류: {str(e)}")
    
    def on_image_selected(self, event):
        """이미지 선택 시 호출"""
        selected_image = self.image_var.get()
        if selected_image:
            self.display_image(selected_image)
            self.status_var.set(f"선택됨: {selected_image}")
        else:
            self.image_label.configure(text="이미지를 선택하세요")
            self.status_var.set("준비됨")
    
    def display_image(self, image_name: str):
        """이미지 표시"""
        try:
            image_path = self.data_dir / image_name
            if image_path.exists():
                # 이미지 로드 및 리사이즈
                image = Image.open(image_path)
                
                # 최대 크기 계산 (패널 크기에 맞춤)
                max_width = 600
                max_height = 400
                
                # 비율 유지하며 리사이즈
                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # PhotoImage로 변환
                photo = ImageTk.PhotoImage(image)
                
                # 이미지 표시
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # 참조 유지
                
                self.current_image = image_name
                
            else:
                self.image_label.configure(
                    text=f"이미지를 찾을 수 없습니다:\n{image_name}",
                    image=""
                )
                self.current_image = None
                
        except Exception as e:
            self.image_label.configure(
                text=f"이미지 로드 오류:\n{str(e)}",
                image=""
            )
            self.current_image = None
    
    def load_result(self):
        """결과 파일 로드"""
        if not self.current_image:
            messagebox.showwarning("경고", "먼저 이미지를 선택해주세요.")
            return
        
        try:
            # 결과 파일 경로
            result_filename = self.current_image.replace('.png', '_result.json')
            result_path = self.result_dir / result_filename
            
            if result_path.exists():
                with open(result_path, 'r', encoding='utf-8') as f:
                    self.current_result = json.load(f)
                
                self.display_result()
                self.status_var.set(f"결과 로드됨: {result_filename}")
                
            else:
                messagebox.showinfo(
                    "정보", 
                    f"결과 파일을 찾을 수 없습니다:\n{result_filename}\n\n이미지를 먼저 처리해주세요."
                )
                self.status_var.set("결과 파일 없음")
                
        except Exception as e:
            messagebox.showerror("오류", f"결과 로드 중 오류 발생:\n{str(e)}")
            self.status_var.set("결과 로드 오류")
    
    def display_result(self):
        """결과 표시"""
        if not self.current_result:
            return
        
        # 텍스트 위젯 초기화
        self.result_text.delete(1.0, tk.END)
        
        result = self.current_result
        
        # 제목
        self.result_text.insert(tk.END, "📊 표 추출 결과\n", "title")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # 성공 여부
        if result.get("success"):
            self.result_text.insert(tk.END, "✅ 처리 성공\n\n", "success")
        else:
            self.result_text.insert(tk.END, f"❌ 처리 실패: {result.get('error', '알 수 없는 오류')}\n\n", "error")
            return
        
        # 요약 정보
        self.result_text.insert(tk.END, "📋 요약 정보\n", "subtitle")
        self.result_text.insert(tk.END, f"• 표 개수: {result.get('table_count', 0)}개\n")
        self.result_text.insert(tk.END, f"• 사용 모델: {result.get('extraction_method', 'N/A')}\n")
        if 'metadata' in result:
            self.result_text.insert(tk.END, f"• 처리 시간: {result['metadata'].get('processed_at', 'N/A')}\n")
        self.result_text.insert(tk.END, "\n")
        
        # 표들 표시
        tables = result.get("tables", [])
        if tables:
            self.result_text.insert(tk.END, f"📊 발견된 표 ({len(tables)}개)\n", "subtitle")
            self.result_text.insert(tk.END, "=" * 30 + "\n\n")
            
            for i, table in enumerate(tables, 1):
                self.result_text.insert(tk.END, f"표 {i}: {table.get('title', '제목 없음')}\n", "table_title")
                self.result_text.insert(tk.END, f"행: {table.get('row_count', 0)}, 열: {table.get('column_count', 0)}\n\n")
                
                # 헤더
                headers = table.get("headers", [])
                if headers:
                    self.result_text.insert(tk.END, "헤더:\n")
                    for j, header in enumerate(headers):
                        self.result_text.insert(tk.END, f"  {j+1}. {header}\n")
                    self.result_text.insert(tk.END, "\n")
                
                # 데이터 행
                rows = table.get("rows", [])
                if rows:
                    self.result_text.insert(tk.END, "데이터:\n")
                    for j, row in enumerate(rows):
                        row_str = " | ".join(str(cell) for cell in row)
                        self.result_text.insert(tk.END, f"  {j+1}. {row_str}\n")
                    self.result_text.insert(tk.END, "\n")
                
                self.result_text.insert(tk.END, "-" * 30 + "\n\n")
        
        # Markdown 형식
        markdown = result.get("markdown", "")
        if markdown:
            self.result_text.insert(tk.END, "📝 Markdown 형식\n", "subtitle")
            self.result_text.insert(tk.END, "=" * 30 + "\n\n")
            self.result_text.insert(tk.END, markdown + "\n\n")
        
        # 요약 텍스트
        summary = result.get("summary", "")
        if summary:
            self.result_text.insert(tk.END, "📄 요약 텍스트\n", "subtitle")
            self.result_text.insert(tk.END, "=" * 30 + "\n\n")
            self.result_text.insert(tk.END, summary + "\n\n")
        
        # 태그 설정
        self.result_text.tag_configure("title", font=("Arial", 14, "bold"), foreground="blue")
        self.result_text.tag_configure("subtitle", font=("Arial", 12, "bold"), foreground="darkgreen")
        self.result_text.tag_configure("table_title", font=("Arial", 11, "bold"), foreground="purple")
        self.result_text.tag_configure("success", font=("Arial", 10, "bold"), foreground="green")
        self.result_text.tag_configure("error", font=("Arial", 10, "bold"), foreground="red")
        
        # 스크롤을 맨 위로
        self.result_text.see("1.0")
    
    def open_html_viewer(self):
        """HTML 뷰어 열기"""
        html_path = Path("visualize_results.html")
        if html_path.exists():
            try:
                # 기본 브라우저로 HTML 파일 열기
                webbrowser.open(f"file://{html_path.absolute()}")
                self.status_var.set("HTML 뷰어가 브라우저에서 열렸습니다")
            except Exception as e:
                messagebox.showerror("오류", f"HTML 뷰어 열기 실패:\n{str(e)}")
        else:
            messagebox.showwarning("경고", "HTML 파일을 찾을 수 없습니다:\nvisualize_results.html")
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()

def main():
    """메인 함수"""
    try:
        app = ResultsVisualizer()
        app.run()
    except Exception as e:
        print(f"애플리케이션 실행 오류: {e}")

if __name__ == "__main__":
    main()
