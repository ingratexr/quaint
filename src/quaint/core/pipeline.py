from .context import Context
from .textifier import Textifier
from .ai_linter import AILinter
from pathlib import Path

class Pipeline:
    def run(ctx: Context):
        """
        Given a context with an input file and valid options, runs the pipeline
        to extract, lint, and save the text from the context's input file.

        :param ctx
        Context with input file and options.
        """
        p = Pipeline
        tx = Textifier(log=ctx.log, progress_fn=ctx.progress_fn)
        ai = AILinter()
        log = ctx.log

        try:
            # extract text, or faceplant gracefully
            text = tx.extract_text(file=ctx.input_file, use_ocr=ctx.use_ocr)    
            if text == None:
                log("Unable to extract text. Aborting.")
                return
            elif text.strip() == "":
                log("Extracted an empty string, or just white space. Aborting.")
                return

            # otherwise 
            p.write_file(path=ctx.extracted_text_file, text=text)
            log("Saved extracted text.")

            # if no lint, that's it
            if ctx.no_lint:
                return

            # lint, save, declare victory
            log("AI linting...")
            linted = ai.lint_text(text=text, linting_prompt=ctx.prompt_text)
            p.write_file(path=ctx.output_file, text=linted)
            log("Finished!")

        except Exception as e:
            log(f"Encountered an unexpected error: {e}")
 

    @staticmethod
    def write_file(path: Path, text: str) -> None:
        with open(path, "w") as f:
            f.write(text)
