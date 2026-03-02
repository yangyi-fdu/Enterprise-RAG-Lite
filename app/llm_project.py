from openai import OpenAI

# 初始化客户端
# ⚠️ 注意：这里要把 "sk-..." 换成你刚才那个真实的、充了10块钱的 API Key 哦！
client = OpenAI(
    api_key="sk-d73a217698e04651959a4e6f38dd80c0", 
    base_url="https://api.deepseek.com"
)

def chat_with_llm(messages: list) -> str:
    """
    职责：只负责和底层大模型打交道。
    接收设定好的消息列表，返回 AI 的回答文本。
    """
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content
