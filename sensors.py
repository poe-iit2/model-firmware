import config
import machine
from dht import DHT22

dht = DHT22(machine.Pin(config.DHT_PIN))
presense = machine.Pin(config.PRESENCE_PIN)

#Select ADC input 0 (GPIO26)
adc = machine.ADC(config.AIR_ADC_PIN)
din = machine.Pin(config.AIR_DIN_PIN, machine.Pin.IN)
conversion_factor = 3.3 / (65535)

def read_sensors():
    dht.measure() # DO NOT MEASURE MORE OFTEN THAN EVERY 2 SECONDS
    return {
        "temperature": dht.temperature(),
        "humidity": dht.humidity(),
        "smoke_detected": din.value() == 1,
        "smoke_volts": adc.read_u16() * conversion_factor,
        "occupancy": presense.value() == 1
    }