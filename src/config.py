WIFI_SSID = "JimmyXPS"
WIFI_PASSWORD = "ashvbiqbrglncawuhciuwli"

GRAPHQL_HOST = "192.168.12.1"
GRAPHQL_PORT = 5000
GRAPHQL_PATH = "/"

led_pins = [
    {
        "PIN": 1,
        "COUNT": 2
    },
    {
        "PIN": 3,
        "COUNT": 5,
    }
]

led_segments = [
    {
        "name": "ROOM1L",
        "span": 5,
        "reversed": False
    },
    {
        "name": "ROOM1R",
        "span": 5,
        "reversed": False
    }
]

devices = (
    {
        "id": 0,
        #"DHT_PIN": 26,
        "PRESENCE_PIN": 35,
        "PRESENCE_TX_PIN": 18,
        "PRESENCE_RX_PIN": 5,
        "PRESENCE_UART_CONTROLLER": 2,
        "LED_SEGMENTS": ["ROOM1L", "ROOM1R"],
        # "AIR_DIN_PIN": 5,
        #"AIR_ADC_PIN": 32
    }, {
        "id": 1,
        # "DHT_PIN": 26,
        # "PRESENCE_PIN": 35,
        # "PRESENCE_TX_PIN": 1,
        # "PRESENCE_RX_PIN": 3,
        # "PRESENCE_UART_CONTROLLER": 0,
        # "AIR_DIN_PIN": 5,
        # "AIR_ADC_PIN": 32
        "LED_SEGMENTS": [],
    }
)
