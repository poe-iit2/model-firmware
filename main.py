import asyncio
import network
import websocket

wifi = network.WLAN(network.STA_IF)

async def connnect_to_wifi():
    if not wifi.active():
        wifi.active(True)
        wifi.connect("jimmy-XPS", "jzbxcakcbakjfuia")
    while not wifi.isconnected():
        await asyncio.sleep(0.1)

async def main():
    await connnect_to_wifi()
    ws = websocket.WebSocket()
    await ws.connect("localhost", 5000, "/")
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
    async for s in gql.subscribe({"query": """subscription MySubscription {
  greetings
}"""}):
        print(s)

    
asyncio.run(main())