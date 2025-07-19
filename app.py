from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import random
app = Flask(__name__)
app.secret_key = 'secret123' 
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/visual')
def visual():
    return render_template("visual.html")
@app.route('/start-gesture')
def start_gesture():
    subprocess.Popen(["python", "main.py"])
    return redirect(url_for('success'))
@app.route('/normal')
def normal():
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    session['captcha'] = code
    return render_template("normal.html", captcha=code)
@app.route('/verify', methods=["POST"])
def verify():
    user = request.form["user_input"]
    real = session.get("captcha", "")
    if user == real:
        return redirect(url_for('success'))
    else:
        return render_template("normal.html", captcha=real, error="Wrong captcha try again")
@app.route('/success')
def success():
    return render_template("success.html")
if __name__ == '__main__':
    app.run(debug=True)
