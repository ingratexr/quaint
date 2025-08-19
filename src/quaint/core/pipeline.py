from .context import Context
from .textifier import Textifier, FileType
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
        log = ctx.log

        # extract and save raw text
        text = p.input_file_text(ctx=ctx, tx=tx)
        p.write_file(path=ctx.extracted_text_file, text=text)

        # if no lint, that's it, declare victory
        if ctx.no_lint:
            return


        log(f"  - chunk extracted text, or don't")
        log(f"  - lint extracted text with ai")
        log(f"  - collect and reassemble chunks of linted text")
        log(f"  - deterministic cleanup (at least for screenplays)")
        log(f"  - save finished linted text")
        log(f"  - declare victory; log any warnings; return")
    

    @staticmethod
    def input_file_type(ctx: Context, tx: Textifier) -> FileType:
        return tx.filetype(ctx.input_file)
    
    
    @staticmethod
    def input_file_text(ctx: Context, tx: Textifier) -> str:
        return tx.extract_text(file=ctx.input_file,
                               use_ocr=ctx.use_ocr)


    @staticmethod
    def write_file(path: Path, text: str) -> None:
        with open(path, "w") as f:
            f.write(text)
