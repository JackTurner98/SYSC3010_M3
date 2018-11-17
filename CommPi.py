import string, socket, sys, time, serial;

ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)

serverIP = "0.0.0.0"
appIP = "0.0.0.0"

toServerPort = "0"
fromServerPort = "0"
toAppPort = "0"
fromAppPort = "0"

toServerAddress = (serverIP, toServerPort)
fromServerAddress = (serverIP, fromServerPort)
toAppAddress = (appIP, toAppPort)
fromAppAddress = (appIP, fromAppPort)

toServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
toAppSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromAppSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

toServerSocket.bind(toServerAddress)
fromServerSocket.bind(fromServerAddress)
toAppSocket.bind(toAppAddress)
fromAppSocket.bind(fromAppAddress)

if __name__ == "__main__":
    while True:
        fromServer = fromServerSocket.recvfrom(2048)
        fromApp = fromAppSocket.recvfrom(2048)
        print(ser.readLine())


