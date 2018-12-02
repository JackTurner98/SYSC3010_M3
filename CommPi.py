import string, socket, sys, time, json, select, serial

#   SYSC 3010 - Automated Aquarium Monitoring Communication Pi
#   Version: December 2nd 2018
#   Author: John Turner

ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)  # Initialize the serial port

# The IPs for communication, * Make sure both devices are using the same IP types (IPv4 and Eth/WLAN)
thisIP = "169.254.0.2"  # IP of this Device
serverIP = "169.254.187.140"  # IP of the Server Pi

toServerPort = 5000  # Assign ports for communication
fromServerPort = 5001

toServerAddress = (serverIP, toServerPort)  # Generate address using IPs and Ports
fromServerAddress = (thisIP, fromServerPort)

toServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create UDP sockets that accept IPs
fromServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromServerSocket.bind(fromServerAddress)  # Bind the receiving sockets to an Address

fromSockets = [fromServerSocket]  # Array of receiving sockets that will be checked until one receives

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


if __name__ == "__main__":
    while Running:
        socketCheck, _, _ = select.select(fromSockets, [], [])  # Checks if any socket has requested something
        for socket in socketCheck:  # For each of the sockets that received data specific operations will be done
            receivedData, add = socket.recvfrom(2048)  # Check what data was sent to this Pi
            fromData = json.loads(receivedData.decode())  # Load the JSON packet into a dictionary
            instr = int(fromData["data"])
            if instr == 5 or instr == 7:  # Instruction: Get current sensor data, send to server
                sendCurrentState(getCurrentState())  # Get and then send the current sensor data to the Server
                if instr == 7:  # If feed instruction is received, start feed cycle
                    startFeed()
