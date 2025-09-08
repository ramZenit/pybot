import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info



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
    
    generate_content(client, messages, verbose)


    


def generate_content(client, messages, verbose=False):
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    verbose and print(f"User prompt: {messages[0].parts[0].text}") 
    verbose and print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") 
    print(response.text)
    print(f"Calling function: {response.function_calls}({response.function_calls.args})")
    verbose and print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    



if __name__ == "__main__":
    main()
