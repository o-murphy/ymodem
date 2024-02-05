import asyncio
import serial_asyncio


class SerialTerminal:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(url=self.port, baudrate=self.baudrate)

    async def read_from_uart(self):
        while True:
            line = await self.reader.readline()
            try:
                print(f'Received: {line.decode().rstrip()}')
            except UnicodeDecodeError:
                print(f'Received {line}')

    async def write_to_uart(self):
        while True:
            data = await self.get_user_input()
            self.writer.write(data.encode() + b'\r')
            await self.writer.drain()

    async def get_user_input(self):
        return await asyncio.get_event_loop().run_in_executor(None, input, 'Send: ')

    async def run(self):
        await self.connect()
        reader_task = asyncio.create_task(self.read_from_uart())
        writer_task = asyncio.create_task(self.write_to_uart())
        await asyncio.gather(reader_task, writer_task)


def main():
    port = 'COM4'  # Change this to your serial port
    baudrate = 115200  # Change this to your baud rate
    terminal = SerialTerminal(port, baudrate)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(terminal.run())
    loop.close()


main()
