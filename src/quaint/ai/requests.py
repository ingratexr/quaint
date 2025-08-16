from dotenv import load_dotenv
import openai
import os

# OPEN AI VARIABLES
OPENAI_API_KEY_NAME="OPENAI_API_KEY"
LINTING_MODEL="gpt-5-mini"

# LINTING PROMPTS
LINT_SCREENPLAY_PROMPT="../prompts/lint_screenplay.txt"
LINT_GENERIC_TEXT_PROMPT="../prompts/lint_generic_text.txt"


if not openai.api_key:
    load_dotenv()
    openai.api_key = os.getenv(OPENAI_API_KEY_NAME)


def get_prompt(file):
    """
    Returns the default prompt for linting a script
    """
    with open(os.path.join(os.path.dirname(__file__), file), "r") as fp:
        return fp.read()


def remove_backticks(res):
    # result normally comes back wrapped in triple backticks, so remove these
    start = 3 if res.startswith("```") else 0
    end = -3 if res.endswith("```") else len(res)
    
    # add double new line at the end to ensure that linted chunks that get
    # concatenated together have blank lines between them
    return f"{res[start:end]}\n\n"  


def get_message(role, prompt):
    if role != "system" and role != "user":
        raise Exception("role must be either 'system' or 'user'")
    return {
        "role": role,
        "content": prompt,
    }


def make_request(model, messages):
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    obj = completion.choices[0]
    res = obj.message.content
    return remove_backticks(res)


def lint_text(text: str, linting_prompt: str):
    return make_request(LINTING_MODEL,
                        [get_message("system", linting_prompt),
                        get_message("user", f"Please clean up the following text:\n\n{text}")])


def lint_generic_text(text:str):
    return lint_text(text, get_prompt(LINT_GENERIC_TEXT_PROMPT))


def lint_screenplay(text: str):
    return lint_text(text, get_prompt(LINT_SCREENPLAY_PROMPT))

