from celery import Celery

from app.database import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from app.utils.docx2pdf import Docx2Pdf


celery = Celery(
    "convert", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND
)


@celery.task
def convert_file(data: bytes) -> bytes:
    return Docx2Pdf().convert(data=data)
