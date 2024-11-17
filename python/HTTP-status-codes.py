# what is the difference between 401 and 403 status codes?

# 401 Unauthorized is when the user is not authenticated. => it means the user is not logged in or the token is expired
# 403 Forbidden is when the user is authenticated but not authorized to access the resource. => it means for example only admins can access this resource not normal users.

from flask import Flask, session, jsonify

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session

@app.route('/protected')
def protected():
    if session.get('user', {}).get('is_authenticated', False):
        return "OK", 200
    else:
        return "Not authorized", 401

@app.route('/admin')
def admin():
    user = session.get('user', {})
    if user.get('is_authenticated', False):
        if user.get('is_admin', False):
            return "OK", 200
        else:
            return "Not in admin group", 403
    else:
        return "Not authorized", 401

@app.route('/login/admin')
def login_admin():
    # session is saved in memory by default, it will be lost when the server restarts
    session['user'] = {"is_authenticated": True, "is_admin": True}
    return "OK", 200

@app.route('/login/user')
def login_user():
    session['user'] = {"is_authenticated": True, "is_admin": False}
    return "OK", 200


@app.route('/session')
def session_info():
    return jsonify(session.get('user', {})), 200

@app.route('/logout')
def logout():
    session.clear()
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
