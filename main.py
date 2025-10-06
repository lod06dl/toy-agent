import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from function.get_files_info import schema_get_files_info, get_files_info
from function.get_file_content import schema_get_file_content, get_file_content
from function.run_python_file import schema_run_python_file, run_python_file
from function.write_file import schema_write_file, write_file
from function.call_function import call_function
from function.call_function import available_functions

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

    message = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        )
    ]
    # response = client.models.generate_content(model='gemini-2.0-flash-001', contents=prompt)
    for i in range(20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=message,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt )
        )
        # print('response.candidates:', response.candidates)
        for cnd in response.candidates:
            message.append(types.Content(parts=cnd.content.parts, role='model'))       
        fr = response.function_calls

        if fr is not None:
            for f in fr:
                print(f"Calling function: {f.name}({f.args})")
                c = call_function(f)
                message.append(types.Content(parts=c.parts, role='user'))
                try:
                    print(f"-> {c.parts[0].function_response.response}")
                except AttributeError:
                    print('call function error returned unxepected object:' ,c )
        else:
            print('Final response:',response.text)
            break

        verbose = '--verbose' in sys.argv
        if verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
