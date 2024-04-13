import openai

openai.api_key = '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'

def chat_with_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": ""}
        ]
    )

    try:
        assistant_message = response.choices[0].message.content.strip()
        print(assistant_message)  
        return assistant_message
    except Exception as e:
        print("Error accessing response", e)
        print("Response object:", response)
        return "I'm sorry, but I couldn't process your request at the moment."


def main():
    topic = input("Enter the topic: ")
    paragraph = chat_with_openai(f"generate a 200 words paragraph about {topic}")
    print(paragraph)

if __name__ == "__main__":
    main()
