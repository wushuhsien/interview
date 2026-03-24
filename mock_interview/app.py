from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import os
from gtts import gTTS

app = Flask(__name__)

# ===== 模擬題庫 =====
questions = [
    "請先做自我介紹",
    "你的優點是什麼？",
    "你的缺點是什麼？"
]
current_index = 0
answers = [] # 存每題回答

# ===== 全域情緒統計 =====
emotion_counts = {"快樂":0, "平靜":0, "傷心":0, "生氣":0, "驚訝":0}

# ===== 路由設定 =====
@app.route('/')
def home():
    return redirect(url_for('student_start'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('student_start'))
    return render_template('login.html')

@app.route('/student_start')
def student_start():
    return render_template('student_start.html')

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
    filename = f"question_{current_index}.mp3"
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_folder = os.path.join(base_dir, "static", "audio")
    os.makedirs(audio_folder, exist_ok=True)
    filepath = os.path.join(audio_folder, filename)

    # 生成語音 (gTTS)
    tts = gTTS(text=q_text, lang="zh-TW")
    tts.save(filepath)

    return jsonify({
        "question": q_text,
        "tts": f"/static/audio/{filename}?v={current_index}",
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

# ===== 表情分析 =====
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    emotion_key = data.get("emotion", "neutral")
    mapping = {"happy":"快樂", "neutral":"平靜", "sad":"傷心", "angry":"生氣", "surprise":"驚訝"}
    emotion = mapping.get(emotion_key, "平靜")
    emotion_counts[emotion] += 1
    return jsonify({"emotion": emotion})

# ===== 取得報告數據 =====
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)