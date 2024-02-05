import asyncio
import serial_asyncio
from rich.console import Console
# from rich.prompt import Prompt
from threading import Thread


class SerialTerminal:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.reader = None
        self.writer = None

        self.console = Console()
        self.running = True
        self.event_loop = None

    # async def connect(self):
    #     self.reader, self.writer = await serial_asyncio.open_serial_connection(url=self.port, baudrate=self.baudrate)
    #
    # async def read_from_uart(self):
    #     while True:
    #         line = await self.reader.readline()
    #         try:
    #             print(f'< {line.decode().rstrip()}')
    #         except UnicodeDecodeError:
    #             print(f'< {line}')
    #
    # async def write_to_uart(self):
    #     while True:
    #         data = await self.get_user_input()
    #         self.writer.write(data.encode() + b'\r')
    #         await self.writer.drain()
    #
    # async def get_user_input(self):
    #     return await asyncio.get_event_loop().run_in_executor(None, input, 'Send: ')
    #
    # async def run(self):
    #     await self.connect()
    #     reader_task = asyncio.create_task(self.read_from_uart())
    #     writer_task = asyncio.create_task(self.write_to_uart())
    #     await asyncio.gather(reader_task, writer_task)

    async def connect(self):
        if self.event_loop is None:
            self.event_loop = asyncio.get_running_loop()  # Get the loop when you're sure it's running
        self.reader, self.writer = await serial_asyncio.open_serial_connection(url=self.port, baudrate=self.baudrate)

    async def read_from_uart(self):

        while self.running:
            line = await self.reader.readline()
            self.console.log(f"Received: {line.decode(errors='ignore').rstrip()}", style="green")

    def write_to_uart_sync(self, event_loop):
        while self.running:
            data = self.console.input(">>> ")
            # data = Prompt.ask("Send", console=self.console, show_default=False)
            # Use the passed event loop reference here
            asyncio.run_coroutine_threadsafe(self.send_to_uart(data), event_loop)

    async def send_to_uart(self, data):
        self.writer.write(data.encode() + b'\r')
        await self.writer.drain()

    async def run(self):
        await self.connect()
        read_task = asyncio.create_task(self.read_from_uart())

        # Pass the event loop reference to the thread
        write_thread = Thread(target=self.write_to_uart_sync, args=(self.event_loop,))
        write_thread.start()

        await read_task


def main(port, baudrate):
    terminal = SerialTerminal(port, baudrate)

    asyncio.run(terminal.run())

    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(terminal.run())
    # finally:
    #     terminal.running = False
    #     loop.close()


# async def main():
#     terminal = SerialTerminal(port, baudrate)
#     await
# # port = 'COM4'  # Change this to your serial port
# # baudrate = 115200  # Change this to your baud rate
# # terminal = SerialTerminal(port, baudrate)
# # asyncio.run(terminal.run())
