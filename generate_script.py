import openai

openai.api_key = "你的API密钥"

def generate_script(theme):
    prompt = f"""
你是一个推理小说大师，请根据下面的风格生成一个剧本杀故事大纲。

风格：{theme}

要求：
- 包括故事背景、角色设定、案件起因、线索、真相。
- 使用简洁明了的语言。
- 最好控制在 400-600 字以内。

请开始输出：
"""

    response = openai.chat.completions.create(
        model="gpt-4",  # 或 "gpt-3.5-turbo"
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    user_theme = input("请输入你喜欢的风格（例如：中世纪奇幻、悬疑校园、未来科幻等）：")
    script = generate_script(user_theme)
    print("\n🎭 你的剧本杀故事大纲：\n")
    print(script)