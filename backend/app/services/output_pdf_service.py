"""
Output PDF Service Module
Generates professional summary PDF using ReportLab
"""

import tempfile
from io import BytesIO
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from typing import Optional
import fitz
from app.core import logger
from app.models.bom import Summary, SummaryItem


class OutputPDFService:
    """Service for generating output PDF summaries"""
    
    def __init__(self):
        """Initialize output PDF service"""
        self.logger = logger
    
    def generate_summary_pdf(self, summary: Summary, output_path: str, source_pdf_path: Optional[str] = None) -> bool:
        """
        Generate summary PDF from Summary object.

        If a source drawing PDF is supplied, the summary is appended as an extra
        page to the original drawing so the returned document contains the source
        drawing plus the extracted summary table.
        """
        try:
            self.logger.info(f"Generating summary PDF: {output_path}")

            # Create output directory if needed
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            if source_pdf_path and Path(source_pdf_path).exists():
                return self._generate_with_source_pdf(summary, source_pdf_path, output_path)

            return self._generate_summary_only_pdf(summary, output_path)
        except Exception as e:
            self.logger.error(f"Error generating PDF: {str(e)}")
            return False

    def _generate_summary_only_pdf(self, summary: Summary, output_path: str) -> bool:
        """Generate a standalone PDF containing the summary table."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        story = []
        story.append(self._create_title())
        story.append(Spacer(1, 0.2*inch))

        table_data = self._create_table_data(summary)
        table = self._create_table(table_data)
        story.append(table)

        story.append(Spacer(1, 0.2*inch))
        story.append(self._create_grand_total(summary))
        story.append(Spacer(1, 0.3*inch))
        story.append(self._create_footer())

        doc.build(story)
        self.logger.info(f"Successfully generated PDF: {output_path}")
        return True

    def _generate_with_source_pdf(self, summary: Summary, source_pdf_path: str, output_path: str) -> bool:
        """Insert summary table on page 1 by overlaying it as an image."""
        try:
            source_doc = fitz.open(source_pdf_path)
            
            # Generate summary table as image
            summary_image_path = Path(tempfile.gettempdir()) / f"summary_table_{datetime.now():%Y%m%d%H%M%S%f}.png"
            if not self._generate_summary_table_image(summary, str(summary_image_path)):
                self.logger.warning("Failed to generate summary as image, using text fallback")
                return self._generate_summary_with_text_fallback(summary, source_doc, output_path)

            output_doc = fitz.open()
            
            # Copy first page
            page1 = source_doc[0]
            output_page = output_doc.new_page(width=page1.rect.width, height=page1.rect.height)
            output_page.show_pdf_page(output_page.rect, source_doc, 0)
            
            # Insert summary table image on page 1
            self._insert_summary_image(output_page, str(summary_image_path), page1)
            
            # Copy remaining pages from source
            for page_index in range(1, len(source_doc)):
                source_page = source_doc[page_index]
                new_page = output_doc.new_page(width=source_page.rect.width, height=source_page.rect.height)
                new_page.show_pdf_page(new_page.rect, source_doc, page_index)

            output_doc.save(output_path)
            output_doc.close()
            source_doc.close()
            
            # Cleanup
            summary_image_path.unlink(missing_ok=True)
            
            self.logger.info(f"Successfully generated source + summary PDF with image overlay: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error combining source PDF with summary image: {str(e)}")
            try:
                return self._generate_summary_with_text_fallback(summary, source_doc, output_path)
            except:
                return self._generate_summary_only_pdf(summary, output_path)

    def _generate_summary_table_image(self, summary: Summary, image_path: str) -> bool:
        """Generate summary table as a high-quality image"""
        try:
            # Create a summary PDF first
            pdf_path = Path(tempfile.gettempdir()) / f"summary_table_{datetime.now():%Y%m%d%H%M%S%f}.pdf"
            
            doc = SimpleDocTemplate(
                str(pdf_path),
                pagesize=(7*inch, 4*inch),
                rightMargin=0.3*inch,
                leftMargin=0.3*inch,
                topMargin=0.3*inch,
                bottomMargin=0.3*inch
            )

            story = []
            
            # Add title
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'TableTitle',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=8,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph("SUMMARY OF COMPONENTS", title_style))
            story.append(Spacer(1, 0.1*inch))
            
            # Create and add table
            table_data = self._create_table_data(summary)
            table = self._create_visible_table(table_data)
            story.append(table)
            
            story.append(Spacer(1, 0.1*inch))
            
            # Add footer with total weight
            if summary.grand_total_weight:
                total_text = f"TOTAL WEIGHT: {summary.grand_total_weight:.2f} kg"
            else:
                total_text = "TOTAL WEIGHT: To be calculated based on complete dimensions"
            
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#333333'),
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph(total_text, footer_style))
            
            # Build PDF
            doc.build(story)
            
            # Convert PDF to image
            pdf_doc = fitz.open(str(pdf_path))
            page = pdf_doc[0]
            # Higher zoom for better quality
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
            pix.save(image_path)
            pdf_doc.close()
            
            pdf_path.unlink(missing_ok=True)
            self.logger.info(f"Generated summary table image: {image_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error generating summary table image: {str(e)}")
            return False

    def _create_visible_table(self, table_data: list) -> Table:
        """Create a visible, properly formatted table for image overlay"""
        
        table = Table(table_data, colWidths=[0.7*inch, 1.8*inch, 0.9*inch, 0.5*inch, 
                                             0.5*inch, 1.0*inch, 1.0*inch])
        
        style = TableStyle([
            # Header style - Dark background
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            
            # Data rows
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            
            # Grid and borders
            ('GRID', (0, 0), (-1, -1), 1.5, colors.black),
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
            
            # Alternating row colors for better readability
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
        ])
        
        table.setStyle(style)
        return table

    def _insert_summary_image(self, page, image_path: str, source_page):
        """Insert summary table image on page 1"""
        try:
            page_width = source_page.rect.width
            page_height = source_page.rect.height
            
            # Position in the SUMMARY TABLE box (lower-right area)
            x0 = page_width * 0.52  # Start at 52% from left
            y0 = page_height * 0.60  # Start at 60% from top
            x1 = page_width * 0.99  # End at 99% from left
            y1 = page_height * 0.98  # End at 98% from top
            
            rect = fitz.Rect(x0, y0, x1, y1)
            page.insert_image(rect, filename=image_path)
            
            self.logger.info(f"Inserted summary table image at position ({x0}, {y0}) to ({x1}, {y1})")
            return True
        except Exception as e:
            self.logger.error(f"Error inserting summary image: {str(e)}")
            return False

    def _generate_summary_with_text_fallback(self, summary: Summary, source_doc, output_path: str) -> bool:
        """Fallback: Generate summary only PDF (append to end)"""
        try:
            output_doc = fitz.open()
            
            # Copy all source pages
            for page_index in range(len(source_doc)):
                source_page = source_doc[page_index]
                output_page = output_doc.new_page(width=source_page.rect.width, height=source_page.rect.height)
                output_page.show_pdf_page(output_page.rect, source_doc, page_index)
            
            # Generate and append summary
            summary_temp_file = Path(tempfile.gettempdir()) / f"summary_{datetime.now():%Y%m%d%H%M%S%f}.pdf"
            if self._generate_summary_only_pdf(summary, str(summary_temp_file)):
                summary_doc = fitz.open(str(summary_temp_file))
                output_doc.insert_pdf(summary_doc)
                summary_doc.close()
                summary_temp_file.unlink(missing_ok=True)
            
            output_doc.save(output_path)
            output_doc.close()
            source_doc.close()
            
            self.logger.info(f"Successfully generated PDF with appended summary: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Fallback method failed: {str(e)}")
            return False

    
    def _create_title(self):
        """Create PDF title"""
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        return Paragraph("SUMMARY OF COMPONENTS", title_style)
    
    def _create_table_data(self, summary: Summary) -> list:
        """Create table data from summary"""
        
        # Table header
        headers = ["PART NO.", "DESCRIPTION", "MATERIAL", "QTY.", "UNIT", 
                  "WEIGHT/UNIT", "TOTAL WEIGHT"]
        
        data = [headers]
        
        # Add summary items
        for item in summary.summary:
            row = [
                str(item.part_no) if item.part_no else "",
                str(item.description) if item.description else "",
                str(item.material) if item.material else "-",
                self._format_quantity(item.quantity),
                str(item.unit) if item.unit else "-",
                self._format_weight(item.weight_per_unit, item.unit),
                self._format_weight(item.total_weight, "kg")
            ]
            data.append(row)
        
        return data
    
    def _create_table(self, table_data: list) -> Table:
        """Create formatted table"""
        
        # Create table
        table = Table(table_data, colWidths=[0.8*inch, 2.0*inch, 0.8*inch, 0.6*inch, 
                                             0.6*inch, 1.2*inch, 1.2*inch])
        
        # Style table
        style = TableStyle([
            # Header style
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            
            # Data style
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            
            # Grid lines
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ])
        
        table.setStyle(style)
        return table
    
    def _create_grand_total(self, summary: Summary):
        """Create grand total section"""
        styles = getSampleStyleSheet()
        
        if summary.grand_total_weight:
            total_text = f"TOTAL / ESTIMATED TOTAL WEIGHT: {summary.grand_total_weight:.2f} kg"
        else:
            total_text = "TOTAL WEIGHT: To be calculated based on complete dimensions"
        
        total_style = ParagraphStyle(
            'GrandTotal',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1a1a1a'),
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold'
        )
        
        return Paragraph(total_text, total_style)
    
    def _create_footer(self):
        """Create PDF footer"""
        styles = getSampleStyleSheet()
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER
        )
        
        footer_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | EngiSummary System"
        return Paragraph(footer_text, footer_style)
    
    def _format_quantity(self, quantity) -> str:
        """Format quantity for display"""
        if quantity is None:
            return "-"
        
        try:
            if isinstance(quantity, float) and quantity == int(quantity):
                return str(int(quantity))
            return str(quantity)
        except Exception:
            return str(quantity)
    
    def _format_weight(self, weight, unit) -> str:
        """Format weight for display"""
        if weight is None:
            return "-"
        
        try:
            unit_str = ""
            if unit and unit.upper() not in ["NOS", "PCS"]:
                unit_str = f" {unit.lower()}/m" if unit.lower() == "m" else f" {unit.lower()}"
            else:
                unit_str = " kg"
            
            return f"{weight:.2f}{unit_str}"
        except Exception:
            return "-"


# Create service instance
output_pdf_service = OutputPDFService()
