import config
import datetime
import yaml
import random
import asyncio
import threading

from .server import Server
from .db import DataServer

from pyModbusTCP.utils import decode_ieee, word_list_to_long

from PySide6 import QtWidgets

import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, reg_addr=0, reg_nb=2, client=None):
        self.animation = None
        self.figure = Figure()
        super().__init__(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.x_data = []
        self.y_data = []

        self.client = client
        self.reg_addr = reg_addr
        self.reg_nb = reg_nb

        self.database = DataServer(client.port, reg_addr, {})

        self.loop = asyncio.get_event_loop()
        if not self.loop.is_running():
            threading.Thread(target=self.loop.run_forever, daemon=True).start()
        self.loop.call_soon_threadsafe(asyncio.create_task, self.update_data())

        self.start_animation()

    async def update_data(self):
        while True:
            read_reg = self.client.read_holding_registers(self.reg_addr, self.reg_nb)

            if read_reg:
                value = [decode_ieee(f) for f in word_list_to_long(read_reg)][0]
                # print('read reg_addr 0 reg_nb 2')
            else:
                value = 0
                # print('unable to read registers')

            self.x_data.append(datetime.datetime.now().strftime('%H:%M:%S:%f'))
            self.y_data.append(value)

            await asyncio.sleep(0.1)

    def start_animation(self):
        color = config.PLOT_COLOR_LIST[random.randint(0, len(config.PLOT_COLOR_LIST) - 1)]

        self.animation = FuncAnimation(self.figure,
                                       self.update_plot,
                                       fargs=(self.x_data, self.y_data, color),
                                       interval=300)

        self.draw()

    def update_plot(self, frame, xs, ys, color):

        size_limit = config.PLOT_SIZE_LIMIT
        xs = xs[-size_limit:]
        ys = ys[-size_limit:]

        values_dict = {xs[i]: ys[i] for i in range(len(xs))}
        if self.database.data_created():
            self.database.update(values_dict)
        else:
            self.database.insert(values_dict)

        self.ax.clear()
        self.ax.plot(xs, ys, color=color)

        self.ax.grid()
        self.ax.set_xticks([i for i in range(len(xs))])
        self.ax.set_xticklabels(xs, rotation=45, ha='right')
        self.figure.subplots_adjust(bottom=0.4)


class PlotsTab(QtWidgets.QWidget):
    def __init__(self, parent=None, server=None):
        super().__init__(parent)
        self.server = server

        self.plots = []
        self.layout = QtWidgets.QVBoxLayout(self)
        self.create_plots()

    def create_plots(self):
        for reg_addr, reg_nb in self.server.regs.items():
            plot = PlotCanvas(self, reg_addr, reg_nb, self.server.get_connection())
            self.layout.addWidget(plot)


class Application(QtWidgets.QMainWindow):
    def __init__(self, config_file_name=config.SERVERS_CONFIG_FILE):
        super().__init__()
        self.config_file_name = config_file_name
        self.servers_list = []
        self.load_servers_from_config_file()

        self.setWindowTitle(config.APPLICATION_NAME)
        self.setGeometry(config.APPLICATION_GEOMETRY_X, config.APPLICATION_GEOMETRY_Y,
                         config.APPLICATION_GEOMETRY_W, config.APPLICATION_GEOMETRY_H)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QtWidgets.QVBoxLayout(central_widget)

        self.tabs_widget = QtWidgets.QTabWidget()
        self.layout.addWidget(self.tabs_widget)

        self.create_tabs_from_servers()

    def add_plot_tab(self, server):
        tab = PlotsTab(self.tabs_widget, server)
        self.tabs_widget.addTab(tab, 'port ' + str(server.port))

    def create_tabs_from_servers(self):
        for server in self.servers_list:
            self.add_plot_tab(server)

    def load_servers_from_config_file(self):
        try:
            with open(self.config_file_name, 'r') as file:
                config_file = yaml.safe_load(file)

                for server in config_file['servers']:
                    new_server = Server(server_info=server)
                    self.servers_list.append(new_server)

        except FileNotFoundError as e:
            raise
