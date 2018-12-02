import string, socket, sys, time, json, select, serial

#   SYSC 3010 - Automated Aquarium Monitoring Communication Pi
#   Version: December 1st 2018
#   Author: John Turner

ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)  # Initialize the serial port

# The IPs for communication, * Make sure both devices are using the same IP types (IPv4 and Eth/WLAN)
thisIP = "169.254.0.2"  # IP of this Device
serverIP = "169.254.187.140"  # IP of the Server Pi
appIP = "169.254.187.140"  # IP of the App

toServerPort = 5000  # Assign ports for communication
fromServerPort = 5001
toAppPort = 5002
fromAppPort = 5003

toServerAddress = (serverIP, toServerPort)  # Generate address using IPs and Ports
fromServerAddress = (thisIP, fromServerPort)
toAppAddress = (appIP, toAppPort)
fromAppAddress = (thisIP, fromAppPort)

toServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create UDP sockets that accept IPs
fromServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
toAppSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fromAppSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromServerSocket.bind(fromServerAddress)  # Bind the receiving sockets to an Address
fromAppSocket.bind(fromAppAddress)

fromSockets = [fromServerSocket, fromAppSocket]  # Array of receiving sockets that will be checked until one receives

Running = True  # While set the system will run

# Requests and receives current sensor data from the Arduino
def getCurrentState():
    read = '{'  # Detecting a JSON packet cuts off the first { so it is added back.
    ser.write('p')  # Send the request to the Arduino for new data
    ser.read_until('{')  # Wait until a JSON packet is received
    read += ser.read_until('}')  # Read until the end of the JSON packet
    sensorData = json.loads(read)  # Load the received packet into a dictionary
    return sensorData


# Sending Feed instruction to the Arduino
def startFeed():
    ser.write('f')  # Send feed instruction to Arduino

# Sends the current sensor data to the Server/Processing Pi
def sendCurrentState(toSend):
    packet = {"data": 0, "temp": toSend['temp'], "level": toSend['level'], "overflow": toSend['overflow']}
    toServerSocket.sendto(json.dumps(packet).encode(), toServerAddress)  # Sends repacked data to the server Pi

# Sends Processed Data to the App
def sendProcessedData(toSend):
    toAppSocket.sendto(toSend, toAppAddress)  # Sends a Packet to the app address


if __name__ == "__main__":
    while Running:
        socketCheck, _, _ = select.select(fromSockets, [], [])  # Checks if App or Server has requested something

        for socket in socketCheck:  # For each of the sockets that received data specific operations will be done
            receivedData, add = socket.recvfrom(2048)  # Check was data was sent to this Pi
            fromData = json.loads(receivedData.decode())  # Load the JSON into a dictionary

            if (int(fromData["data"]) == 5):  # Instruction: Get current sensor data, send to server
                sendCurrentState(getCurrentState())  # Get and then send the current sensor data to the Server

                receivedProcessedData, addSecond = fromServerSocket.recvfrom(2048)  # Receive the processed data
                fromServerSecond = json.loads(receivedProcessedData.decode())  # Load the received data into dictionary
                instr = int(fromServerSecond["data"])  # Variable to check the current instruction

                if (instr >= 2 and instr <= 7 and not instr == 5):  # Instruction: Received processed data, send to app
                    if (instr == 7):  # If the feeder needs to be turned on
                        startFeed()  # Send Feed Instruction
                    sendProcessedData(receivedProcessedData)  # Send the processed data to the App

            elif (int(fromData["data"]) == 8):  # Instruction: Received target date, send to server for query
                toServerSocket.sendto(receivedData, toServerAddress)  # Send the data that was received
                receivedPastData, addSecond = fromServerSocket.recvfrom(2048)  # Receive the queried data
                sendProcessedData(receivedPastData)  # Send the queried data to the app









