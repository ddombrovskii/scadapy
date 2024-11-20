import config

from pyModbusTCP.client import ModbusClient


class Server:
    def __init__(self, server_info=None, host='localhost'):
        self.connection = None
        self.port = None
        self.host = host
        self.regs = {}  # {reg_addr: reg_nb}

        self.parse_server_info(server_info)
        self.create_connection()

    def create_connection(self):
        self.connection = ModbusClient(host=self.host, port=self.port)

    def add_reg(self, reg_addr, reg_num):
        self.regs[reg_addr] = reg_num

    def get_connection(self):
        return self.connection

    def parse_server_info(self, server_info: dict):
        self.port, raw_regs_list = list(server_info.items())[0]
        self.convert_raw_reg_list(raw_regs_list)

    def convert_raw_reg_list(self, raw_regs_list):
        for reg in raw_regs_list:
            print(list(reg.values()))
            reg_data = list(reg.values())
            self.add_reg(reg_data[0]['reg_addr'],config.DATATYPES_DICT[reg_data[0]['reg_type'].lower()])