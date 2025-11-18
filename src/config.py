import board

GRAPHQL_HOST = "localhost"
GRAPHQL_PORT = 5000
GRAPHQL_PATH = "/"

led_pins = [
    {
        "PIN": board.D18,
        "COUNT": 120
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
        "LED_SEGMENTS": ["ROOM1R", "ROOM1L"],
        # "AIR_DIN_PIN": ,
    }, {
        "id": 1,
        "LED_SEGMENTS": ["ROOM2R", "ROOM2L"],
    },
)
