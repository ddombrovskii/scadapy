import sys

from scadapy import Application
from PySide6 import QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print(e)
