from abc import ABC, abstractmethod
from typing import Dict
from pathlib import Path

class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate_csv(self, data: Dict, output_path: Path) -> Path:
        """
        Generate CSV report from analysis data
        
        Args:
            data: Dictionary containing analysis results
            output_path: Path where the report should be saved
            
        Returns:
            Path to the generated report
        """
        pass

    @abstractmethod
    def generate_pdf(self, data: Dict, output_path: Path) -> Path:
        """
        Generate PDF report from analysis data
        
        Args:
            data: Dictionary containing analysis results
            output_path: Path where the report should be saved
            
        Returns:
            Path to the generated report
        """
        pass