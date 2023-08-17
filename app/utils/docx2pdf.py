import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Docx2Pdf:
    timeout = None

    def create_tempfile(self, data: bytes):
        with tempfile.NamedTemporaryFile(
            suffix=".docx", delete=False
        ) as temp_docx:
            temp_docx.write(data)

        return temp_docx.name

    def open_file(self, filename: str):
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
