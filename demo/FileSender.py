import logging
import os
import sys
import time

import serial

from ymodem.Protocol import ProtocolType
from ymodem.Socket import ModemSocket
from ymodem.__main__ import TaskProgressBar

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    serial_io = serial.Serial()
    serial_io.port = "COM5"
    serial_io.baudrate = "115200"
    serial_io.parity = "N"
    serial_io.bytesize = 8
    serial_io.stopbits = 1
    serial_io.timeout = 2

    try:
        serial_io.open()
    except Exception as e:
        raise Exception("Failed to open serial port!")


    def read(size, timeout=3):
        serial_io.timeout = timeout
        return serial_io.read(size)


    def write(data, timeout=3):
        serial_io.write_timeout = timeout
        serial_io.write(data)
        serial_io.flush()
        return


    sender = ModemSocket(read, write, ProtocolType.YMODEM)
    # sender = ModemSocket(read, write, ProtocolType.YMODEM, ['g'])

    os.chdir(sys.path[0])
    file_path1 = os.path.abspath(r"demo/local/sample6.bin")
    # file_path2 = os.path.abspath('local/sample2.stl')
    # file_path3 = os.path.abspath('local/sample3.stl')
    progress_bar = TaskProgressBar()
    # sender.send([file_path1, file_path2, file_path3], progress_bar.show)
    sender.send([file_path1], progress_bar.show)

    # timeout = 4
    while True:
        time.sleep(1)
        print(serial_io.read(128))

    # serial_io.close()
