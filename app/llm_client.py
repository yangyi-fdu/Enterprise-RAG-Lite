from openai import OpenAI

# ⚠️ 这里记得写你真实的 API Key
client = OpenAI(
    api_key="sk-d73a217698e04651959a4e6f38dd80c0", 
    base_url="https://api.deepseek.com"
)

def chat_with_llm(messages: list) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content
