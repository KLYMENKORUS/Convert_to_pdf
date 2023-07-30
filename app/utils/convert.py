from io import BytesIO

from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class Docx2Pdf:

    def __init__(self, data: bytes) -> None:
        self.data = data

    async def convert(self):
        docx_buffer = BytesIO(self.data)
        doc = Document(docx_buffer)

        pdf_buffer = BytesIO()

        canvas_pdf = canvas.Canvas(pdf_buffer, letter)

        for para in doc.paragraphs:
            canvas_pdf.drawString(72, 800, para.text)
            canvas_pdf.showPage()

        canvas_pdf.save()

        return pdf_buffer.getvalue()