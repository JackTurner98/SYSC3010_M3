import socket, time, sys, json

toCommIP = "localhost"

toCommPort = 5001
fromCommPort = 5000

toCommAddress = (toCommIP, toCommPort)
fromCommAddress = (toCommIP, fromCommPort)

toCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromCommSocket.bind(fromCommAddress)

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

    return {"data":data["data"], "temp":temp, "level":level, "overflow":over}


def loadData(Packet):
    a

def getCurrentState():
    print("getting current state")
    toSend = {"data":5}
    toCommSocket.sendto(json.dumps(toSend).encode(), toCommAddress)

if __name__ == "__main__":
    for i in range(5):
        getCurrentState()
        received, add = fromCommSocket.recvfrom(2048)
        fromComm = json.loads(received.decode())
        print("received " + str(fromComm['temp']) + " " + str(fromComm['level']) + " " + str(fromComm['overflow']))
        outData = processData(received)
        toCommSocket.sendto(json.dumps(outData).encode(), toCommAddress)
        print("sending data back")
        time.sleep(5)
