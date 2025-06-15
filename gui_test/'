import sys
from datetime import datetime
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5 import QtGui
from PyQt5 import QtCore


class UpdateMinObject(QtCore.QObject):

    signalUpdateTime = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @QtCore.pyqtSlot()
    def startWork(self, eqn_period=60):
        print("STARTING WORK")
        while True:
            cur_sec = datetime.now().second
            time.sleep(eqn_period - cur_sec)

            time_str = datetime.now().strftime('%H:%M:%S %p')
            self.signalUpdateTime.emit(time_str)


class MyWindow(QWidget):

    def __init__(self):
        super().__init__()

        # set up window
        self.setWindowTitle("test clock")
        self.setGeometry(100, 100, 400, 200)

        # WIDGETS
        # label
        cur_time_str = datetime.now().strftime('%H:%M:%S %p')
        self.label = QLabel(cur_time_str, self)
        self.label.setFont(QtGui.QFont("Arial", 40))
        self.label.setGeometry(0,0,500,100)
        # button
        # self.button_start = QPushButton('Start', self)

        # add all widgets to layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        # layout.addWidget(self.button_start)

        self.setLayout(layout)


    @QtCore.pyqtSlot(str)
    def updateTime(self, time_str):
        self.label.setText(time_str)


class MyApp(QtCore.QObject):

    signalStartUpdateTimeThread = QtCore.pyqtSignal()

    def __init__(self, app, parent=None):
        super().__init__(parent)

        # Connect to app
        self.app = app

        # Create gui
        self.gui = MyWindow()
        self.gui.show()

        # Start worker thread
        self.runWorkerThread()

    def runWorkerThread(self):
        # Setup worker object and start worker thread
        self.worker = UpdateMinObject()
        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        # Connect worker signals and tell worker to start working
        self.worker.signalUpdateTime.connect(self.gui.updateTime)
        self.signalStartUpdateTimeThread.connect(self.worker.startWork)

        # Start time update thread after wait
        time.sleep(0.5)
        self.signalStartUpdateTimeThread.emit()
        

def main():
    app = QApplication(sys.argv)
    myApp = MyApp(app)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
