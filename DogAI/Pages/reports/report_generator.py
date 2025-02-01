from abc import ABC, abstractmethod
from typing import Protocol, Dict
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image
from reportlab.lib.styles import getSampleStyleSheet

class ReportGenerator(Protocol):
    """개방-폐쇄 원칙(OCP)을 따르는 리포트 생성 인터페이스"""
    
    def generate(self, analysis_data: Dict) -> io.BytesIO: ...

class PDFReportGenerator:
    """구체적인 PDF 리포트 생성 클래스"""
    
    def generate(self, analysis_data: Dict) -> io.BytesIO:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        styles = getSampleStyleSheet()
        story.append(Paragraph("강아지 눈 건강 진단 보고서", styles['Heading1']))
        
        # 분석 결과 테이블 생성
        data = [[k, str(v)] for k, v in analysis_data.items()]
        story.append(Table(data))
        
        # 날짜 추가
        story.append(Paragraph(
            f"진단 일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
            styles['Normal']
        ))
        
        doc.build(story)
        buffer.seek(0)
        return buffer 