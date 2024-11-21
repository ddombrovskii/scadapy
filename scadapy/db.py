import psycopg2
import json


class DataServer:
    def __init__(self, server_port, reg_addr, values):
        self.server_port = server_port
        self.reg_addr = reg_addr
        self.values = values

        self.cursor = None
        self.data_by_reg_addr_created = False

        self.create_connection()
        self.clear_table()

    def create_connection(self):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="12345678", host="127.0.0.1")
        conn.autocommit = True
        self.cursor = conn.cursor()

    def clear_table(self):
        self.cursor.execute("DELETE FROM modbus WHERE server_num = %s AND reg_addr = %s;",
                            (self.server_port, self.reg_addr))

    def data_created(self):
        return self.data_by_reg_addr_created

    def insert(self, values: dict):
        self.cursor.execute("INSERT INTO modbus (server_num, reg_addr, values) VALUES (%s, %s, %s);",
                            (self.server_port, self.reg_addr, json.dumps(values)))

        self.data_by_reg_addr_created = True

    def update(self, values: dict):
        self.cursor.execute("UPDATE modbus SET values = %s WHERE server_num = %s AND reg_addr = %s;",
                            (json.dumps(values), self.server_port, self.reg_addr))
