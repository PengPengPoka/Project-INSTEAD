# # import serial
# # import datetime
# # import csv

# # ser = serial.Serial('COM7', baudrate=115200)  # usb port settings
# # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
# # csv_filename = f"sensor_data_{timestamp}.csv"


# # def request_data(delay, amount):
# #     data_to_send = f"{delay}#{amount}\n"
# #     ser.write(data_to_send.encode())
# #     with open(csv_filename, mode='w', newline='') as csv_file:
# #         for i in range(int(amount)):
# #             serial_data = ser.readline().decode('ascii')    # read serial data from usb
# #             split_values = serial_data.split("#")   # split values by #
# #             int_values = [int(value) for value in split_values]
# #             print(int_values)  # Output: [123, 456, 789]
# #             csv_writer = csv.writer(csv_file)
# #             csv_writer.writerow(int_values)  # append data to csv file


# # while 1:
# #     delay = input("Delay (ms): ")  # input delay from user
# #     amount = input("How many data? ")  # input amount from user
# #     # print(delay+amount)
# #     request_data(delay, amount)

# import serial
# import datetime
# import csv
# import multiprocessing

# ser = serial.Serial('COM7', baudrate=115200)  # usb port settings


# def request_data(delay, amount):
#     data_to_send = f"{delay}#{amount}\n"  # data format
#     ser.write(data_to_send.encode())  # send data to usb

#     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
#     csv_filename = f"sensor_data_{timestamp}.csv"

#     with open(csv_filename, mode='w', newline='') as csv_file:
#         for i in range(int(amount)):
#             serial_data = ser.readline().decode('ascii')    # read serial data from usb
#             split_values = serial_data.split("#")   # split values by #
#             int_values = [int(value) for value in split_values]
#             print(int_values)  # Output: [123, 456, 789]
#             csv_writer = csv.writer(csv_file)
#             csv_writer.writerow(int_values)  # append data to csv file


# if __name__ == "__main__":
#     delay = input("Delay (ms): ")  # input delay from user
#     amount = input("How many data? ")  # input amount from user
#     p1 = multiprocessing.Process(target=request_data, args=(delay, amount))
#     p1.start()


################################
# import serial
# import datetime
# import csv
# import multiprocessing

# ser = serial.Serial('COM10', baudrate=115200)  # usb port settings
# # ser = serial.Serial('COM10', baudrate=9600)  # usb port settings


# def request_data(delay, amount):
#     data_to_send = f"{delay}#{amount}\n"  # data format
#     ser.write(data_to_send.encode())  # send data to usb

#     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
#     csv_filename = f"sensor_data_{timestamp}.csv"

#     with open(csv_filename, mode='w', newline='') as csv_file:
#         for i in range(int(amount)):
#             serial_data = ser.readline().decode('ascii')    # read serial data from usb
#             split_values = serial_data.split("#")   # split values by #
#             int_values = [int(value) for value in split_values]
#             print(int_values)  # Output: [123, 456, 789]
#             csv_writer = csv.writer(csv_file)
#             csv_writer.writerow(int_values)  # append data to csv file


# if __name__ == "__main__":
#     delay = input("Delay (ms): ")  # input delay from user
#     amount = input("How many data? ")  # input amount from user
#     request_data(delay=delay,amount=amount)
    # p1 = multiprocessing.Process(target=request_data, args=(delay, amount))
    # p1.start()
    # while(1):

import time
import threading
import csv 
import datetime
import serial

class DataSamplingThread(threading.Thread):
    def __init__(self, delay, amount, progress_callback, serial_callback):
        super().__init__()
        self.delay = delay
        self.amount = amount
        self.progress_callback = progress_callback
        self.serial_callback = serial_callback

    def run(self,amount,delay):
        for i in range(5):
            print("Searching for COM ports...")
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                try:
                    print('Found port ' + port.device, port.serial_number)
                    ser = serial.Serial(port.device, 115200, timeout=1)
                    ser.flush()
                    print('Connect ' + ser.name)

                    data_to_test = f"{60}#{1}\n"  # data format
                    ser.write(data_to_test.encode())  # send data to usb
                    serial_data_test = ser.readline().decode('ascii')
                    if serial_data_test == '':
                        print("Wrong COM port")
                        raise Exception("Wrong COM port")
                    split_values_test = serial_data_test.split(
                        "#")   # split values by #
                    int_values_test = [int(value) for value in split_values_test]
                    if int_values_test.__len__() < 6:
                        print("Wrong COM port")
                        raise Exception("Wrong COM port")

                except:
                    print("error")
                    ser.close()
                    continue



                data_to_send = f"{delay}#{amount}\n"  # data format
                ser.write(data_to_send.encode())  # send data to usb


                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                csv_filename = f"sensor_data_{timestamp}_BOHEA_AMPAS_7-{i+1}.csv"
                
                self.progress_callback(i + 1)
                self.serial_callback( )    

                with open(csv_filename, mode='w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    header = ["Sensor 1", "Sensor 2", "Sensor 3",
                            "Sensor 4", "Sensor 5", "Sensor 6"]
                    csv_writer.writerow(header)
                    for i in range(int(amount)):
                        serial_data = ser.readline().decode('ascii')    # read serial data from usb
                        split_values = serial_data.split("#")   # split values by #
                        int_values = [int(value) for value in split_values]
                        # for i in range(6):
                        # int_values[i] = round((int_values[i]*3.3/65536), 3)
                        print(i+1, int_values)  # Output: [123, 456, 789]
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(int_values)  # append data to csv file
                    ser.close()
                    break
