from flask import Flask, render_template, request, redirect, url_for, abort, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';
app.config['USERNAME'] = 'test'
app.config['PASSWORD'] = 'test'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test', methods = ['GET'])
def test():
    return render_template('test.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('test'))
    return render_template('signup.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('test'))
    return render_template('login.html')


# @app.route('/message')
# def message():
#     if not 'username' in session:
#         return abort(403)
#     return render_template('message.html', username=session['username'], 
#                                            message=session['message'])

if __name__ == '__main__':
    app.run()