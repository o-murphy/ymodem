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


def add_modem_args(parser):
    parser.add_argument("-p", "--port", required=True, type=str, help="COM port")
    parser.add_argument("-b", "--baudrate", type=int, default=115200, help="Baudrate, default 115200")
    parser.add_argument("-pr", "--parity", type=str, default="N", help="Parity, default N")
    parser.add_argument("-sz", "--bytesize", type=int, default=8, help="Bytesize, default 8")
    parser.add_argument("-sb", "--stopbits", type=int, default=1, help="Stopbits, default 1")
    parser.add_argument("-t", "--timeout", type=float, default=2, help="Serial timeout, default 2")
    parser.add_argument("-cz", "--chunk-size", type=int, default=1024, help="Chunk size, default 1024")
    parser.add_argument("-d", "--debug", action='store_true')


def get_cli_args():
    parser = argparse.ArgumentParser(
        prog='ymodem',
        description='sends files via ymodem'
    )

    subparsers = parser.add_subparsers(title='Commands', dest='cmd', required=True,
                                       help="'{send,receive} -h' for more info")

    sender_argparser = subparsers.add_parser('send', help="command to send files")
    sender_argparser.add_argument("sources", nargs="+")
    add_modem_args(sender_argparser)

    receiver_argparser = subparsers.add_parser('recv', help="command to receive file")
    receiver_argparser.add_argument("dest")
    add_modem_args(receiver_argparser)

    return vars(parser.parse_args())


def main():
    def read(size, timeout=3):
        serial_io.timeout = timeout
        return serial_io.read(size)

    def write(data, timeout=3):
        serial_io.write_timeout = timeout
        serial_io.write(data)
        serial_io.flush()
        return

    args = get_cli_args()

    debug = args.pop('debug')
    cmd = args.pop('cmd')
    packet_size = args.pop('chunk_size', 1024)
    sources = args.pop('sources', [])
    dest = args.pop('dest', './')

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO, format='%(message)s')

    serial_io = serial.Serial(**args)

    if serial_io.is_open:
        logging.info(f"Port {args['port']} opened")
        try:
            progress_bar = TaskProgressBar()
            socket = ModemSocket(read, write, ProtocolType.YMODEM, packet_size=packet_size)

            if cmd == 'send':
                paths = [os.path.abspath(source) for source in sources]
                logging.info(f"Waiting for command from Receiver...")
                socket.send(paths, progress_bar.show)
            elif cmd == 'recv':
                path = os.path.abspath(dest)
                logging.info(f"Waiting for response from Sender...")
                socket.recv(path, progress_bar.show)
            else:
                raise Exception("Unknown command")
        except (Exception, KeyboardInterrupt) as exc:
            logging.exception(exc)

        finally:
            serial_io.close()
            logging.info(f"Port {args['port']} closed")


if __name__ == '__main__':
    main()
