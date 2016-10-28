from bs4 import BeautifulSoup
import re
import urllib.request

def retriveData(url):
    house = []
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content)
    print ("Soup Loaded")
    data = soup.find_all("div", { "class" : "info clear" })
    for i in range(0,len(data)):
        curHome = {}
        curHome['title'] = data[i].a.string
        curHome['totalPrice'] = data[i].find("div",{"class":"totalPrice"}).span.string
        curHome['totalPrice'] = data[i].find("div",{"class":"totalPrice"}).span.string
        unitPriceStr = data[i].find("div",{"class":"unitPrice"}).span.string
        curHome['unitPrice'] = int((re.findall('\d+', unitPriceStr ))[0])
        curHome['address'] = data[i].find("div",{"class":"houseInfo"}).a.string
        houseInfo = data[i].find("div",{"class":"houseInfo"}).contents[2].string
        curHome['bathroom'] = int((re.findall('\d+', houseInfo.strip(",").strip(" ").split("|")[1] ))[0])
        curHome['livingroom'] = int((re.findall('\d+', houseInfo.strip(",").strip(" ").split("|")[1] ))[1])
        curHome['area'] = int((re.findall("\d+", houseInfo.strip(",").strip(" ").split("|")[2] ))[0])
        curHome['direction'] = houseInfo.strip(",").strip(" ").split("|")[3]
        curHome['furnished'] = houseInfo.strip(",").strip(" ").split("|")[4]
        curHome['elevator'] = houseInfo.strip(",").strip(" ").split("|")[5]
        positionInfo = data[i].find("div",{"class":"positionInfo"}).contents[1]
        try:
            curHome['age'] = int(re.findall('\d+', positionInfo.split(" ")[2] )[0])
        except:
            curHome['age'] = "NA"
        try:
            curHome['totalFloor'] = int(re.findall('\d+', positionInfo.split(" ")[0] )[0])
        except:
            curHome['totalFloor'] = "NA"
        try:
            curHome['floor'] = positionInfo.split(" ")[0].split("(")[0]
        except:
            curHome['totalFloor'] = "NA"
        house.append(curHome)
    return house




house = []
baseurl = "http://bj.lianjia.com/ershoufang/"
for i in range(0,9):
    for j in range(0,100):
        curURL = baseurl + "p" + str(i+1) + "/pg" + str(j+1) + "/"
        print ("Start retrieving: " + curURL)
        if (i!=0 and j!=0 and retriveData(curURL) == retrivedPage):
            print ("End of a category found")
            break
        retrivedPage = retriveData(curURL)
        house+=retrivedPage
        print ("Successfully retrived: " + str(len(retrivedPage)))
        print ("Current Total:"  + str(len(house)))
