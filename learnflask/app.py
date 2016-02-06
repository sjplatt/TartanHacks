from flask import Flask, render_template, request, redirect, url_for, abort, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')

@app.route('/message')
def message():
    if not 'username' in session:
        return abort(403)
    return render_template('message.html', username=session['username'], 
                                           message=session['message'])


if __name__ == '__main__':
    app.run()