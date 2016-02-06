from flask import Flask, render_template, request, redirect, url_for, abort, session
import api
from scottylabparser import *
import random

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
    image = api.get_user_image(session['user_logged_in'])
    return render_template('request_food.html', restaurants=restaurants,
        rest_dict=rest_dict,locations=api.get_location_list(),image=image,
        username=session['user_logged_in'])

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['logged_in'] = True
        session['user_logged_in'] = username
        writeFile('data/users.txt', '%s\n' % (username))
        writeFile('data/%s.txt' % (username), 'password:%s\n' % password)
        rand = random.randint(1,5)
        writeFile('data/%s.txt' % (username), 
            'image:%s' % "image"+str(rand)+".jpg\n")
        return redirect(url_for('request_food'))
    return render_template('signup.html')

@app.route('/login/<chose_id>', methods = ['GET','POST'])
def login(chose_id):
    error = None
    session['chose_id'] = str(chose_id)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        checkFile = False
        users = readFile('data/users.txt')
        for user in users.splitlines():
            if user ==  username:
                checkFile = True
                break
        if checkFile:
            text = readFile('data/%s.txt' % (username))
            for line in text.splitlines():
                [key, val] = line.split(":")
                if key == "password":
                    passwordHash = (val)
                    break
            if passwordHash == (password):
                session['logged_in'] = True
                session['user_logged_in'] = username
                if session['chose_id'] == "1":
                    return redirect(url_for('request_food'))
                else:
                    return redirect(url_for('auction_list'))
            else:
                error = 'Invalid password'
        else:
            error = 'Invalid username'
    return render_template('login.html',chose_id=chose_id)

@app.route('/my_auction',methods = ['POST'])
def my_auction():
    restaurant = request.form['restaurant']
    category = request.form['category']
    item,price = request.form['item'].split(',')
    auction_length = request.form['auction_length']
    location = request.form['location']
    order = restaurant + ": " + category + ": " + item + ": " + price
    image = api.get_user_image(session['user_logged_in'])
    image_map = api.user_image_map()
    print("image map - ", image_map)
    aid = api.create_auction(session['user_logged_in'],order,price,auction_length,location)
    bids = api.get_bids(aid)
    return render_template('my_auction.html',username=session['user_logged_in'],order=order,location=location,aid=aid,bids=bids,images=image,
        image_map=image_map)

@app.route('/auction_list', methods = ['GET'])
def auction_list():
    api.check_current_auctions()
    auctionList = []
    image = api.get_user_image(session['user_logged_in'])
    image_map = api.user_image_map()

    for auctionID in api.get_all_active():
        auctionList.append([auctionID] + api.get_info_auction(auctionID))
    return render_template('auction_list.html', auctionList=auctionList,
        image=image,image_map=image_map,username=session['user_logged_in'])


@app.route('/any_auction/<auction_id>',methods = ['GET','POST'])
def any_auction(auction_id):
    if request.method == 'GET':
        auction_info = api.get_info_auction(auction_id)
        is_self = False
        if auction_info[0] == session['user_logged_in']:
            is_self = True
        username = auction_info[0]
        bids = api.get_bids(auction_id)
        locations = api.get_location_list();
        image = api.get_user_image(session['user_logged_in'])
        image_map = api.user_image_map()
        return render_template('any_auction.html',username=username,
            order=auction_info[1],location=auction_info[5],aid=auction_id,
            bids=bids,is_self=is_self,locations=locations,
            image=image,image_map=image_map)
    
    location = request.form['location']
    price = request.form['price']
    cur_id = session['user_logged_in']
    api.add_bid_to_auction(auction_id,cur_id,price,location)

    return redirect(url_for('any_auction',auction_id=auction_id))


# @app.route('/message')
# def message():
#     if not 'username' in session:
#         return abort(403)
#     return render_template('message.html', username=session['username'], 
#                                            message=session['message'])

if __name__ == '__main__':
    app.run(debug=True)
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