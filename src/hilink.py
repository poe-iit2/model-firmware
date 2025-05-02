import asyncio
import machine

def vars(o):
    return o.__dict__

class HiLink:
    SHORT_RESOLUTION = b"\x00\x00"
    LONG_RESOLUTION = b"\x01\x00"

    def __init__(self, controller, tx, rx):
        if "mock_ajskdnjk" in vars(machine):
            return
        self.uart = machine.UART(controller, baudrate=256000, bits=8, parity=None, stop=1, tx=tx, rx=rx)
        self.reader = asyncio.StreamReader(self.uart)
        self.writer = asyncio.StreamWriter(self.uart)
        self.response = None
        self.event = asyncio.Event()
        self.auto_config_end = asyncio.Event()
        self.auto_config_success = False
        self.lock = asyncio.Lock()
        self.value = False
        self.ticker = 0

    async def send_frame(self, data):
        self.writer.write(b"\xfd\xfc\xfb\xfa"
                          + len(data).to_bytes(2, "little")
                          + data
                          + b"\x04\x03\x02\x01")
        return await self.writer.drain()
    
    async def exec(self, command, data):
        if "mock_ajskdnjk" in vars(machine):
            return b"\x00\x00"
        async with self.lock:
            self.event.clear()
            await self.send_frame(command.to_bytes(2, "little") + data)
            await self.event.wait()
            assert int.from_bytes(self.response[:2], "little") == command | 0x0100
            return self.response[2:]

    async def handler(self):
        if "mock_ajskdnjk" in vars(machine):
            while True:
                await asyncio.sleep(1)
        k = 0
        while True:
            # print("reading")
            header = await self.reader.readexactly(4)
            # print("read: " + repr(header))
            if header == b"\xfd\xfc\xfb\xfa":
                n = await self.reader.readexactly(2)
                n = int.from_bytes(n, "little")
                self.response = await self.reader.readexactly(n)
                header = await self.reader.readexactly(4)
                assert header == b"\x04\x03\x02\x01"
                self.event.set()
            elif header == b"\xf4\xf3\xf2\xf1":
                n = await self.reader.readexactly(2)
                n = int.from_bytes(n, "little")
                data = await self.reader.readexactly(n)
                assert data[0] == 0x02
                assert data[1] == 0xaa
                assert data[-2] == 0x55
                assert data[-1] == 0x00
                data = data[2:-2]
                k+=1
                print(str(k) + " Radar: " + data.hex(" "))
                if data[0] == 0x05 or data[0] == 0x06:
                    self.auto_config_success = data[0] == 0x05
                    self.auto_config_end.set()
                if data[0]:
                    self.ticker += 1
                else:
                    self.ticker = 0
                # self.value = data[0] != 0

                    

    async def enable_config(self):
        result = await self.exec(0x00ff, b"\x01\x00")
        if result[0]:
            raise RuntimeError("ACK indicated failure")
    
    async def disable_config(self):
        result = await self.exec(0x00fe, b"")
        if result[0]:
            raise RuntimeError("ACK indicated failure")

    async def set_max_gate_and_duration(self, max_move_gate, max_rest_gate, noone_duration):
        result = await self.exec(0x0060,
                                 b"\x00\x00"
                                 + max_move_gate.to_bytes(4, "little")
                                 + b"\x01\x00"
                                 + max_rest_gate.to_bytes(4, "little")
                                 + b"\x02\x00"
                                 + noone_duration.to_bytes(4, "little"))
        if result[0]:
            raise RuntimeError("ACK indicated failure")
        
    async def set_gate_sensitivity(self, gate, move_sensitivity, rest_sensitivity):
        result = await self.exec(0x0064,
                                 b"\x00\x00"
                                 + gate.to_bytes(4, "little")
                                 + b"\x01\x00"
                                 + move_sensitivity.to_bytes(4, "little")
                                 + b"\x02\x00"
                                 + rest_sensitivity.to_bytes(4, "little"))
        if result[0]:
            raise RuntimeError("ACK indicated failure")
    
    async def set_bluetooth(self, is_on):
        result = await self.exec(0x00a4,
                                 b"\x01\x00" if is_on else b"\x00\x00")
        if result[0]:
            raise RuntimeError("ACK indicated failure")
        
    async def set_resolution(self, resolution):
        result = await self.exec(0x00aa, resolution)
        if result[0]:
            raise RuntimeError("ACK indicated failure")
    
    async def begin_automatic_config(self, duration=10):
        result = await self.exec(0x00B, duration.to_bytes(2, "little"))
        if result[0]:
            raise RuntimeError("ACK indicated failure")
        
    async def run_automatic_config(self, duration=10):
        if "mock_ajskdnjk" in vars(machine):
            return
        self.auto_config_end.clear()
        await self.begin_automatic_config(duration)
        await self.disable_config()
        await self.auto_config_end.wait()
        await self.enable_config()
        if not self.auto_config_success:
            raise RuntimeError("Auto config of radar failed")


    
        
        