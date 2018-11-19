import socket, json

thisIP = "localhost"

toCommIP = "localhost"
toCommPort = 5003
toCommAddress = (toCommIP, toCommPort)
toCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromCommIP = "localhost"
fromCommPort = 5002
fromCommAddress = (thisIP, fromCommPort)
fromCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromCommSocket.bind(fromCommAddress)


if __name__ == "__main__":
    print("Sending Test packet")
    toSend = {"data":8, "TEST":4}
    toCommSocket.sendto(json.dumps(toSend).encode(), toCommAddress)

    received, add = fromCommSocket.recvfrom(2048)
    fromData = json.loads((received).decode())

    print("received: " + str(fromData))