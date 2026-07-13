from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class ReportService:
    def build_pdf(self, analysis: dict[str, Any]) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, title="BluePHish Report")
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Heading1"],
            fontSize=18,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=12,
        )
        body_style = ParagraphStyle(
            "BodyStyle",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
        )

        story = []
        story.append(Paragraph("BluePHish - Phishing Report", title_style))
        story.append(Paragraph(f"Asunto: {analysis.get('subject', 'Sin asunto')}", body_style))
        story.append(Paragraph(f"Remitente: {analysis.get('from', 'Sin remitente')}", body_style))
        story.append(Paragraph(f"Puntuación: {analysis.get('score', 0)}/100", body_style))
        story.append(Paragraph(f"Nivel: {analysis.get('risk_level', 'low')}", body_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Resumen", styles["Heading2"]))
        story.append(Paragraph(analysis.get("summary", "Sin resumen"), body_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Indicadores", styles["Heading2"]))
        indicators = analysis.get("indicators", [])
        table_data = [["Tipo", "Detalle"]]
        for item in indicators:
            table_data.append([item.get("type", "-"), item.get("detail", "-")])
        table = Table(table_data, colWidths=[120, 360])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 10))
        story.append(Paragraph("Recomendaciones", styles["Heading2"]))
        ai_block = analysis.get("ai", {})
        recommendations = ai_block.get("recommendations", ["Verifica la URL antes de hacer clic."])
        for item in recommendations:
            story.append(Paragraph(f"• {item}", body_style))

        doc.build(story)
        return buffer.getvalue()


report_service = ReportService()
