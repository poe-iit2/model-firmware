import config
import asyncio
import network
import websocket
import sensors

wifi = network.WLAN(network.STA_IF)

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

async def connnect_to_wifi():
    if not wifi.active():
        wifi.active(True)
        wifi.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    while not wifi.isconnected():
        await asyncio.sleep(0.1)

async def main():
    await connnect_to_wifi()
    ws = websocket.WebSocket()
    await ws.connect(config.GRAPHQL_HOST, config.GRAPHQL_PORT, config.GRAPHQL_PATH)
    gql = websocket.GraphQLWs(ws)
    await gql.connect()
    asyncio.create_task(gql.handler())
    print("connected")
    print(await gql.query({"query": """query MyQuery {
  model {
    device0: getDevice(id: 0) {
      airQuality
      danger
      evacState
      humidity
      ledState
      occupied
      temperature
    }
    device1: getDevice(id: 1) {
      airQuality
      danger
      evacState
      humidity
      ledState
      occupied
      temperature
    }
  }
}"""}))
    async for s in gql.subscribe({"query": "subscription MySubscription { greetings }"}):
        print(s)
    for i in range(5):
        await asyncio.sleep(2)
        readings = sensors.read_sensors()
        print(await gql.query({
            "query":update_sensors_query,
            "variables": {
                "id": 1,
                "airQuality": readings["smoke_volts"],
                "humidity": readings["humidity"],
                "temperature": readings["temperature"],
                "occupied": readings["occupancy"]
            }
        }))

    
asyncio.run(main())