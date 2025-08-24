from .context import Context, Mode
from .textifier import Textifier, FileType, Text
from .ai_linter import AILinter
from pathlib import Path
from .strutil import Strutil
from typing import Callable

class Pipeline:
    def __init__(
            self, 
            log=print, 
            progress_fn=lambda msg: print(f"\r{msg}", nl=False),
        ) -> None:
        self.log = log
        self.progress_fn = progress_fn
        self.textifier = Textifier(
            log=self.log, 
            progress_fn=self.progress_fn,
        )
        self.strutil = Strutil(log=self.log)
        self.ai = AILinter()


    def run(self, context: Context) -> None:
        try:
            text = self.textifier.extract_text(
                file=context.input_file, 
                use_ocr=context.use_ocr
            )
            if (text.filetype == FileType.UNSUPPORTED or not text.filetype
                or not (text.text or text.pages)):
                self.log("Unable to extract text. Sorry!")
                return 
            match context.mode:
                case Mode.TEXT:
                    return self._generic_text_pipeline(context, text)
                case Mode.SCREENPLAY:
                    return self._screenplay_pipeline(context, text)
                case _:
                    raise Exception(f"Unexpected mode: {context.mode}")
        except Exception as e:
            self.log(f"Encountered an unexpected error: {e}")
 

    def _screenplay_pipeline(self, context: Context, text: Text) -> str:
        chunks = self._chunker(text, self.strutil.chunk_screenplay_text)
        print("chunks length: ", len(chunks))
        print("ai lint not yet implemented")


    def _generic_text_pipeline(self, context: Context, text: Text) -> str:
        chunks = self._chunker(text, self.strutil.chunk_generic_text)
        print("chunks length: ", len(chunks))
        print("ai lint not yet implemented")
        

    def _chunker(self, text: Text, text_chunker: Callable) -> list[str]:
        if text.pages:
            return self.strutil.chunk_pages(text.pages)
        elif text.text:
            return text_chunker(text.text)
        else:
            raise Exception("Extracted text contains neither text nor pages.")


    @staticmethod
    def write_file(path: Path, text: str) -> None:
        with open(path, "w") as f:
            f.write(text)




            # # now that strutil exists next step is:
            # # - split the input file into chunks depending on filetype
            # # - make ai lint calls in parallel so it doesn't take so long
            # # - reconstruct and save

            # raise Exception("Text is now an array! Not implemented in pipeline!")

            # # extract text, or faceplant gracefully
            # text = tx.extract_text(file=ctx.input_file, use_ocr=ctx.use_ocr)    
            # if text == None:
            #     log("Unable to extract text. Aborting.")
            #     return
            # elif text.strip() == "":
            #     log("Extracted an empty string, or just white space. Aborting.")
            #     return

            # # otherwise 
            # p.write_file(path=ctx.extracted_text_file, text=text)
            # log("Saved extracted text.")

            # # if no lint, that's it
            # if ctx.no_lint:
            #     return

            # # lint, save, declare victory
            # log("AI linting...")
            # linted = ai.lint_text(text=text, linting_prompt=ctx.prompt_text)
            # p.write_file(path=ctx.output_file, text=linted)
            # log("Finished!")