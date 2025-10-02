import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python import *
from functions.write_file_content import *



def main():
    args = sys.argv[1:]    
    if not args:
        print("error: no prompt specified")
        print('usage: python main.py "your prompt here"')
        print('example: python main.py "are you going to take over the world?"')
        sys.exit(1)
    verbose = False
    if "--verbose" in args:
        verbose = True
    args = list(filter(lambda a: a != "--verbose", args))
    prompt = " ".join(args)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    for _ in range(20):
        try:                
            res = generate_content(client, messages, verbose)
            if res == "done":
                break
        except Exception as err:
            print(f"Error in generate_content: {err}")

    


def generate_content(client, messages, verbose=False):
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    for candidate in response.candidates:
        messages.append(candidate.content)

    verbose and print(f"User prompt: {messages[0].parts[0].text}") 
    verbose and print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") 
    if response.function_calls:
        function_responses = []
        for function_called in response.function_calls:
            print(function_called.args)
            call_result = call_function(function_called, verbose)
            function_responses.append(call_result.parts[0])            
            try:
                payload = call_result.parts[0].function_response.response
            except Exception:
                raise RuntimeError("Function response missing")
            verbose and print(f"-> {payload}")
        message = types.Content(role="user", parts=function_responses)
        messages.append(message)
    else:
        print(response.text)
        return "done"
        
    verbose and print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    functions_list = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    fname = function_call_part.name
    if fname not in functions_list:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fname,
                    response={"error": f"Unknown function: {fname}"},
                )
            ],
        )
    kwargs = dict(function_call_part.args)
    kwargs["working_directory"] = "./calculator"
    function_result = functions_list[fname](**kwargs)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fname,
                response={"result": function_result},
            )
        ],
    )

if __name__ == "__main__":
    main()
