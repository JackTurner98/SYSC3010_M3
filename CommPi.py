import string, socket, sys, time, json#,serial

#ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)

serverIP = "localhost"
appIP = "localhost"

toServerPort = 5000
fromServerPort = 5001
toAppPort = 5002
fromAppPort = 5003

toServerAddress = (serverIP, toServerPort)
fromServerAddress = ("localhost", fromServerPort)
toAppAddress = (appIP, toAppPort)
fromAppAddress = ("localhost", fromAppPort)

toServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
toAppSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromAppSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromServerSocket.bind(fromServerAddress)
fromAppSocket.bind(fromAppAddress)

appNeeds = False

def getCurrentState():
    sensorData = [None, None, None]
    sensorData[0] = 20#Read temp sensor
    sensorData[1] = 2#Read level sensor
    sensorData[2] = 0#Read OverFlow Sensor
    return sensorData

def sendCurrentState(toSend):
    packet = {"data":0, "temp":toSend[0], "level":toSend[1], "overflow":toSend[2]}
    toServerSocket.sendto(json.dumps(packet).encode(), toServerAddress)

if __name__ == "__main__":
    while True:
        print("waiting for instruction")
        receivedData, add = fromServerSocket.recvfrom(2048)
        fromServer = json.loads((receivedData).decode())

        if(int(fromServer["data"]) == 5):
            sendCurrentState(getCurrentState())
            print("got current state, sending now")
            appNeeds = True
        elif(appNeeds):
            #toAppSocket.sendall(fromServer)
            print("received: " + str(fromServer["temp"]) + " " + str(fromServer["level"]) + " " + str(fromServer["overflow"]))
            print("sending processed data to app now")
            appNeeds = False






