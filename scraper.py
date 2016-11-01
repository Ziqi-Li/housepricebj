#Ziqi Li
#liziqi1992@gmail.com
#Retrieving listed used house price in Beijing from -
#www.lianjia.com, one of the biggest property agents.

from bs4 import BeautifulSoup
import re
import urllib.request
import pandas as pd

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
        curHome['link'] = data[i].find("div", { "class" : "houseInfo" }).a['href']
        contentLocation = urllib.request.urlopen(curHome['link']).read()
        soupLocation = BeautifulSoup(contentLocation)
        curHome['lon'] = float(soupLocation.find_all("script", { "type" : "text/javascript" })[1].string.split("resblockPosition:")[1].split("'")[1].split(",")[0])
        curHome['lat'] = float(soupLocation.find_all("script", { "type" : "text/javascript" })[1].string.split("resblockPosition:")[1].split("'")[1].split(",")[1])
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
        print (curHome['address'],curHome['lon'],curHome['lat'])
        house.append(curHome)
    return house



#Retrive house price for each price categories.
#Maximum of 100 pages per category.
#Maximum 30 listings per page.
house = [] #List of pd dfs
baseurl = "http://bj.lianjia.com/ershoufang/"
for i in range(8,10):
    for j in range(20,100):
        curURL = baseurl + "p" + str(i+1) + "/pg" + str(j+1) + "/"
        print ("Start retrieving: " + curURL)
        retrivedPage = retriveData(curURL)
        house.append(pd.DataFrame(retrivedPage))
        print ("Successfully retrived: " + str(len(retrivedPage)))
        print ("Current Total:"  + str(len(house)))

#Save to csv file
df = pd.concat(house)
df = df.drop_duplicates()
df.to_csv('house_compelete.csv', index=False)
