# main.py

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schema_definitions import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = '''
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.  You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory.  You do not need to specify the working directory in your functions calls as it is automatically injected for security reasons.
'''

if len(sys.argv) < 2:
    print(f"Usage: python3 main.py 'your prompt here'")
    sys.exit(1)

input_prompt = sys.argv[1]

messages = [
    types.Content(role="user", 
    parts=[types.Part(text=input_prompt)])
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

# GenerateContentResponse object assignment
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt)
)

if "--verbose" in sys.argv:
        print(f"User prompt: {input_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)
else:
    if response.function_calls:
         for func in response.function_calls:
            print(f"Calling function: {func.name}({func.args})")
    else:
        print(response.text)