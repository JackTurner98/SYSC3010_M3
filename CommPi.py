import string, socket, sys, time, serial;
output = " "
ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)
while True:
    print(ser.readLine())
