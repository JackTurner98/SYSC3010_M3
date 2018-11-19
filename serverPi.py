import socket, time, sys, json, pymongo, datetime

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



