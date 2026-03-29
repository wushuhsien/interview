from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import os
from gtts import gTTS

from positions import positions
from ai_module import generate_question
from db import insert_generated_question, insert_answer

app = Flask(__name__)

# ===== 模擬題庫 =====
questions = [
    "請先做自我介紹12",
    "你的優點是什麼？",
    "你的缺點是什麼$$？"
]

# ===== 面試狀態 =====
current_index = 0
answers = [] # 存每題回答

# ===== 全域情緒統計 =====
emotion_counts = {"快樂":0, "平靜":0, "傷心":0, "生氣":0, "驚訝":0}

# ===== 路由設定 =====
# ===== 登入 =====
@app.route('/')
def home():
    return redirect(url_for('student_start'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('student_start'))
    return render_template('login.html')

# ===== 註冊 =====
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register-1')
def register_step2():
    return render_template('register-1.html')

# ===== 學生主頁 =====
@app.route('/student_start')
def student_start():
    return render_template('student_start.html')

# ===== 學生基本資料 =====
@app.route('/student_information')
def student_information():
    return render_template('student_information.html')

# ===== 學生上傳履歷 =====
@app.route('/student_resume')
def student_resume():
    return render_template('student_resume.html')

# ===== 學生面試紀錄 =====
@app.route('/student_interview_history')
def student_interview_history():
    return render_template('student_interview_history.html')

# ===== 學生問題紀錄 =====
@app.route('/student_question')
def student_question():
    return render_template('student_question.html')

# ===== 學生問題紀錄 =====
@app.route('/student_question_history')
def student_question_history():
    return render_template('student_question_history.html')






# ===== 面試頁面 =====
@app.route('/mock_interview')
def mock_interview():
    return render_template('index.html')

# ===== 重設面試 =====
@app.route('/reset')
def reset():
    global emotion_counts, current_index, answers
    current_index = 0
    answers = []
    for key in emotion_counts:
        emotion_counts[key] = 0
    return {"status":"reset ok"}

# ===== 取得下一題並生成語音 =====
@app.route('/next_question')
def next_question():
    global current_index
    if current_index >= len(questions):
        return jsonify({"end": True})

    q_text = questions[current_index]
    current_index += 1
    filename = f"normal_q_{current_index}.mp3"
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_folder = os.path.join(base_dir, "static", "audio")
    os.makedirs(audio_folder, exist_ok=True)
    filepath = os.path.join(audio_folder, filename)

    # 生成語音 (gTTS)
    tts = gTTS(text=q_text, lang="zh-TW")
    tts.save(filepath)

    import time
    # 加入 ?v={time.time()} 讓瀏覽器強制重新讀取，不要用舊快取
    return jsonify({
        "question": q_text,
        "tts": f"/static/audio/{filename}?v={int(time.time())}",
        "end": False
    })

# ===== 儲存學生回答 =====
@app.route('/save_answer', methods=['POST'])
def save_answer():
    global answers
    data = request.json
    answer_text = data.get("answer", "").strip()
    if not answer_text:
        return jsonify({"status": "skip"})
    
    if len(answers) < len(questions):
        question_text = questions[len(answers)]
        answers.append({"question": question_text, "answer": answer_text})
    return jsonify({"status": "ok"})

# ===== 表情分析(共用API) =====
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    emotion_key = data.get("emotion", "neutral")
    mapping = {"happy":"快樂", "neutral":"平靜", "sad":"傷心", "angry":"生氣", "surprise":"驚訝"}
    emotion = mapping.get(emotion_key, "平靜")
    emotion_counts[emotion] += 1
    return jsonify({"emotion": emotion})

# ===== 取得報告數據(共用API) =====
@app.route('/report')
def report():
    return jsonify(emotion_counts)

# ===== 下載文字報告 =====
@app.route('/download_report')
def download_report():
    content = ""
    for i, qa in enumerate(answers, start=1):
        content += f"第{i}題：{qa['question']}\n回答：{qa['answer']}\n{'-'*40}\n"
    return Response(content, mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=interview_report.txt"})









# ===== 題目分類 =====
categories = [
    "自我介紹類",
    "求職動機類",
    "能力與經驗類",
    "情境題",
    "專業技能題目",
    "未來規劃類",
    "壓力/個性測試題",
    "結尾問題"
]

# ===== 面試狀態 =====
current_identity = None
current_position = None

# ===== AI題目練習面試頁面 =====
@app.route('/ai_practice')
def ai_practice():
    return render_template('ai_practice.html')

# ===== 取得職群 =====
@app.route('/positions')
def get_positions():
    return jsonify(positions)

# ===== 設定面試身份與職位 =====
@app.route('/set_interview', methods=['POST'])
def set_interview():
    global current_identity, current_position, current_index
    data = request.json
    current_identity = data.get("identity")
    current_position = data.get("position")
    current_index = 0
    return jsonify({"status":"ok"})

# ===== 重設面試 =====
@app.route('/ai_reset')
def ai_reset():
    global emotion_counts, current_index
    current_index = 0
    for key in emotion_counts:
        emotion_counts[key] = 0
    return {"status":"ai reset ok"}

# ===== AI 取得下一題 =====
@app.route('/ai_next_question')
def ai_next_question():
    global current_index
    if current_index >= len(categories):
        return jsonify({"end": True})

    category = categories[current_index]

    # 最後一題固定
    if category == "結尾問題":
        q_text = "你有沒有問題想問我們公司？"
    else:
        q_text = generate_question(current_identity, current_position, category)

    # 記錄到資料庫
    question_id = insert_generated_question(current_identity, current_position, category, q_text)

    current_index += 1

    # ===== 生成語音 =====
    filename = f"ai_q_{current_index}.mp3"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_folder = os.path.join(base_dir, "static", "audio")
    os.makedirs(audio_folder, exist_ok=True)
    filepath = os.path.join(audio_folder, filename)

    tts = gTTS(text=q_text, lang="zh-TW")
    tts.save(filepath)

    import time
    # 加入 ?v={time.time()} 防止快取錯誤
    return jsonify({
        "question": q_text,
        "category": category,
        "question_id": question_id,
        "tts": f"/static/audio/{filename}?v={int(time.time())}",
        "end": False
    })
    
# ===== 使用者回答提交 =====
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    answer = data.get("answer")
    question_id = data.get("question_id")
    if answer and question_id:
        insert_answer(question_id, answer)
        return jsonify({"status":"ok"})
    return jsonify({"status":"error"})



























if __name__ == "__main__":
    app.run(debug=True, port=5000)