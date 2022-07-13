import serial
import time

#  COMポートを開く
print("Open Port")
ser =serial.Serial("COM7 ", 9600)
while True:
    try:
        command = input("type 0 or 1: ")
        if command == "0" or command == "1":
            ser.write(command.encode())
        else:
            print("ignore command")
    except KeyboardInterrupt:
        break

print("Close Port")
ser.close()




