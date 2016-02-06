import datetime
import os
from dateutil import parser

class MenuItem:
    def __init__(self,name,price,options):
        self.name = name
        self.price = price
        self.options = options

    def __repr__(self):
        return self.name + " " + self.price + " " + str(self.options)


def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def writeFileAppend(path,contents):
    with open(path,"at") as f:
        f.write(contents)

#Parse restaurant information
def parse_restaurant(name):
    read = readFile("data/" + name + ".txt")
    lines = read.split('\n')
    result = {lines[0] : []}
    cur_cat = lines[0]
    skip_line = False
    count = 0
    cur_name = ""
    cur_price = ""
    cur_options = []

    for index,line in enumerate(lines[1:]):
        if line == '':
            skip_line = True
        elif skip_line:
            cur_cat = line
            skip_line = False
        else:
            if count == 0:
                cur_name = line
                count+=1
            elif count == 1:
                cur_price = line
                count+=1
            elif count == 2:
                nl = line[1:-1].split(",")
                cur_options = list(nl)
                myItem = MenuItem(cur_name,cur_price,cur_options)
                cur_name = ""
                cur_price = ""
                cur_options =[]
                count = 0
                if not cur_cat in result:
                    result[cur_cat] = []
                result[cur_cat].append(myItem)
                count=0
    return result

def get_restaurants():
    read = readFile("data/restaurants.txt")
    lines = read.split('\n')
    result = []
    for line in lines:
        result.append(line)
    return result

######MAIN API#############

def find_highest_offset():
    res = []
    for file in os.listdir("./data/bidding"):
        if file.endswith(".txt"):
            if "auction" in file[:7]:
                res.append(int(file[7:-4]))

    return max(res)+1

def create_auction(userid, order, price, wait, loc):
    print("START")
    timestamp = datetime.datetime.time(datetime.datetime.now())
    output = ""
    output+=str(userid) + "\n"
    output+=str(order) + "\n"
    output+=str(price) + "\n"
    output+=str(timestamp) + "\n"
    output+=str(wait) + "\n"
    output+=str(loc) + "\n"

    offset = find_highest_offset()
    writeFile("./data/bidding/auction"+str(offset)+".txt",output)
    add_to_current_auctions(offset)
    return offset

def add_to_current_auctions(id):
    writeFileAppend("./data/bidding/open_auctions.txt",str(id) + "\n")

def check_current_auctions():
    res = readFile("./data/bidding/open_auctions.txt").split("\n")
    keep = []
    remove = []
    for line in res:
        if(line != "" and line != "\n"):
            auc = readFile("./data/bidding/auction"+line+".txt").split("\n")
            cur_time = datetime.datetime.now()
            wait_time = auc[4]
            timestamp = parser.parse(auc[3])+datetime.timedelta(minutes=int(wait_time))
            if(timestamp > cur_time):
                keep.append(line)
            else: remove.append(line)
    
    result = ""
    for k in keep:
        result+=k + "\n"
    writeFile("./data/bidding/open_auctions.txt",result)

    result = ""
    for r in remove:
        result+=r + "|\n"
    writeFileAppend("./data/bidding/closed_auctions.txt",result)

def is_current_auction(id):
    res = readFile("./data/bidding/open_auctions.txt").split("\n")
    for line in res:
        if line == str(id):
            return True
    return False

#Form: bid_user:
def add_bid_to_auction(id, bid_user_id, price,location):
    timestamp = datetime.datetime.time(datetime.datetime.now())
    result = str(bid_user_id) + "|" + str(price) + "|" + str(timestamp) + "|" + location + " \n"
    writeFileAppend("./data/bidding/auc_bid" + str(id) + ".txt",result)

def get_bids(id):
    result = []
    try:
        res = readFile("./data/bidding/auc_bid"+str(id)+".txt")
        res = res.split('\n')
        for line in res:
            if line != "" and line != "\n":
                result.append(line.split("|"))
        return result
    except:
        return result

def get_location_list():
    res = readFile("./data/locations.txt").split("\n")
    ret = []
    for line in res:
        ret.append(line)
    return ret

def get_all_active():
    res = readFile("./data/bidding/open_auctions.txt").split("\n")
    answer = []
    for line in res:
        if line != '':
            answer.append(line)
    return answer

def get_info_auction(id):
    res = readFile("./data/bidding/auction"+str(id) + ".txt")
    return res.split("\n")

#add_bid_to_auction(2,"sjplatt","2")
#create_auction("sjplatt","burrito","6.95","5","resnick")
#create_auction("sjplatt","burrito","6.95","1","resnick")
#check_current_auctions()