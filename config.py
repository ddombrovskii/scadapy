# GUI APPLICATION SETTINGS
APPLICATION_NAME = 'SCADA'
APPLICATION_GEOMETRY_X = 100
APPLICATION_GEOMETRY_Y = 100
APPLICATION_GEOMETRY_W = 800
APPLICATION_GEOMETRY_H = 800
PLOT_SIZE_LIMIT = 30
PLOT_COLOR_LIST = ['blue',
                   'green',
                   'red',
                   'cyan',
                   'magenta',
                   'black']

SERVERS_CONFIG_FILE = 'modbus-config.yaml'

SERVERS_HOST = 'localhost'

DATATYPES_DICT = {
    "word": 1,
    "float": 2,
    "shortint": 0,
    "integer": 2,
    "dword": 2,
    "int64": 4,
    "bool": 0,
    "datetime": 4,
    "double": 4,
    "string": 2
}
