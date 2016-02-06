from flask import Flask, render_template, request, redirect, url_for, abort, session
import api
from scottylabparser import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';
app.config['id'] = 0
app.config['USERNAME'] = 'test'
app.config['PASSWORD'] = 'test'

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "at") as f:
        f.write(contents)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/request_food', methods = ['GET'])
def request_food():
    restaurants = api.get_restaurants()
    rest_dict = {}
    for restaurant in restaurants:
        rest_dict[restaurant] = api.parse_restaurant(restaurant)
    
    return render_template('request_food.html', restaurants=restaurants,
        rest_dict=rest_dict,locations=api.get_location_list())

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['logged_in'] = True
        session['user_logged_in'] = username
        writeFile('data/users.txt', '%s\n' % (username))
        writeFile('data/%s.txt' % (username), 'password:%s' % password)
        return redirect(url_for('request_food'))
    return render_template('signup.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        checkFile = False
        users = readFile('data/users.txt')
        for user in users.splitlines():
            print(user, username)
            if user ==  username:
                checkFile = True
                break
        if checkFile:
            text = readFile('data/%s.txt' % (username))
            print(text)
            print(hash(password))
            for line in text.splitlines():
                [key, val] = line.split(":")
                if key == "password":
                    passwordHash = (val)
                    break
            if passwordHash == (password):
                session['logged_in'] = True
                session['user_logged_in'] = username
                return redirect(url_for('request_food'))
            else:
                error = 'Invalid password'
        else:
            error = 'Invalid username'
    return render_template('login.html')

@app.route('/my_auction',methods = ['POST'])
def my_auction():
    restaurant = request.form['restaurant']
    category = request.form['category']
    item,price = request.form['item'].split(',')
    auction_length = request.form['auction_length']
    location = request.form['location']
    order = restaurant + ": " + category + ": " + item + ": " + price

    aid = api.create_auction(session['user_logged_in'],order,price,auction_length,location)
    bids = api.get_bids(aid)
    return render_template('my_auction.html',username=session['user_logged_in'],order=order,location=location,aid=aid,bids=bids)

@app.route('/auction_list', method = ['GET'])
def auction_list():
    auctionList = []
    return render_template('auction_list.html', auctionList)

@app.details('/auction_details', methods = ['POST'])
def auction_details():
    return render_template('auction_details.html')


# @app.route('/message')
# def message():
#     if not 'username' in session:
#         return abort(403)
#     return render_template('message.html', username=session['username'], 
#                                            message=session['message'])

if __name__ == '__main__':
    app.run()
# from flask import Flask, render_template, request, redirect, url_for, abort, session

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'F34TF$($e34D';
# app.config['USERNAME'] = 'test'
# app.config['PASSWORD'] = 'test'

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/test', methods = ['GET'])
# def test():
#     return render_template('test.html')

# @app.route('/signup', methods = ['GET', 'POST'])
# def signup():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             return redirect(url_for('test'))
#     return render_template('signup.html')

# @app.route('/login', methods = ['GET','POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             return redirect(url_for('test'))
#     return render_template('login.html')


# # @app.route('/message')
# # def message():
# #     if not 'username' in session:
# #         return abort(403)
# #     return render_template('message.html', username=session['username'], 
# #                                            message=session['message'])

# if __name__ == '__main__':
#     app.run()