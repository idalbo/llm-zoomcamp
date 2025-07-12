import json
from IPython.display import display, HTML
import markdown

class Tools:
    def __init__(self):
        self.tools = {}
        self.functions = {}

    def add_tool(self, function, description):
        self.tools[function.__name__] = description
        self.functions[function.__name__] = function
    
    def get_tools(self):
        # Return tools in the correct format with 'function' property
        return [
            {
                "type": "function",
                "function": tool_desc
            }
            for tool_desc in self.tools.values()
        ]

    def function_call(self, tool_call_response):
        function_name = tool_call_response.function.name
        arguments = json.loads(tool_call_response.function.arguments)

        f = self.functions[function_name]
        result = f(**arguments)

        return {
            "tool_call_id": tool_call_response.id,
            "role": "tool",
            "content": json.dumps(result, indent=2),
        }


def shorten(text, max_length=50):
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


class ChatInterface:
    def input(self):
        try:
            question = input("You: ")
            return question
        except (KeyboardInterrupt, EOFError):
            return "stop"
    
    def display(self, message):
        print(message)

    def display_function_call(self, entry, result):
        call_html = f"""
            <details>
            <summary>Function call: <tt>{entry.function.name}({shorten(entry.function.arguments)})</tt></summary>
            <div>
                <b>Call</b>
                <pre>{entry.function.name}({entry.function.arguments})</pre>
            </div>
            <div>
                <b>Output</b>
                <pre>{result['content']}</pre>
            </div>
            </details>
        """
        display(HTML(call_html))

    def display_response(self, content):
        response_html = markdown.markdown(content)
        html = f"""
            <div>
                <div><b>Assistant:</b></div>
                <div>{response_html}</div>
            </div>
        """
        display(HTML(html))


class ChatAssistant:
    def __init__(self, tools, developer_prompt, chat_interface, client, model):
        self.tools = tools
        self.developer_prompt = developer_prompt
        self.chat_interface = chat_interface
        self.client = client
        self.model = model
    
    def gpt(self, chat_messages):
        return self.client.chat.completions.create(
            model=self.model,
            messages=chat_messages,
            tools=self.tools.get_tools(),
        )

    def run(self):
        chat_messages = [
            {"role": "system", "content": self.developer_prompt},
        ]

        # Chat loop
        while True:
            question = self.chat_interface.input()
            
            # Handle empty input or exit commands
            if not question or question.strip().lower() in ['stop', 'exit', 'quit']:  
                self.chat_interface.display("Chat ended.")
                break

            message = {"role": "user", "content": question}
            chat_messages.append(message)

            while True:  # inner request loop
                response = self.gpt(chat_messages)
                message = response.choices[0].message

                # Only add tool_calls if they exist
                assistant_message = {
                    "role": "assistant",
                    "content": message.content,
                }
                if message.tool_calls:
                    assistant_message["tool_calls"] = message.tool_calls
                
                chat_messages.append(assistant_message)

                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        result = self.tools.function_call(tool_call)
                        chat_messages.append(result)
                        self.chat_interface.display_function_call(tool_call, result)
                else:
                    self.chat_interface.display_response(message.content)
                    break