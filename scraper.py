#Ziqi Li
#liziqi1992@gmail.com
#Retrieving listed used house price in Beijing from -
#www.lianjia.com, one of the biggest property agents.

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
        curHome['totalPrice'] = data[i].find("div",{"class":"totalPrice"}).span.string #Total price in RMB
        unitPriceStr = data[i].find("div",{"class":"unitPrice"}).span.string
        curHome['unitPrice'] = int((re.findall('\d+', unitPriceStr ))[0]) #Unit price RMB/m2
        curHome['address'] = data[i].find("div",{"class":"houseInfo"}).a.string #Address in Chinese
        houseInfo = data[i].find("div",{"class":"houseInfo"}).contents[2].string
        curHome['bedroom'] = int((re.findall('\d+', houseInfo.strip(",").strip(" ").split("|")[1] ))[0]) #Number of bedrooms
        curHome['livingroom'] = int((re.findall('\d+', houseInfo.strip(",").strip(" ").split("|")[1] ))[1]) #Number of livingrooms
        curHome['area'] = int((re.findall("\d+", houseInfo.strip(",").strip(" ").split("|")[2] ))[0]) #Total area in m2
        curHome['direction'] = houseInfo.strip(",").strip(" ").split("|")[3] #Direction of house in Chinese
        curHome['furnished'] = houseInfo.strip(",").strip(" ").split("|")[4] #Furnishing levels in Chinese
        curHome['elevator'] = houseInfo.strip(",").strip(" ").split("|")[5] #Whether has elevator
        positionInfo = data[i].find("div",{"class":"positionInfo"}).contents[1]
        try:
            curHome['age'] = int(re.findall('\d+', positionInfo.split(" ")[2] )[0]) # Built year
        except:
            curHome['age'] = "NA"
        try:
            curHome['totalFloor'] = int(re.findall('\d+', positionInfo.split(" ")[0] )[0]) #Total floors for the building
        except:
            curHome['totalFloor'] = "NA"
        try:
            curHome['floor'] = positionInfo.split(" ")[0].split("(")[0] # Floor of the home
        except:
            curHome['totalFloor'] = "NA"
        house.append(curHome)
    return house



#Retrive house price for each price categories.
#Maximum of 100 pages per category.
#Maximum 30 listings per page.
house = [] #List of dictionaries
baseurl = "http://bj.lianjia.com/ershoufang/"
for i in range(0,10):
    for j in range(0,100):
        curURL = baseurl + "p" + str(i+1) + "/pg" + str(j+1) + "/"
        print ("Start retrieving: " + curURL)
        retrivedPage = retriveData(curURL)
        house+=retrivedPage
        print ("Successfully retrived: " + str(len(retrivedPage)))
        print ("Current Total:"  + str(len(house)))

#Save to csv file
#keys = hosue.key
with open('./house1.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(house)
