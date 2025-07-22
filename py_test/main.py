import os
import sys
import signal

from PyQt5.QtWidgets import QApplication
from gui_test import MyApp

def main():
    # create app
    app = QApplication(sys.argv)
    myApp = MyApp(app)

    signal.signal(signal.SIGINT, myApp._destroy)

    # start the app
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
