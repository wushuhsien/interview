import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_question(identity, position, category):
    prompt = f"""
你是一位專業面試官，請幫我以繁體中文生成一題約20字數的面試問題。
身份: {identity}
應徵職位: {position}
題目類別: {category}
要求: 問題清楚、專業、適合該身份及職位。
只簡短輸出題目文字。
"""
    from google.generativeai import GenerativeModel
    model = GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()