import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    except mysql.connector.Error as e:
        print("資料庫連線失敗:", e)
        raise
    

def insert_generated_question(identity, position, category, question_text):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO generated_questions (identity, position, category, question_text) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (identity, position, category, question_text))
    conn.commit()
    question_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return question_id

def insert_answer(question_id, answer_text):

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO interview_answers (question_id, answer_text)
    VALUES (%s, %s)
    """

    cursor.execute(sql, (question_id, answer_text))
    conn.commit()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ 資料庫連線成功！")
        conn.close()

        # 測試插入
        insert_generated_question(
            identity="fresh_graduate",
            position="軟體工程師",
            category="自我介紹類",
            question_text="請簡單介紹自己"
        )
        print("✅ 測試題目成功插入資料庫！")

    except Exception as e:
        print("❌ 發生錯誤:", e)