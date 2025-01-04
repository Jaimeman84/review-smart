import pandas as pd
from pathlib import Path
from typing import Dict
from fpdf import FPDF
from src.interfaces.report_generator_interface import ReportGeneratorInterface

class ReportGenerator(ReportGeneratorInterface):
    def generate_csv(self, data: Dict, output_path: Path) -> Path:
        df = pd.DataFrame({
            'Metric': ['Average Rating', 'Total Reviews'] + list(data['common_issues'].keys()),
            'Value': [data['average_rating'], data['total_reviews']] + list(data['common_issues'].values())
        })
        
        csv_path = output_path / 'analysis_report.csv'
        df.to_csv(csv_path, index=False)
        return csv_path
    
    def generate_pdf(self, data: Dict, output_path: Path) -> Path:
        pdf = FPDF()
        pdf.add_page()
        
        # Add title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Review Analysis Report', ln=True, align='C')
        
        # Add summary
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Average Rating: {data['average_rating']:.2f}", ln=True)
        pdf.cell(0, 10, f"Total Reviews: {data['total_reviews']}", ln=True)
        
        # Add common issues
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Common Issues:', ln=True)
        pdf.set_font('Arial', '', 12)
        for issue, count in data['common_issues'].items():
            pdf.cell(0, 10, f"- {issue}: {count}", ln=True)
        
        pdf_path = output_path / 'analysis_report.pdf'
        pdf.output(str(pdf_path))
        return pdf_path