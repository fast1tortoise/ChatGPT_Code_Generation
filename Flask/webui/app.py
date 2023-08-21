from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 设置一个用于加密session的密钥

# 模拟用户数据库，实际使用时可以连接真实的数据库
users = {
    "user1": {"password": "password1", "background": "background1.jpg"},
    "user2": {"password": "password2", "background": "background2.jpg"},
}

# 路径配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json', 'jpg', 'jpeg', 'png', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if username in users and users[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        
        return "Invalid login credentials. Please try again."
    
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    user_background = users[username]["background"]
    
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
    
    return render_template("dashboard.html", username=username, background=user_background)

if __name__ == "__main__":
    app.run(debug=True)
