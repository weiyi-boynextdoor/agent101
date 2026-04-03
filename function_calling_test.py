import ollama
import datetime
import json

MODEL_NAME = 'qwen3.5:397b-cloud'

def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def parse_tool_arguments(tool_call):
    arguments = tool_call['function'].get('arguments', {})

    if isinstance(arguments, str):
        arguments = arguments.strip()
        if not arguments:
            return {}
        return json.loads(arguments)

    if isinstance(arguments, dict):
        return arguments

    raise TypeError(f'Unsupported tool arguments type: {type(arguments).__name__}')

if __name__ == '__main__':
    while True:
        user_input = input('User: ')
        messages = [{'role': 'user', 'content': user_input}]

        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            tools=[{
                'type': 'function',
                'function': {
                    'name': 'get_current_time',
                    'description': 'get current local time',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                    },
                },
            }]
        )
        while response['message'].get('tool_calls'):
            available_functions = {
                'get_current_time': get_current_time,
            }

            for tool in response['message']['tool_calls']:
                function_to_call = available_functions[tool['function']['name']]
                function_arguments = parse_tool_arguments(tool)
                function_response = function_to_call(**function_arguments)

                messages.append({
                    'role': 'tool',
                    'content': function_response,
                })
            response = ollama.chat(model=MODEL_NAME, messages=messages)
        print('Assistant:', response['message']['content'])
