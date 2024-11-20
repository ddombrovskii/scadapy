import config
import datetime
import yaml

from .server import Server

from pyModbusTCP.utils import decode_ieee, word_list_to_long

from PySide6 import QtWidgets

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, reg_addr=0, reg_nb=2, client=None):
        self.figure = Figure()
        super().__init__(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.x_data = []
        self.y_data = []

        self.client = client
        self.reg_addr = reg_addr
        self.reg_nb = reg_nb

        self.animation = FuncAnimation(self.figure, self.update_plot, fargs=(self.x_data, self.y_data), interval=100)
        self.draw()

    def update_plot(self, frame, xs, ys):

        read_reg = self.client.read_holding_registers(self.reg_addr, self.reg_nb)

        if read_reg:
            value = [decode_ieee(f) for f in word_list_to_long(read_reg)][0]
            print('read reg_addr 0 reg_nb 2')
        else:
            value = 0
            print('unable to read registers')

        xs.append(datetime.datetime.now().strftime('%H:%M:%S %f'))
        ys.append(value)

        size_limit = config.PLOT_SIZE_LIMIT
        xs = xs[-size_limit:]
        ys = ys[-size_limit:]

        self.ax.clear()
        self.ax.plot(xs, ys)

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
