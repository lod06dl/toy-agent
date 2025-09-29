import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from function.get_files_info import schema_get_files_info

def main():
    print("Hello from toy-agent!")
    load_dotenv()
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
   
    try:
        prompt = sys.argv[1]  # first argument after the script name
        print("First argument:", prompt)
    except IndexError:
        print("Error: No argument provided. Please provide a prompt as the first argument.")
        sys.exit(1)

    verbose = '--verbose' in sys.argv

    # response = client.models.generate_content(model='gemini-2.0-flash-001', contents=prompt)
    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=prompt,
    config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
)
    fr = response.function_calls
    if fr is not None:
        for f in fr:
            print(f"Calling function: {f.name}({f.args})")

    print(response.text)
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
