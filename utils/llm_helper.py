import ollama

def ask_llm(prompt):

    response = ollama.chat(
        model='tinyllama',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response['message']['content']