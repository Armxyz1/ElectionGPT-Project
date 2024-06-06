import os
import openai
os.environ["OPENAI_API_KEY"] =""
openai.api_key = os.environ.get("OPENAI_API_KEY")
def generate_gpt3_response(user_text, messages=[], print_output=False):
    completions = openai.Completion.create(
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        messages=messages,           # A list of previous messages
        temperature=0.5,            # Level of creativity in the response
        prompt=user_text,           # What the user typed in
        max_tokens=100,             # Maximum tokens in the prompt AND response
    )

    # Displaying the output can be helpful if things go wrong
    if print_output:
        print(completions)

    # Return the first choice's text
    return completions.choices[0].text
prompt = """You are a chatbot having a conversation with a human.
User: {query}
Chatbot: {response}"""
messages=[]
while True:
    query = input("User: ")
    if query == "exit":
        break
    resp=generate_gpt3_response(query,messages)
    print(prompt.format(query=query,response=resp))
    messages.append({"role": query, "content": resp})