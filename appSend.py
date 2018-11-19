import socket, json

thisIP = "169.254.187.140"

toCommIP = "169.254.0.2"
toCommPort = 5003
toCommAddress = (toCommIP, toCommPort)
toCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromCommIP = thisIP
fromCommPort = 5002
fromCommAddress = (thisIP, fromCommPort)
fromCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromCommSocket.bind(fromCommAddress)


if __name__ == "__main__":
    #print("Sending Test packet")
    #toSend = {"data":8, "TEST":4}
    #toCommSocket.sendto(json.dumps(toSend).encode(), toCommAddress)
    while True:
        received, add = fromCommSocket.recvfrom(2048)
        fromData = json.loads((received).decode())

        if(fromData["data"] == 2):
            print("ALERT LOW WATER LEVEL")
        elif(fromData["data"] == 3):
            print("ALERT LOW WATER LEVEL AND OVERFLOW")
        elif(fromData["data"] == 4):
            print("ALERT OVERFLOW")
        else:
            print("Everything Normal")
        print(str(fromData))