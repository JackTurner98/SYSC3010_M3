import socket, time, sys, json, pymongo, datetime

#myClient = pymongo.MongoClient("mongodb://localhost:27017/")
#myDataBase = myClient["mydatabase"]
#myCollection = myDataBase["fishData"]

toCommIP = "localhost"

toCommPort = 5001
fromCommPort = 5000

toCommAddress = (toCommIP, toCommPort)
fromCommAddress = ('localhost', fromCommPort)

toCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


fromCommSocket.bind(fromCommAddress)

updateDelay = 5
updateCounter = 500
appPollTime = 5

def processData(packet):
    #loadData(packet)

    data = json.loads(packet) #data is a dict, keys: data, temp, level, overflow
    temp = data['temp']
    level = data['level']
    over = data['overflow']

    # Any Conversions or units added here
    temp -= 1
    level -= 1
    over += 1

    return {"data":6, "temp":temp, "level":level, "overflow":over}


def loadData(packet):
    a
    #myDict = json.loads(packet)
    #myDict["data"] = datetime.datetime.now().strftime("%d%m%Y")
    #myCollection.insert_one(myDict)

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
            toCommSocket.sendto(json.dumps(outData).encode(), toCommAddress)
            print("Sending processed data now")
            updateCounter = 0

        try:
            print("Polling for app request")
            fromCommSocket.settimeout(appPollTime)
            appData, add2 = fromCommSocket.recvfrom(2048)

            fromCommApp = json.loads(appData.decode())
            print("Received Test Sending back now")
            toCommSocket.sendto(appData, toCommAddress)
        except:
            print("No app request was made")
        finally:
            updateCounter += updateDelay



