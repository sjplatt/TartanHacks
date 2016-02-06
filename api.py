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

#Parse restaurant information
def parse_restaurant(name):
    read = readFile(name + ".txt")
    lines = read.split('\n')
    result = {lines[0] : []}
    cur_cat = lines[0]
    skip_line = False
    count = 0
    cur_name = ""
    cur_price = ""
    cur_options = []

    for index,line in enumerate(lines[1:]):
        print(result)
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


parse_restaurant("Carnegie Mellon Cafe")
