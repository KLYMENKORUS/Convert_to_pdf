import re
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Type


class FormatFile(str, Enum):
    docx: str = ".docx"
    jpg: str = ".jpg"
    odt: str = ".odt"


@dataclass(slots=True, unsafe_hash=True)
class FromCyrillic:
    letters = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }

    def __call__(self, filename: str) -> Callable[[str], str]:
        return self.translate_to_en(filename)

    def translate_to_en(self, filename: str) -> str:
        return "".join(
            self.letters.get(char, char) for char in filename.lower()
        )


@dataclass(slots=True, unsafe_hash=True)
class Cyrillic:
    cyrillic: Type[FromCyrillic] = FromCyrillic()

    def check_cyrillic(self, filename: str) -> bool:
        cyrillic_pattern = re.compile("[\u0400-\u04FF]")
        return bool(cyrillic_pattern.search(filename))

    def check_filename(self, filename: str) -> str:
        return (
            self.cyrillic(filename)
            if self.check_cyrillic(filename)
            else filename
        )

    def __call__(self, filename: str) -> Callable[[str], str]:
        return self.check_filename(filename)
