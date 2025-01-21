from flask import Flask, request, render_template, redirect
import jwt

app = Flask(__name__)

SECRET_KEY = "N0t_th3_5eCReT_K3y"  # Keep your secret key secure

# Load the flag from a file
def get_flag():
    try:
        with open('./flag.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "flag{placeholder_flag}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if username == 'user' and password == 'password':
            role = 'user'
            token = jwt.encode({"username": username, "role": role}, SECRET_KEY, algorithm="HS256")
            
            response = redirect('/community')
            response.set_cookie('auth_token', token)
            return response
        else:
            return render_template('index.html', error="Invalid credentials!")
    return render_template('index.html')

@app.route('/community')
def community():
    token = request.cookies.get('auth_token', '')
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        role = decoded.get("role", "user")
        
        comments = [
            {"author": "admin", "content": "Welcome to the community!"},
            {"author": "admin", "content": "Inspection is going on!"},
            {"author": "admin", "content": "There will be a meetup soon!"}
        ]
        
        # Add the flag as a comment if the user is an admin
        if role == "admin":
            # Add the flag as a comment without the admin's name
            comments.append({"author": "admin", "content": get_flag()})  # Empty author for the flag

        return render_template('community.html', role=role, comments=comments)
    except jwt.DecodeError:
        return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
