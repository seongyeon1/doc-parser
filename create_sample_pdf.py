#!/usr/bin/env python3
"""
테스트용 샘플 PDF 파일을 생성하는 스크립트
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_sample_pdf(filename="sample_document.pdf"):
    """샘플 PDF 문서를 생성합니다."""
    
    # PDF 문서 생성
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # 스토리 (문서 내용)
    story = []
    
    # 제목
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # 중앙 정렬
    )
    title = Paragraph("샘플 문서 분석 테스트", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    # 소개
    intro_text = """
    이 문서는 OpenAI PDF 분석 API를 테스트하기 위한 샘플 문서입니다.
    다양한 내용과 표를 포함하고 있어 API의 기능을 충분히 테스트할 수 있습니다.
    """
    intro = Paragraph(intro_text, styles['Normal'])
    story.append(intro)
    story.append(Spacer(1, 20))
    
    # 표 1: 회사 정보
    company_data = [
        ['회사명', '설립연도', '직원수', '매출액'],
        ['테크솔루션즈', '2010', '150명', '50억원'],
        ['인노베이션랩', '2015', '80명', '25억원'],
        ['퓨처시스템', '2018', '200명', '75억원'],
        ['넥스트젠', '2020', '120명', '40억원']
    ]
    
    company_table = Table(company_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    company_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(Paragraph("회사 정보", styles['Heading2']))
    story.append(company_table)
    story.append(Spacer(1, 20))
    
    # 표 2: 프로젝트 현황
    project_data = [
        ['프로젝트명', '담당자', '진행률', '완료예정일', '상태'],
        ['웹사이트 리뉴얼', '김개발', '85%', '2024-03-15', '진행중'],
        ['모바일 앱 개발', '이디자인', '60%', '2024-04-20', '진행중'],
        ['데이터베이스 마이그레이션', '박데이터', '100%', '2024-02-28', '완료'],
        ['보안 시스템 구축', '최보안', '45%', '2024-05-10', '진행중']
    ]
    
    project_table = Table(project_data, colWidths=[2*inch, 1.2*inch, 1*inch, 1.5*inch, 1.2*inch])
    project_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(Paragraph("프로젝트 현황", styles['Heading2']))
    story.append(project_table)
    story.append(Spacer(1, 20))
    
    # 표 3: 월별 실적
    performance_data = [
        ['월', '매출액', '비용', '순이익', '성장률'],
        ['1월', '8.5억원', '6.2억원', '2.3억원', '+15%'],
        ['2월', '9.2억원', '6.8억원', '2.4억원', '+4%'],
        ['3월', '10.1억원', '7.1억원', '3.0억원', '+25%'],
        ['4월', '9.8억원', '7.0억원', '2.8억원', '-7%'],
        ['5월', '11.2억원', '7.5억원', '3.7억원', '+32%']
    ]
    
    performance_table = Table(performance_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
    performance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(Paragraph("월별 실적", styles['Heading2']))
    story.append(performance_table)
    story.append(Spacer(1, 20))
    
    # 결론
    conclusion_text = """
    이 샘플 문서는 다음과 같은 내용을 포함하고 있습니다:
    
    • 회사 정보 및 현황
    • 프로젝트 진행 상황
    • 월별 실적 데이터
    
    OpenAI PDF 분석 API는 이러한 복잡한 문서 구조를 이해하고 
    요청된 정보를 정확하게 추출할 수 있습니다.
    """
    conclusion = Paragraph(conclusion_text, styles['Normal'])
    story.append(conclusion)
    
    # PDF 생성
    doc.build(story)
    print(f"샘플 PDF 파일이 생성되었습니다: {filename}")

if __name__ == "__main__":
    create_sample_pdf()
    print("테스트용 샘플 PDF 생성이 완료되었습니다.")
    print("이 파일을 사용하여 PDF 분석 API를 테스트할 수 있습니다.")
