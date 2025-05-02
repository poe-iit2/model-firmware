WIFI_SSID = "JimmyXPS"
WIFI_PASSWORD = "ashvbiqbrglncawuhciuwli"

GRAPHQL_HOST = "192.168.12.1"
GRAPHQL_PORT = 5000
GRAPHQL_PATH = "/"

led_pins = [
    {
        "PIN": 25,
        "COUNT": 102
    },
]

led_segments = [
    {
        "name": "HALL",
        "color": (10,10,10),
        "span": 26,
        "reversed": False
    },
    {
        "name": "ROOM2R",
        # "color": (10,10,10),
        "span": 19,
        "reversed": False
    },
        {
        "name": "ROOM2L",
        # "color": (10,10,10),
        "span": 19,
        "reversed": True
    },
        {
        "name": "ROOM1R",
        # "color": (10,10,10),
        "span": 19,
        "reversed": False
    },
    {
        "name": "ROOM1L",
        # "color": (10,10,10),
        "span": 19,
        "reversed": True
    },
]

devices = (
    {
        "id": 0,
        "DHT_PIN": 14,
        # "PRESENCE_PIN": 35,
        "PRESENCE_TX_PIN": 17,
        "PRESENCE_RX_PIN": 16,
        "PRESENCE_UART_CONTROLLER": 1,
        # "LED_SEGMENTS": [],
        "LED_SEGMENTS": ["ROOM1R", "ROOM1L"],
        "AIR_DIN_PIN": 34,
        #"AIR_ADC_PIN": 32
    }, {
        "id": 1,
        "DHT_PIN": 27,
        # "PRESENCE_PIN": 35,
        "PRESENCE_TX_PIN": 18,
        "PRESENCE_RX_PIN": 5,
        "PRESENCE_UART_CONTROLLER": 2,
        "AIR_DIN_PIN": 32,
        # "AIR_ADC_PIN": 32,
        # "LED_SEGMENTS": [],
        "LED_SEGMENTS": ["ROOM2R", "ROOM2L"],
    }
)
