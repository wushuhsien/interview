from flask import Blueprint, request

start_bp = Blueprint('start', __name__)

@start_bp.route('/start', methods=['POST'])
def start():
    username = request.form['username']
    return f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>面試流程模擬與評估系統｜開始面試</title>
    <style>
        body {{
            font-family: "Microsoft JhengHei", sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #f3e9dc, #e2d1c3);
        }}

        /* 固定頂部導航列 */
        .top-menu {{
            position: fixed;
            top: 0;
            left: 0;
            width:100%;
            height: 80px;
            background-color: #2a5298;
            display: flex;
            align-items: center;
            padding: 0 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            z-index: 1000;
        }}

        .top-menu h1 {{
            color: #ffffff;
            font-size: 22px;
            margin: 0;
            letter-spacing: 1px;
            font-weight: 600;
            cursor: pointer;
        }}

        .top-menu h1:hover {{
            color: #e8f3ff;
        }}

        /* 右側功能區 */
        #top-right-box {{
            display: flex;
            align-items: center;
            gap: 5px;
            margin-left: auto;  /* 保持靠右 */
            margin-right: 50px; /* 往左偏移 20px，可調整數值 */
            position: relative;
        }}

        .cart-container, .dropdown {{
            color: white;
            cursor: pointer;
        }}

        .dropbtn {{
            background: #e0e8ff;       /* 藍色系，和導航列搭配 */
            border: none;
            cursor: pointer;
            padding: 6px 12px;         /* 上下 6px，左右 12px */
            border-radius: 6px;        /* 小圓角 */
            color: #000000;            /* 文字黑色 */
            font-weight: 500;
            transition: all 0.2s ease-in-out; /* 平滑過渡 */
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .dropbtn:hover {{
            background: #2a4290;        /* hover 顏色加深 */
            color: #ffffff; 
            box-shadow: 0 2px 6px rgba(0,0,0,0.25); /* 小陰影 */
        }}

        .dropbtn i {{
            font-size: 20px;           /* 調整圖標大小 */
            color: #ffffff;            /* 保持白色 */
        }}

        .dropdown-content {{
            display: none;
            position: absolute;
            flex-direction: column;  /* 垂直排列 */
            right: 0;
            background-color: #ffffff;
            min-width: 150px;
            box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
            z-index: 1001;
            border-radius: 5px;
            overflow: hidden;
        }}

        .dropdown-content button {{
            width: 100%;
            padding: 10px;
            border: none;
            background: none;
            text-align: left;
            cursor: pointer;
        }}

        .dropdown-content button:hover {{
            background-color: #e0e8ff;
        }}

        .sub-dropdown {{
            display: none;
            flex-direction: column;  /* 子選單也垂直排列 */
            background-color: #f9faff;
            border-left: 3px solid #4a90e2;
        }}

        .sub-dropdown input[type="button"] {{
            padding-left: 20px;
        }}

        .content {{
            margin-top: 90px; /* 避免內容被固定頂欄蓋住 */
            padding: 20px;
        }}

        /* 按鈕置右 */
        .menu-items {{
            margin-left: auto;
            display: flex;
            align-items: center;
        }}

        /* 主按鈕 */
        .menu-item {{
            position: relative;
            padding: 14px 18px;
            color: #ffffff;
            cursor: pointer;
            border-radius: 8px;
            margin-left: 15px;
            transition: all 0.25s ease;
            font-size: 15px;
            background: #4A90E2;
            opacity: 0.95;
        }}

        .menu-item:hover {{
            background: #357ABD;
            box-shadow: 0 4px 12px rgba(53, 122, 189, 0.45);
            transform: translateY(-1px);
        }}

    </style>
    <script>
        function toggleDropdown() {{
            var dropdown = document.getElementById("myDropdown");
            dropdown.style.display = dropdown.style.display === "flex" ? "none" : "flex";
        }}

        function toggleSubMenu(event) {{
            // 防止點擊子選單時觸發 window.onclick
            event.stopPropagation();
            var submenu = document.getElementById("subMenu");
            submenu.style.display = submenu.style.display === "flex" ? "none" : "flex";
        }}

        // 點擊頁面空白處關閉 dropdown
        window.onclick = function(event) {{
            var dropdown = document.getElementById("myDropdown");
            if (!event.target.closest('.dropdown')) {{
                if (dropdown) dropdown.style.display = "none";
                var submenu = document.getElementById("subMenu");
                if (submenu) submenu.style.display = "none";
            }}
        }}
    </script>
</head>
<body>
    <div class="top-menu">
        <h1 onclick="alert('前往會員首頁')">會員首頁</h1>
        <div class="menu-items">
            <div class="menu-item">面試測驗</div>
        </div>
               
        <div id="top-right-box">
            <div class="dropdown">
                <button class="dropbtn" onclick="toggleDropdown()">歡迎 {username} !</button>
                <div id="myDropdown" class="dropdown-content">
                    <button onclick="toggleSubMenu(event)">個人設定 ▼</button>
                    <div id="subMenu" class="sub-dropdown">
                        <button onclick="alert('前往基本資料')">基本資料</button>
                        <button onclick="alert('前往面試紀錄')">面試紀錄</button>
                    </div>
                    <button onclick="alert('前往問題頁面')">問題</button>
                    <button onclick="alert('登出')">登出</button>
                </div>
            </div>
        </div>
                
    </div>

    <div class="content">
        <h1>開始面試</h1>
        <p>歡迎 {username} 進入面試頁面</p>
    </div>
</body>
</html>
"""