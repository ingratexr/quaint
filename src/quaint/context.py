import shutil
from pathlib import Path
from typing import Optional

# paths to linting prompts
dir = Path(__file__).parent
LINT_SCREENPLAY_PROMPT=Path(dir / "./prompts/lint_screenplay.txt")
LINT_GENERIC_TEXT_PROMPT=Path(dir /"./prompts/lint_generic_text.txt")

# constants for mode list
TEXT_SHORT = "t"
TEXT = "text"
SCREENPLAY_SHORT = "sp"
SCREENPLAY = "screenplay"

# preset modes
modes = [TEXT_SHORT, TEXT, SCREENPLAY_SHORT, SCREENPLAY]

# map each mode to the path for its prompt
mode_to_prompt_path_map = {
    TEXT_SHORT: LINT_GENERIC_TEXT_PROMPT,
    TEXT: LINT_GENERIC_TEXT_PROMPT,
    SCREENPLAY_SHORT: LINT_SCREENPLAY_PROMPT,
    SCREENPLAY: LINT_SCREENPLAY_PROMPT,
}

# defaults
DEFAULT_LINTED_SUFFIX = "_linted.txt"
DEFAULT_EXTRACTED_SUFFIX = "_extracted_text.txt"
DEFAULT_MODE = TEXT

class CLIContext:
    """
    """
    def __init__(self, 
                 input_file,
                 output_path,
                 extracted_text_path,
                 use_ocr,
                 no_lint,
                 mode,
                 custom_prompt_path,
                 echo,
                 confirm):
        self.echo = echo
        self.confirm = confirm
        self.input_file = Path(input_file)
        self.output_file = self._confirmed_filename_or_none(output_path, DEFAULT_LINTED_SUFFIX)
        self.extracted_text_file = self._confirmed_filename_or_none(extracted_text_path, DEFAULT_EXTRACTED_SUFFIX) 
        self.use_ocr = use_ocr
        self.no_lint = no_lint
        self.prompt_text = self._get_prompt_text(mode, custom_prompt_path, no_lint)


    def _confirmed_filename_or_none(self, provided_filename, default_suffix) -> Optional[Path]:
        input_filename = self.input_file.stem
        input_directory = self.input_file.parent
        val = Path(provided_filename) if provided_filename else input_directory / f"{input_filename}{default_suffix}"
        return val if self._confirm_path_writeable(val) else None


    def _confirm_path_writeable(self, path: Path) -> bool:
        if not path.is_file():
            return True
        return self.confirm(f"A file already exists at {path}. Overwrite it?")


    def _get_prompt_text(self, provided_mode, custom_prompt_path, no_lint) -> str: 
        if no_lint and (provided_mode or custom_prompt_path):
            self.echo("You provided the --no-lint flag, so no linting will be performed. The mode and/or prompt you provided will be ignored.")
            return ""
        if provided_mode and custom_prompt_path:
            self.echo(f"You provided the preset mode {provided_mode} and also the custom prompt file {custom_prompt_path}. Ignoring {provided_mode} mode and using the custom prompt instead.")
        mode = provided_mode if provided_mode else DEFAULT_MODE
        path = custom_prompt_path if custom_prompt_path else mode_to_prompt_path_map[mode]
        with open(path, "r") as file:
            return file.read().strip()


    def is_valid_context(self) -> bool:
        valid_prompt_text = True if self.no_lint else bool(self.prompt_text) 
        req = [self.input_file, self.output_file, self.extracted_text_file, valid_prompt_text]
        return sum([bool(_) for _ in req]) == len(req)
        

    def has_ocr_dependencies_installed(self) -> bool:
        tesseract = shutil.which("tesseract")
        poppler = shutil.which("pdftoppm")
        if not poppler:
            poppler = shutil.which("pdftocairo")
        if poppler and tesseract:
            return True
        missing = ["tesseract" if not tesseract else None,
                   "poppler" if not poppler else None]
        missing = (", ").join(missing)
        print(f"Tesseract and Poppler must both be installed on your machine \
              to use OCR. It looks like you may be missing [{missing}].")
        return False
