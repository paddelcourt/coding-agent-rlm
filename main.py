import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.run_any_file import schema_run_any_file
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.delete_file import schema_delete_file
from functions.call_sub_rlm import schema_call_sub_rlm
from functions.call_functions import call_function
import click


@click.command()
@click.option("--verbose", is_flag=True, help="Print token usage and tool outputs.")
@click.option("--max-turns", default=20, show_default=True)

def cli(verbose, max_turns):
     
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")


    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_run_any_file, schema_write_file, schema_get_file_content, schema_delete_file, schema_call_sub_rlm],
    )
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    click.echo("How can I assist you today?")
    messages = []
    

    while True:
        counter = 0
        final_text = None

        user_msg = click.prompt("> ", default="", show_default=False)
        if not user_msg or user_msg.strip().lower() == "/exit":
            break
        messages.append(types.Content(role="user", parts=[types.Part(text=user_msg)]))

        while counter < max_turns: #limit tool calling to 20 turns
            final_text = generate_content(client, messages, verbose, config)
            if final_text:
                click.echo(final_text)
                break
            counter += 1
        if counter >= max_turns and not final_text:
            click.echo("No final response after max_turns; try again.")

        


def generate_content(client, messages, verbose, config):
        
        model_name = os.environ.get("GEMINI_MODEL")
        
        function_responses = []

        try:
            

            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=config
            )

            if verbose:
                click.echo(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                click.echo(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if not response.function_calls:
                    return response.text



            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=verbose, client=client)
                function_responses += function_call_result.parts
                # just print the function result if verbose
                if verbose:
                        cli.echo(
                            f"-> {function_call_result.parts[0].function_response.response}"
                            )
                
            
            messages.append(types.Content(role="user", parts=function_responses))
            return None
                
                

        except Exception as e:
            print(f"Error: {e}")

    
if __name__ == "__main__":
    cli()



