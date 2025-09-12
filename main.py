import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    print("Hello from toy-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    try:
        prompt = sys.argv[1]  # first argument after the script name
        print("First argument:", prompt)
    except IndexError:
        print("Error: No argument provided. Please provide a prompt as the first argument.")
        sys.exit(1)

    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=prompt)
    print(response.text)
    if (len(sys.argv) > 2):
        if (sys.argv[2] == "--verbose"):
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
