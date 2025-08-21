from dotenv import load_dotenv
import openai
import os

# OPEN AI VARIABLES
OPENAI_API_KEY_NAME="OPENAI_API_KEY"
LINTING_MODEL="gpt-5-mini"

class AILinter:
    def __init__(self):
        if not openai.api_key:
            load_dotenv()
            openai.api_key = os.getenv(OPENAI_API_KEY_NAME)


    def remove_backticks(self, text: str) -> str:
        # in case of extra new lines or spacing
        stripped = text.strip()
        start = 3 if stripped.startswith("```") else 0
        end = -3 if stripped.endswith("```") else len(stripped)
        
        # add double new line at the end to ensure that linted chunks that get
        # concatenated together have blank lines between them
        return f"{stripped[start:end]}\n\n"  


    def get_message(self, role: str, prompt: str) -> dict:
        if role != "system" and role != "user":
            raise Exception("role must be either 'system' or 'user'")
        return {
            "role": role,
            "content": prompt,
        }


    def make_request(self, model: str, messages: list) -> str:
        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model=model,
            messages=messages
        )
        obj = completion.choices[0]
        res = obj.message.content
        return self.remove_backticks(res)


    def lint_text(self, text: str, linting_prompt: str):
        return self.make_request(LINTING_MODEL,
                                 [self.get_message("system", linting_prompt),
                                  self.get_message("user", f"Please clean up the following text:\n\n{text}")])
