import machine
from dht import DHT22
import asyncio
import hilink
import asyncio

led_update_sub = """
subscription ($id: Int = 0) {
  ledStateChanged(id: $id)
}
"""

led_update_query = """
query ($id: Int = 0) {
  model {
    getDevice(id: $id) {
      ledState
    }
  }
}
"""

update_sensors_query = """
mutation ($id: Int!, $airQuality: Float, $humidity: Float = 1.5, $occupied: Boolean, $temperature: Float) {
    updateSensors(
        id: $id
        sensors: {airQuality: $airQuality, humidity: $humidity, temperature: $temperature, occupied: $occupied}
    ) {
        success
    }
}
"""

class Device:
    def __init__(self, config, gql, segments):
        self.config = config
        self.gql = gql
        self.segments = []
        for name in config["LED_SEGMENTS"]:
            self.segments.append(segments[name])

        if "DHT_PIN" in config:
            self.dht = DHT22(machine.Pin(config["DHT_PIN"]))
        else:
            self.dht = None

        if "AIR_DIN_PIN" in config:
            self.din = machine.Pin(config["AIR_DIN_PIN"], machine.Pin.IN)
        else:
            self.din = None

        if "AIR_ADC_PIN" in config:
            self.adc = machine.ADC(config["AIR_ADC_PIN"])
        else:
            self.adc = None

        if "PRESENCE_PIN" in config:
            self.presence_pin = machine.Pin(config["PRESENCE_PIN"], machine.Pin.IN)
        else:
            self.presence_pin = None
        
        if "PRESENCE_UART_CONTROLLER" in config:
            print(f'{config["PRESENCE_UART_CONTROLLER"]} {config["PRESENCE_TX_PIN"]} {config["PRESENCE_RX_PIN"]}')
            # self.presence_uart = machine.UART(config["PRESENCE_UART_CONTROLLER"], tx=config["PRESENCE_TX_PIN"], rx=config["PRESENCE_RX_PIN"])
            self.presence = hilink.HiLink(config["PRESENCE_UART_CONTROLLER"], tx=config["PRESENCE_TX_PIN"], rx=config["PRESENCE_RX_PIN"])
        else:
            self.presence_uart = None
            self.presence = None

    async def config_presence(self):
        if self.presence is None:
            return
        print("configuring")
        await self.presence.enable_config()
        print("setting resolution")
        await self.presence.set_resolution(hilink.HiLink.SHORT_RESOLUTION)
        print("setting running config")
        await self.presence.run_automatic_config()
        # each gate is about 7.87 inches
        print("setting max")
        await self.presence.set_max_gate_and_duration(2, 2, 5)
        # print("disabling config")
        await self.presence.disable_config()
        print("configured")

    def led_update_state(self, state):
        if state == "OFF":
            for s in self.segments:
                s.off()
        elif state == "SAFE":
            for s in self.segments:
                s.safe()
        elif state == "EVAC_OCCUPIED":
            for s in self.segments:
                s.evac_occupied()
        elif state == "EVAC_UNOCCUPIED":
            for s in self.segments:
                s.evac_unoccupied()

    async def led_update_handler(self):
        # state subscription first so that we don't miss an update between the start of subscriptions and the query
        sub = await self.gql.subscribe({
            "query": led_update_sub,
            "variables": {"id": self.config["id"]}
        })
        result = await self.gql.query({
            "query": led_update_query,
            "variables": {"id": self.config["id"]}
        })
        self.led_update_state(result["data"]["model"]["getDevice"]["ledState"])
        async for s in sub:
            state = s["data"]["ledStateChanged"]
            self.led_update_state(state)

                

    async def read_sensors_loop(self):
        # DO NOT CALL MORE OFTEN THAN EVERY 2 SECONDS
        while True:
            await asyncio.sleep(2)
            readings = {"id": self.config["id"]}
            if self.dht:
                self.dht.measure() # DO NOT MEASURE MORE OFTEN THAN EVERY 2 SECONDS
                readings["temperature"] = self.dht.temperature()
                readings["humidity"] = self.dht.humidity()
            if self.din:
                readings["smoke_detected"] = self.din.value() == 1
            if self.adc:
                readings["airQuality"] = self.adc.read_u16() * 3.3 / (65535)
            if self.presence_pin:
                readings["occupied"] = self.presence_pin.value() == 1
                print(self.presence_pin.value())
            await self.gql.query({
                "query": update_sensors_query,
                "variables": readings
            })

    async def presence_handler(self):
        if self.presence:
            asyncio.create_task(self.presence.handler())
            await self.config_presence()
        