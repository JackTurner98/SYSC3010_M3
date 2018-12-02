import socket, json

# SYSC 3010 - Automated Aquarium Monitoring App Receiving/Sending
# Version: December 1st 2018
# Author: John Turner

thisIP = "169.254.187.140"  # The IP of this device

toCommIP = "169.254.0.2"    # The IP of the Communication Pi
toCommPort = 5003
toCommAddress = (toCommIP, toCommPort)
toCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromCommIP = thisIP
fromCommPort = 5002
fromCommAddress = (thisIP, fromCommPort)
fromCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromCommSocket.bind(fromCommAddress)


if __name__ == "__main__":
    toSend = {"data":8, "date":(2018, 12, 2)}
    toCommSocket.sendto(json.dumps(toSend).encode(), toCommAddress)
    received, add = fromCommSocket.recvfrom(2048)
    fromData = json.loads(received.decode())
    print(str(fromData))