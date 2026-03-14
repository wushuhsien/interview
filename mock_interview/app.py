from flask import Flask, render_template, request, redirect, url_for, jsonify
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

# ===== 全域情緒統計 =====
emotion_counts = {"快樂":0, "平靜":0, "傷心":0, "生氣":0, "驚訝":0}

# ===== 首頁登入 =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 取得表單帳號密碼
        username = request.form.get('username')
        password = request.form.get('password')

        # 這裡可以加驗證邏輯，例如比對資料庫
        # if valid_user(username, password):
        #     return redirect(url_for('student_start'))
        # else:
        #     return "帳號或密碼錯誤"

        # 暫時先直接跳轉
        return redirect(url_for('student_start'))

    # GET 時顯示登入頁
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

# ===== 面試頁面 =====
@app.route('/mock_interview')
def mock_interview():
    return render_template('index.html')

# ===== 重設面試 =====
@app.route('/reset')
def reset():
    global emotion_counts, current_index
    current_index = 0
    for key in emotion_counts:
        emotion_counts[key] = 0
    return {"status":"reset ok"}

# ===== 取得下一題 =====
@app.route('/next_question')
def next_question():
    global current_index

    if current_index >= len(questions):
        return jsonify({"end": True})

    q_text = questions[current_index]
    current_index += 1

    filename = f"question_{current_index}.mp3"
    audio_folder = os.path.join("static", "audio")
    os.makedirs(audio_folder, exist_ok=True)
    filepath = os.path.join(audio_folder, filename)

    # 使用 gTTS 生成語音
    tts = gTTS(text=q_text, lang="zh-TW")
    tts.save(filepath)

    return jsonify({
        "question": q_text,
        "tts": f"/static/audio/{filename}",
        "end": False
    })

# ===== 表情分析 =====
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    emotion_key = data.get("emotion", "neutral")
    mapping = {"happy":"快樂","neutral":"平靜","sad":"傷心","angry":"生氣","surprise":"驚訝"}
    emotion = mapping.get(emotion_key,"平靜")
    emotion_counts[emotion] += 1
    return jsonify({"emotion": emotion})

# ===== 面試報告 =====
@app.route('/report')
def report():
    return jsonify(emotion_counts)

if __name__ == "__main__":
    app.run(debug=True)