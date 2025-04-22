import machine
from dht import DHT22
import asyncio

led_update_query = """
subscription ($id: Int = 0) {
  ledStateChanged(id: $id)
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
    def __init__(self, config, gql):
        self.config = config
        self.gql = gql

        if "DHT_PIN" in config:
            self.dht = DHT22(machine.Pin(config["DHT_PIN"]))
        else:
            self.dht = None

        if "AIR_DIN_PIN" in config:
            self.din = machine.Pin(config["AIR_DIN_PIN"])
        else:
            self.din = None

        if "AIR_ADC_PIN" in config:
            self.adc = machine.ADC(config["AIR_ADC_PIN"])
        else:
            self.adc = None

        if "PRESENCE_PIN" in config:
            self.presense = machine.Pin(config["PRESENCE_PIN"])
        else:
            self.presense = None

    async def led_update_handler(self):
        async for s in await self.gql.subscribe({
            "query": led_update_query,
            "variables": {"id": self.config["id"]}
        }):
            print(s)

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
            if self.presense:
                readings["occupied"] = self.presense.value() == 1
            await self.gql.query({
                "query": update_sensors_query,
                "variables": readings
            })
        