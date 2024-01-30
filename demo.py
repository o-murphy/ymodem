import argparse
import logging
import math
import os
import sys
import time

import serial

from ymodem.Protocol import ProtocolType
from ymodem.Socket import ModemSocket


class TaskProgressBar:
    def __init__(self):
        self.bar_width = 50
        self.last_task_name = ""
        self.current_task_start_time = -1

    def show(self, task_index, task_name, total, success):
        if task_name != self.last_task_name:
            self.current_task_start_time = time.perf_counter()
            if self.last_task_name != "":
                print('\n', end="")
            self.last_task_name = task_name

        success_width = math.ceil(success * self.bar_width / total)

        a = "#" * success_width
        b = "." * (self.bar_width - success_width)
        progress = (success_width / self.bar_width) * 100
        cost = time.perf_counter() - self.current_task_start_time

        print(f"\r{task_index} - {task_name} {progress:.2f}% [{a}->{b}]{cost:.2f}s", end="")


def main(filepaths, port, baud=115200, parity='N', bytesize=8, stopbits=1, com_timeout=2,
         timeout=2, chunk_size=1024):

    print(filepaths)

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    serial_io = serial.Serial()
    serial_io.port = port
    serial_io.baudrate = baud
    serial_io.parity = parity
    serial_io.bytesize = bytesize
    serial_io.stopbits = stopbits
    serial_io.timeout = com_timeout

    try:
        serial_io.open()
    except Exception as e:
        print(e)
        raise Exception("Failed to open serial port!")

    def read(size, timeout=timeout):
        serial_io.timeout = timeout
        return serial_io.read(size)

    def write(data, timeout=timeout):
        serial_io.write_timeout = timeout
        serial_io.write(data)
        serial_io.flush()
        return

    sender = ModemSocket(read, write, ProtocolType.YMODEM, packet_size=chunk_size)
    # # sender = ModemSocket(read, write, ProtocolType.YMODEM, ['g'])

    progress_bar = TaskProgressBar()
    sender.send(*filepaths, progress_bar.show)

    serial_io.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ymodem sender',
        description='sends files via ymodem'
    )

    parser.add_argument("filepaths", nargs="+")
    parser.add_argument("-p", "--port", required=True, type=str, help="COM port")
    parser.add_argument("-b", "--baud", type=int, default=115200, help="Baudrate, default 115200")
    parser.add_argument("-pr", "--parity", type=str, default="N", help="Parity, default N")
    parser.add_argument("-sz", "--bytesize", type=int, default=8, help="Bytesize, default 8")
    parser.add_argument("-sb", "--stopbits", type=int, default=1, help="Stopbits, default 1")
    parser.add_argument("-ct", "--com-timeout", type=float, default=2, help="Serial timeout, default 2")
    parser.add_argument("-t", "--timeout", type=float, default=2, help="Timeout, default 2")
    parser.add_argument("-cz", "--chunk-size", type=int, default=1024, help="Chunk size, default 1024")

    args = parser.parse_args()
    print(vars(args))

    main(**vars(args))
