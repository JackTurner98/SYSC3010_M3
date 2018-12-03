import socket, time, json, pymongo

# SYSC 3010 - Automated Aquarium Monitoring Processing Pi
# Version: December 2nd 2018
# Author: John Turner

client = pymongo.MongoClient('mongodb://Sahil:Sahil_742995@ds139844.mlab.com:39844/aqua')
db = client.aqua    # Initializing the database
posts = db.posts

# The IPs for communication, * Make sure both devices are using the same IP types (IPv4 and Eth/WLAN)
toCommIP = "169.254.0.2"  # The IP of the Communication Pi
thisIP = "169.254.187.140"  # The IP of this device

toCommPort = 5001  # Set ports for communication
fromCommPort = 5000

toCommAddress = (toCommIP, toCommPort)  # Combine IPs and Ports into addresses
fromCommAddress = (thisIP, fromCommPort)

toCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Initialize UDP Sockets that accept IPs
fromCommSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromCommSocket.bind(fromCommAddress)  # Bind receiving sockets to a specific address

updateDelay = 15  # Initialize variable that determines when to update sensor data
feedCounter = 0  # Variable that determines if the feed signal should be sent
feedDelay = 2
Running = True  # Variable to set if the system runs or not


# Processes data from a  JSON packet, converts data to be usable and returns a dictionary
def processData(packet):
    data = json.loads(packet)  # Loads JSON packet into dictionary

    tempRead = data['temp']  # Get the data out of the dictionary
    level = data['level']
    over = data['overflow']

    tempRead = tempRead / 1024 * 5000  # Conversion from raw data to usable values
    temp = (tempRead / 10)  # Unit is Celsius
    over = (over * 4 / 600)  # Unit is cm
    level = (level * 4 / 600)  # Unit is cm

    temp = round(temp, 2)  # To keep the database clean the values are shortened to only have 2 decimal places
    level = round(level, 2)
    over = round(over, 2)

    update(temp, level, over)  # The processed values are tested and then inserted into the DataBase


# Sends a request to the Communication Pi to update the sensor data
def getCurrentState():
    toSend = {"data": 5}
    toCommSocket.sendto(json.dumps(toSend).encode(), toCommAddress)  # Sends update instruction to the Comm Pi


def sendFeed():
    toSend = {"data": 7}
    toCommSocket.sendto(json.dumps(toSend).encode(), toCommAddress)  # Sends feed instruction to the Comm Pi


def update(temp, level, over):
    currDate = time.gmtime()  # Get the current date
    refinedDate = str(currDate[0]) + "," + str(currDate[1]) + "," + str(currDate[2])  # Split date into year, month, day

    postTest_data = {   # A Packet is created that will be inserted into the DataBase
        'Date': refinedDate,
        'Temperature': temp,
        'waterLevel': level,
        'overflowLevel': over
    }

    if test(temp, level, over):  # The data is tested to make sure no bad values go into the DataBase
        store(postTest_data)


def test(temperature, waterLvl, overflowLvl):
    assert(waterLvl >= 0),"waterLevel cant be negative"
    assert(temperature >= 0),"temperature cant be negative"
    assert(overflowLvl >= 0),"temperature cant be negative"

    assert(waterLvl <= 7), "hardware error, sensor range 0-4 cm"
    assert(temperature <= 40),"hardware error,sensor range 0-40celcius"
    assert(overflowLvl <= 7), "hardware error, sensor range 0-4 cm"

    assert(waterLvl != " "),"cannot insert null value"
    assert(temperature != " "), "cannot insert null value"
    assert(overflowLvl != " "), "cannot insert null value"

    return True


def store(data):
    posts.insert_one(data)  # The tested values are inserted into the database


if __name__ == "__main__":
    while Running:
        if feedCounter > feedDelay:  # If its time to feed, send the feed instruction
            sendFeed()
            feedCounter = 0  # Reset the feed delay
        else:
            getCurrentState()  # Sends update instruction to Comm Pi
        received, add = fromCommSocket.recvfrom(2048)  # Receives data from the Comm Pi
        processData(received)  # Process the received data
        feedCounter += 1
        time.sleep(updateDelay)  # Wait until the next update cycle
