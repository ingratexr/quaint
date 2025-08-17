import click
from ..context import CLIContext, modes


@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.option('-o', '--output', 
              type=click.Path(),
              help='Save linted output to this file instead of default')
@click.option('--extracted-text', 
              type=click.Path(),
              help='Save extracted unlinted text to this file instead of default')
@click.option('--ocr', 
              is_flag=True, 
              help='Use optical character recognition to read pdf instead of direct text extraction')
@click.option("--no-lint", 
              is_flag=True, 
              help='Extract and save text without linting')
@click.option('-m', '--mode', 
              type=click.Choice(modes, case_sensitive=False),
              help='Type of input text')
@click.option('--prompt', 
              type=click.Path(exists=True, readable=True),
              help="File to use as custom ai linting prompt")
@click.pass_context
def main(ctx, input_file, output, extracted_text, ocr, no_lint, mode, prompt):
    """Use text extraction """

    ctx.obj = CLIContext(input_file=input_file,
                         output_path=output,
                         extracted_text_path=extracted_text,
                         use_ocr=ocr,
                         no_lint=no_lint,
                         mode=mode,
                         custom_prompt_path=prompt,
                         echo=click.echo,
                         confirm=click.confirm)
    valid = ctx.obj.is_valid_context()

    if not valid:
        click.echo("Setup is invalid! Aborting.")
        return
    
    click.echo("Get text: from pdf (extraction or ocr), or as text.")
    click.echo("Save the extracted text! With or without page breaks!")
    click.echo("Figure out how/whether to split into chunks")
    click.echo("Submit one or many calls to the ai! In parallel or not!")
    click.echo("Reassemble text")
    click.echo("Save text")
    click.echo("Log any warnings")


if __name__ == '__main__':
    main()
