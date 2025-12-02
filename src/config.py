import board

GRAPHQL_HOST = "localhost"
GRAPHQL_PORT = 5000
GRAPHQL_PATH = "/"

led_pins = [
    {
        "PIN": board.D18,
        "COUNT": 72
    },
]

led_segments = [
    {
        "name": "HALL3",
        "span": 14,
        "reversed": False
    },
    {
        "name": "HALL2",
        "span": 14,
        "reversed": False
    },
        {
        "name": "HALL1",
        "span": 13,
        "reversed": False
    },
        {
        "name": "HALL0",
        "span": 31,
        "reversed": False
    },
]

devices = (
    {
        "id": 0,
        "LED_SEGMENTS": ["HALL0"],
        "AIR_DIN_PIN": board.D24,
        "AIR_DIN_PIN_INVERT": True
    }, {
        "id": 1,
        "LED_SEGMENTS": ["HALL1"],
    }, {
        "id": 2,
        "LED_SEGMENTS": ["HALL2"],
    }, {
        "id": 3,
        "LED_SEGMENTS": ["HALL3"],
        "AIR_DIN_PIN": board.D23,
        "AIR_DIN_PIN_INVERT": True
    }
)
