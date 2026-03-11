from flask import Flask

app = Flask(__name__)

# 導入並註冊 blueprint
from routes.login import login_bp
from routes.start import start_bp
from routes.register import register_bp

app.register_blueprint(login_bp)
app.register_blueprint(start_bp)
app.register_blueprint(register_bp)

if __name__ == "__main__":
    app.run(debug=True)

    # python login.py