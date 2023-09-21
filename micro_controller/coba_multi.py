import serial
import datetime
import csv
import time
import multiprocessing


def request_data(delay, amount):
    for i in range(int(amount)):
        print("f", i)
        time.sleep(0.05)


if __name__ == "__main__":
    delay = 100
    amount = 100
    # print(delay+amount)
    p1 = multiprocessing.Process(target=request_data, args=(delay, amount))
    p1.start()
    for i in range(int(amount)):
        print("main", i)
        time.sleep(0.05)
    # request_data(delay, amount)
