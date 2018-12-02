import socket, time, sys, json, pymongo, datetime
from pymongo import *
import unittest

#myClient = pymongo.MongoClient("mongodb://localhost:27017/")
#myDataBase = myClient["mydatabase"]
#myCollection = myDataBase["fishData"]

toCommIP = "169.254.0.2"
thisIP = "169.254.187.140"

toCommPort = 5001
fromCommPort = 5000

toCommAddress = (toCommIP, toCommPort)
fromCommAddress = (thisIP, fromCommPort)

toCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromCommSocket.bind(fromCommAddress)

#Establish connection to database
client = MongoClient('mongodb://Sahil:Sahil_742995@ds139844.mlab.com:39844/aqua')
db = client.aqua
posts = db.posts

updateDelay = 5
updateCounter = 500
appPollTime = 5

def processData(packet):
    #loadData(packet)

    data = json.loads(packet) #data is a dict, keys: data, temp, level, overflow
    tempRead = data['temp']
    level = data['level']
    over = data['overflow']
    instruction = data["data"]
    print(str(tempRead) + " " + str(level) + " " + str(over))

    tempRead = tempRead /1024 * 5000
    temp = tempRead / 10

    over = over * 4 / 600
    level = level * 4 / 600

    if(level <= 2):
        instruction = 2
        if(over >= 1):
            instruction = 3
    elif(over >= 1):
        instruction = 4

    update(temp,level,over)
    return {"data":instruction, "temp":temp, "level":level, "overflow":over}


def loadData(packet):
    a
    #myDict = json.loads(packet)
    #myDict["data"] = datetime.datetime.now().strftime("%d%m%Y")
    #myCollection.insert_one(myDict)
def getPastData(date):
    a

def getCurrentState():
    toSend = {"data":5}
    toCommSocket.sendto(json.dumps(toSend).encode(), toCommAddress)

if __name__ == "__main__":
    #for i in range(5):
    while True:
        if(updateCounter >= updateDelay):
            getCurrentState()
            print("Sending current state request")
            fromCommSocket.settimeout(None)
            received, add = fromCommSocket.recvfrom(2048)
            fromComm = json.loads(received.decode())
            print("Received current state: " + str(fromComm))
            outData = processData(received)
            #loadData(outData)
            toCommSocket.sendto(json.dumps(outData).encode(), toCommAddress)
            print("Sending processed data now")
            updateCounter = 0

        try:
            print("Polling for app request")
            fromCommSocket.settimeout(appPollTime)
            appData, add2 = fromCommSocket.recvfrom(2048)
            fromCommApp = json.loads(appData.decode())

            print("Received Test Sending back now")
            toCommSocket.sendto(getPastData(fromCommApp), toCommAddress)
        except:
            print("No app request was made")
        finally:
            updateCounter += updateDelay

def update(temp,level,over):
    
    postTest_data = {
        'Temperature' : temp,
        'waterLevel' : level,
        'overflowLevel' : over
    }
    if(test(temp, level, over))
        store(postTest_data)
                                                                
def test(temperature, waterLvl, ovrflowLvl):
    assert(waterLvl > 0),"waterLevel cant be negative"
    assert(temperature > 0),"temperature cant be negative"
    assert(ovrflowLvl > 0),"temperature cant be negative"

    assert(waterLvl < 7), "hardware error, sensor range 0-4 cm"
    assert(temperature < 40),"hardware error,sensor range 0-40celcius"
    assert(ovrflowLvl< 7), "hardware error, sensor range 0-4 cm"

    assert(waterLvl != " "),"cannot insert null value"
    assert(temperature != " "), "cannot insert null value"
    assert(ovrflowLvl!= " "), "cannot insert null value"
    print("Data is checked and is okay to store")
    return true

def store(data):
    result = posts.insert_one(data)
    print('One post: {0}'.format(result.inserted_id))
    retrived_posts = db.posts
    for document in retrived_posts.find():
        print(document)
    print("data was stored without any errors")




