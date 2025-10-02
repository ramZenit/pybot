import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function, available_functions
from config import MAX_ITERS
from prompts import system_prompt


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv    
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    
    if not args:
        print("error: no prompt specified")
        print('usage: python main.py "your prompt here" [--verbose]')
        print('example: python main.py "are you going to take over the world?"')
        sys.exit(1)
        
    user_prompt = " ".join(args)
    verbose and print(f"User prompt: {user_prompt}\n")
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iteration ({MAX_ITERS}) reached.")
            sys.exit(1)
        
        try:                
            
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as err:
            print(f"Error in generate_content: {err}")



def generate_content(client, messages, verbose=False):

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    verbose and print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") 
    verbose and print(f"Response tokens: {response.usage_metadata.candidates_token_count}") 
    
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)        
    
    if not response.function_calls:
        return response.text
    
    function_responses = []
    for function_called_parts in response.function_calls:
        function_call_result = call_function(function_called_parts, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        
        function_responses.append(function_call_result.parts[0])            
        payload = function_call_result.parts[0].function_response.response
        verbose and print(f"-> {payload}")
    
    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    message = types.Content(role="user", parts=function_responses)
    messages.append(message)
    

if __name__ == "__main__":
    main()
