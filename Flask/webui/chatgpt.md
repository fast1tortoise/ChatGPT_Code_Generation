你的项目涉及到多个方面，包括用户认证、文件处理以及页面样式的变更。我可以为你提供一个基本的框架，帮助你实现这些功能。以下是一个使用Python和Flask实现的简单示例，展示了如何实现你所描述的功能：

首先，确保你已经安装了Flask库。你可以使用以下命令来安装：

```bash
pip install Flask
```

接下来，创建一个名为`app.py`的文件，开始编写你的Flask应用：

```python
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
```

在上述代码中，你需要创建以下文件夹结构：

```
- your_project_folder/
    - app.py
    - templates/
        - login.html
        - dashboard.html
    - uploads/
```

接下来，你需要在`templates`文件夹中创建`login.html`和`dashboard.html`，分别用于登录页面和仪表盘页面的展示。

`login.html`示例：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form method="post">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

`dashboard.html`示例：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <style>
        body {
            background-image: url("static/{{ background }}");
            background-size: cover;
        }
    </style>
</head>
<body>
    <h1>Welcome, {{ username }}!</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".json, .jpg, .jpeg, .png, .mp4" required>
        <button type="submit">Upload</button>
    </form>
</body>
</html>
```

请注意，以上示例中的代码仅为基本的框架，需要你根据实际需求进行修改和扩展。此外，由于涉及到文件上传和用户认证等敏感操作，确保在实际应用中采取适当的安全措施。例如，密码应该进行哈希存储，文件上传可能需要限制文件大小和类型，以防止安全风险。