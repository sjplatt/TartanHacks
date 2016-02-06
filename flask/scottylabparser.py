import json,urllib.request
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def parse_original():
    url = "http://apis.scottylabs.org/dining/v1/locations"
    response = urllib.request.urlopen(url).read().decode('utf8')
    data = json.loads(response)
    if 'locations' in data:
        return data['locations']

#DO NOT CALL AGAIN 
def get_restaurant_list():
    data = parse_original()
    to_write = ""
    for loc in data:
        to_write+=loc['name']+"\n"
    writeFile("restaurants.txt",to_write)
#API FUNCTIONS
def restaurant_dict(name):
    data = parse_original()
    for loc in data:
        if(loc['name'] == name):
            return loc
            break

def restaurant_location(loc):
    return loc['location']

def restaurant_description(loc):
    return loc['description']

def restaurant_times(loc):
    return loc['times']
