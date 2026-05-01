import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY 沒有設定")

client = genai.Client(api_key=api_key)

# （可選 debug）
# for m in client.models.list():
#     print(m.name)


def generate_question(identity, position, category):
    prompt = f"""
你是一位專業的企業面試主管。現在你要面試一位「{identity}」，他正在應徵「{position}」。
請針對「{category}」這個類別，生成一題該職位最常被問到的「經典面試問題」。

【要求】：
1. 自然口語
2. 精準符合職位
3. 15~20字
4. 只輸出問題

不要任何解釋或標號。
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=200,
            temperature=0.7,
        )
    )

    return response.text.strip()