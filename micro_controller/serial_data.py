import serial
 
ser = serial.Serial('COM7', baudrate = 115200, timeout=1)
 
while 1:
    arduinoData = ser.readline().decode('ascii')
    split_values = arduinoData.split("#")
    # int_values = list(map(int, split_values))
    int_values = [int(value) for value in split_values]
    print(int_values)  # Output: [123, 456, 789]
    # print(arduinoData)