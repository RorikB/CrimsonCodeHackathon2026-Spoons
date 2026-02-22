import ollama

# Choose a chat-capable model (ensured it is pulled)
# model_name = 'deepseek-r1:latest'
# model_name = 'llama3.2'
model_name = 'gemma3n:e4b'
# model_name = 'gemma3n:e2b'
# model_name = 'gemma3:latest'


with open('systemprompt.txt', 'r', encoding='utf-8') as f:
    system_prompt = f.read()

messages = [
    {"role": "system", "content": system_prompt}
]


response = ollama.chat(model=model_name, messages=messages)
print("Bot:", response.message.content)

# Continue the conversation:
def chat(input):

    if not input:
        return  # exit loop on empty input
    messages.append({"role": "user", "content": input})
    response = ollama.chat(model=model_name, messages=messages)
    answer = response.message.content
    print("Bot:", answer)
    messages.append({"role": "assistant", "content": answer})
    return answer