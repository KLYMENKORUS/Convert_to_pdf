import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Any

from PIL import Image


@dataclass(frozen=True, slots=True)
class Docx2Pdf:
    timeout = None

    def create_tempfile(self, data: bytes):
        with tempfile.NamedTemporaryFile(
            suffix=".docx", delete=False
        ) as temp_docx:
            temp_docx.write(data)

        return temp_docx.name

    def open_file(self, filename: str) -> bytes:
        with open(filename, "rb") as file:
            result = file.read()

        return result

    def convert(self, **kwargs: Any) -> bytes:
        args = [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            "temp",
            self.create_tempfile(kwargs.get("data")),
        ]

        process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=self.timeout,
        )
        filename = re.search("-> (.*?) using filter", process.stdout.decode())

        result = self.open_file(f"{filename.group(1)}")

        os.remove(filename.group(1))

        return result


@dataclass(frozen=True, slots=True)
class Jpg2Pdf:
    def __call__(self, **kwds: Any) -> Any:
        return self.jpg2pdf(**kwds)

    def create_tempfile(self, data: bytes) -> str:
        with tempfile.NamedTemporaryFile(
            suffix=".jpg", delete=False
        ) as temp_jpg:
            temp_jpg.write(data)

        return temp_jpg.name

    def convert(self, **kwds: Any) -> str:
        file = self.create_tempfile(kwds.get("data"))
        image = Image.open(file)
        image.convert("RGB")
        image.save(file.replace(".jpg", ".pdf"))

        return file.replace(".jpg", ".pdf")

    def jpg2pdf(self, **kwds: Any) -> bytes:
        file_convert = self.convert(**kwds)

        with open(file_convert, "rb") as file:
            result = file.read()

        os.remove(file_convert)

        return result
