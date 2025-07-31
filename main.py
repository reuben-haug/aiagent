# main.py

import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function, available_functions
from system_prompt import system_prompt

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        sys.exit(1)

    input_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {input_prompt}\n")

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", 
        parts=[types.Part(text=input_prompt)])
    ]

    result = generate_content(client, messages, verbose)
    print(result)

def generate_content(client, messages, verbose):
    max_iterations = 20
    for i in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            if verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if not response.function_calls:
                if hasattr(response, "text") and response.text:
                    return response.text
                else:
                    continue

            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                messages.append(types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=str(function_call_part.name),
                            response=function_call_result.parts[0].function_response.response
                        )
                    ],
                ))

                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("No function response in returned content.")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response['result']}")
                function_responses.append(function_call_result.parts[0])

            if not function_responses:
                raise Exception("No function response generated.")

        except Exception as e:
            print(f"Error during iteration {i+1}: {e}")
            break

    return None

    
if __name__ == "__main__":
    main()