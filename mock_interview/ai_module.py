import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_question(identity, position, category):
    prompt = f"""
你是一位專業的企業面試主管。現在你要面試一位「{identity}」，他正在應徵「{position}」。
請針對「{category}」這個類別，生成一題該職位最常被問到的「經典面試問題」。

【要求】：
1. 語氣：自然口語，像真人面試官在聊天，不要太生硬。
2. 內容：必須精準符合「{position}」的職場情境。
3. 優先度：優先選擇該類別中最常見、最必問的題目（例如：{category}如果是自我介紹，就直接問自我介紹）。
4. 長度：約 15~20 字。
5. 限制：只輸出問題文字，不要有標號或額外解釋。

範例參考：
- 若類別是「能力與經驗」，可以問：針對{position}這個角色，你過去最成功的專案經驗是什麼？
- 若類別是「求職動機」，可以問：你為什麼會想來應徵我們公司的{position}，而不是去其他公司？
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=800,
            temperature=0.7,
        )
    )

    return response.text.strip()