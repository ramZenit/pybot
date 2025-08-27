import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


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
    response = client.models.generate_content(    
        model="gemini-2.0-flash-001",
        contents=messages
        )
    
    print(f"User prompt: {messages[0].parts[0].text}") if verbose else None
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") if verbose else None
    print(response.text)
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}") if verbose else None
    



if __name__ == "__main__":
    main()
