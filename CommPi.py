import string, socket, sys, time, json, select, serial

ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)

thisIP = "169.254.0.2"
serverIP = "169.254.187.140"
appIP = "169.254.187.140"


toServerPort = 5000
fromServerPort = 5001
toAppPort = 5002
fromAppPort = 5003

toServerAddress = (serverIP, toServerPort)
fromServerAddress = (thisIP, fromServerPort)
toAppAddress = (appIP, toAppPort)
fromAppAddress = (thisIP, fromAppPort)

toServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
toAppSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromAppSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromServerSocket.bind(fromServerAddress)
fromAppSocket.bind(fromAppAddress)

fromSockets = [fromServerSocket, fromAppSocket]
appNeeds = False

def getCurrentState():

    ser.write('1')
    read = ser.read_until('}')
    sensorData = json.loads(read)
    return sensorData

def sendCurrentState(toSend):
    packet = {"data":0, "temp":toSend['temp'], "level":toSend['level'], "overflow":toSend['overflow']}
    toServerSocket.sendto(json.dumps(packet).encode(), toServerAddress)

def sendProcessedData(toSend):
    toAppSocket.sendto(toSend, toAppAddress)

if __name__ == "__main__":
    while True:
        print("\nwaiting for instruction")
        socketCheck,_,_ = select.select(fromSockets, [], [])
        for socket in socketCheck:
            receivedData, add = socket.recvfrom(2048)
            fromData = json.loads((receivedData).decode())
            print("Received Instruction: " + str(fromData))
            if(int(fromData["data"]) == 5): #Instruction: Get current sensor data, send to server
                sendCurrentState(getCurrentState())
                print("got current state, sending back")
                receivedProcessedData, addSecond = fromServerSocket.recvfrom(2048)
                fromServerSecond = json.loads(receivedProcessedData.decode())
                print("Received processed Data: " + str(fromServerSecond))
                instr = int(fromServerSecond["data"])
                if( instr == 6 or instr == 2 or instr == 3 or instr == 4): #Instruction: Received processed data, send to app
                    sendProcessedData(receivedProcessedData)
                    print("sending processed data to app now")


            elif(int(fromData["data"]) == 8): #Instruction: Received target date, send to server for query
                toServerSocket.sendto(receivedData, toServerAddress)
                print("Sending Date query")
                receivedPastData, addSecond = fromServerSocket.recvfrom(2048)
                pastData = json.loads(receivedPastData.decode())
                print("Received past data: " + str(pastData))
                #if(int(pastData["data"]) == 9): #Instruction: Received queried data, send to App
                sendProcessedData(receivedPastData)
                print("Sending past data to app now")







