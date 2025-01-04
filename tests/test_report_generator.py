import pytest
from pathlib import Path
from src.services.report_generator_service import ReportGenerator

@pytest.fixture
def sample_data():
    return {
        'average_rating': 3.5,
        'total_reviews': 100,
        'common_issues': {
            'bug': 10,
            'crash': 5
        }
    }

def test_generate_csv(sample_data, tmp_path):
    generator = ReportGenerator()
    csv_path = generator.generate_csv(sample_data, tmp_path)
    
    assert csv_path.exists()
    assert csv_path.suffix == '.csv'
    
    # Check if CSV contains expected data
    import pandas as pd
    df = pd.read_csv(csv_path)
    assert 'Metric' in df.columns
    assert 'Value' in df.columns
    assert len(df) > 0

def test_generate_pdf(sample_data, tmp_path):
    generator = ReportGenerator()
    pdf_path = generator.generate_pdf(sample_data, tmp_path)
    
    assert pdf_path.exists()
    assert pdf_path.suffix == '.pdf'
    
    # Check if PDF file is not empty
    assert pdf_path.stat().st_size > 0