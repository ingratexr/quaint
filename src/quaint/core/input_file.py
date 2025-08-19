from .textifier import FileType
from pathlib import Path
from typing import Optional


class InputFile:
    def __init__(self, path: Path):
        self.path: Path = path
        self.type: Optional[FileType] = None
        self.extracted_text: Optional[str] = None
        self.linted_text: Optional[str] = None


    def set_type(self, type: FileType) -> None:
        self.type = type


    def set_extracted_text(self, text: str) -> None:
        self.extracted_text = text

