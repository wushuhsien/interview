from flask import Blueprint

register_bp = Blueprint('register', __name__)

@register_bp.route('/register')
def register():

    # message = ""

    # if request.method == "POST":

    #     username = request.form["username"]
    #     password = request.form["password"]
    #     confirm = request.form["confirm_password"]
    #     role = request.form["role"]

    #     # 密碼確認
    #     if password != confirm:
    #         message = "密碼與確認密碼不一致！"

    #     # 帳號是否存在
    #     elif username in accounts:
    #         message = "帳號已存在！"

    #     else:
    #         # 存到 session
    #         session["reg_username"] = username
    #         session["reg_password"] = password
    #         session["reg_role"] = role

    #         return redirect("/register_step2")

    return f"""
<!DOCTYPE html>
<html lang="zh-Hant">

<head>
<meta charset="UTF-8">
<title>註冊帳號</title>

<style>

body {{
font-family:"Microsoft JhengHei", sans-serif;
background: linear-gradient(135deg,#f3e9dc,#e2d1c3);
margin:0;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
}}

.container {{
background:white;
padding:45px 55px;
border-radius:18px;
box-shadow:0 10px 30px rgba(0,0,0,0.2);
width:420px;
text-align:center;
}}

.system-title {{
font-size:26px;
font-weight:bold;
color:#1e3c72;
margin-bottom:10px;
}}

h1 {{
margin-bottom:25px;
}}

input, select {{
width:100%;
padding:12px;
margin-top:10px;
border-radius:10px;
border:1px solid #ccc;
font-size:16px;
}}

button {{
margin-top:20px;
width:100%;
padding:12px;
background:#2a5298;
color:white;
border:none;
border-radius:10px;
font-size:16px;
cursor:pointer;
}}

button:hover {{
background:#1e3c72;
}}

.login-btn {{
margin-top:15px;
background:#f0f4ff;
color:#2a5298;
border:1px solid #2a5298;
}}

.login-btn:hover {{
background:#e0e8ff;
}}

.error {{
color:red;
margin-top:10px;
}}

</style>
</head>

<body>

<div class="container">

<div class="system-title">面試流程模擬與評估系統</div>

<h1>註冊帳號</h1>

<form method="POST">

<input type="text" name="username" placeholder="帳號" required>

<input type="password" name="password" placeholder="密碼" required>

<input type="password" name="confirm_password" placeholder="確認密碼" required>

<select name="role">
<option value="0">會員</option>
<option value="1">管理員</option>
</select>

<button type="submit">下一頁</button>

</form>

<button class="login-btn" onclick="window.location.href='/'">返回登入</button>

<div class="error">{message}</div>

</div>

</body>
</html>
"""


# @app.route("/register_step2")
# def register_step2():

#     username = session.get("reg_username")

#     return f"""
#     <h1>註冊第2步</h1>
#     <p>帳號：{username}</p>
#     <p>（這裡可以繼續填寫個人資料）</p>
#     """

