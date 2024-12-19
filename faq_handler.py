import openai

def handle_faq(question):
    openai.api_key = "your_openai_api_key"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Provide an insightful answer for a digital marketer's question: {question}",
        max_tokens=150
    )
    return response["choices"][0]["text"].strip()
