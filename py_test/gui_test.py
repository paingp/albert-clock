import sys
from datetime import datetime
import time
import threading

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5 import QtGui
from PyQt5 import QtCore

from alg_test import EquationAlg
# TO DO import your own equation here

class Worker(QtCore.QObject):

    updateTimeSig = QtCore.pyqtSignal(str)
    updateAnsSig = QtCore.pyqtSignal(str)

    def __init__(self, alg, time_mode='am', diff_mode='easy', parent=None):
        super().__init__(parent)

        self.alg = alg

        # check time mode validity
        self.valid_time_modes = {'am', 'military'}
        if (time_mode not in self.valid_time_modes):
            print(f"Error: invalid time mode {time_mode}, expecting: {self.valid_time_modes}")
            sys.exit(-1)

        # check difficuly mode validity
        self.valid_diff_modes = {'easy', 'hard'}
        if (diff_mode not in self.valid_diff_modes):
            print(f"Error: invalid diff mode {diff_mode}, expecting: {self.valid_diff_modes}")
            sys.exit(-1)

        self.time_mode = time_mode
        self.time_mode_lock = threading.Lock()

        self.diff_mode = diff_mode
        self.diff_mode_lock = threading.Lock()

    def getTimeMode(self):
        time_mode = ''

        self.time_mode_lock.acquire()
        time_mode = self.time_mode
        self.time_mode_lock.release()

        return time_mode

    def getDiffMode(self):
        diff_mode = ''

        self.diff_mode.acquire()
        diff_mode = self.diff_mode
        self.diff_mode.release()

        return diff_mode

    @QtCore.pyqtSlot()
    def getTimeEqnStr(self):
        time_str = ""
        
        # get current hour and min
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        # get meridian string
        meridian = f"  {now.strftime('%p')}"
        if (self.getTimeMode() == 'am'):
            if (hour != 12): hour = hour % 12
        else:
            meridian = ""

        # get equation
        hour_eqn, min_eqn = "", ""
        if (self.diff_mode == 'easy'):
            # TO DO: generate your own equation for hour_eqn and min_eqn here if diff_mode is easy
            hour_eqn = "HOUR"
            min_eqn = "MIN"
        elif (self.diff_mode == 'hard'):
            hour_eqn = self.alg.getRandomEqn(hour)
            min_eqn = self.alg.getRandomEqn(minute)

        time_str = f"{hour_eqn}  :  {min_eqn}" + meridian

        return time_str

    @QtCore.pyqtSlot()
    def updateTimeMode(self, time_mode):
        print(f"UPDATING TIME_MODE TO {time_mode}")
        # update mode
        self.time_mode_lock.acquire()
        self.time_mode = time_mode
        self.time_mode_lock.release()

        # update display to reflect
        time_str = self.getTimeEqnStr()
        self.updateTimeSig.emit(time_str)

    @QtCore.pyqtSlot()
    def updateDiffMode(self, diff_mode):
        print(f"UPDATING DIFF_MODE TO {diff_mode}")
        # update mode
        self.diff_mode_lock.acquire()
        self.diff_mode = diff_mode
        self.diff_mode_lock.release()

        # update display to reflect
        time_str = self.getTimeEqnStr()
        self.updateTimeSig.emit(time_str)

    @QtCore.pyqtSlot()
    def getAnswerStr(self, show_flag):
        print("TOGGLING ANSWER STR")

        time_str = ""

        if (show_flag):
            now = datetime.now()
            meridian = f"  {now.strftime('%p')}"
            hour = now.hour
            minute = now.minute

            if (self.getTimeMode() == 'am'):
                if (hour != 12): hour = hour % 12
            else:
                meridian = ""

            time_str = f"{hour}  :  {minute}" + meridian

        self.updateAnsSig.emit(time_str)

    @QtCore.pyqtSlot()
    def startTimeThread(self, eqn_period=60):
        print("STARTING TIME THREAD")
        while True:
            # wait till the start of next period
            cur_sec = datetime.now().second
            time.sleep(eqn_period - cur_sec)

            # update display
            time_str = self.getTimeEqnStr()
            self.updateTimeSig.emit(time_str)


class MyWindow(QWidget):

    updateTimeDoneSig = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # set up window
        self.setWindowTitle("test clock")
        self.setGeometry(100, 100, 400, 200)

        # WIDGETS
        # time label
        cur_time_str = datetime.now().strftime('%H:%M:%S %p')
        self.time_label = QLabel(cur_time_str, self)
        self.time_label.setFont(QtGui.QFont("Arial", 40))
        self.time_label.setGeometry(0,0,500,100)

        # change time mode button
        self.change_time_mode_button = QPushButton('Change Time Mode', self)
        self.change_time_mode_button.setCheckable(True)

        # change mode button
        self.change_diff_mode_button = QPushButton('Change Diff Mode', self)
        self.change_diff_mode_button.setCheckable(True)

        # answer label
        self.answer_label = QLabel("", self)
        self.answer_label.setFont(QtGui.QFont("Arial", 30))
        self.answer_label.setGeometry(0,0,500,100)

        # show answer button
        self.show_answer_button = QPushButton('Show Answer', self)
        self.show_answer_button.setCheckable(True)

        # add all widgets to layout
        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.change_time_mode_button)
        layout.addWidget(self.change_diff_mode_button)
        layout.addWidget(self.answer_label)
        layout.addWidget(self.show_answer_button)

        # set layout
        self.setLayout(layout)

    @QtCore.pyqtSlot(str)
    def updateTimeDisplay(self, time_str):
        self.time_label.setText(time_str)
        self.updateTimeDoneSig.emit(time_str)

    @QtCore.pyqtSlot(str)
    def updateAnsDisplay(self, time_str):
        self.answer_label.setText(time_str)



class MyApp(QtCore.QObject):

    startUpdateTimeThreadSig = QtCore.pyqtSignal()

    def __init__(self, app, parent=None):
        super().__init__(parent)

        # Connect to app
        self.app = app

        # Create equation generator
        self.alg = EquationAlg()

        # Create gui
        self.gui = MyWindow()
        self.gui.show()

        # Start worker thread
        self.runWorkerThread()

    def runWorkerThread(self):
        # Setup worker object and start worker thread
        self.worker = Worker(self.alg)
        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        # CONNECT SIGNALS
        # worker->gui update time label signal
        self.worker.updateTimeSig.connect(self.gui.updateTimeDisplay)

        # worker->gui update answer label signal
        self.worker.updateAnsSig.connect(self.gui.updateAnsDisplay)

        # gui->worker update time mode signal (lambda function to translate button toggle state -> time mode string)
        self.gui.change_time_mode_button.clicked.connect(
            lambda: self.worker.updateTimeMode("am" if self.gui.change_time_mode_button.isChecked() else "military")
        )

        # gui->worker update diff mode signal (lambda function to translate button toggle state -> diff mode string)
        self.gui.change_diff_mode_button.clicked.connect(
            lambda: self.worker.updateDiffMode("easy" if self.gui.change_diff_mode_button.isChecked() else "hard")
        )

        # gui->worker show answer signal (use button toggle state as flag to show/hide answer)
        self.gui.show_answer_button.clicked.connect(
            lambda: self.worker.getAnswerStr(self.gui.show_answer_button.isChecked())
        )

        # gui->worker time updated signal (so we can sync answer string if show answer is toggled)
        self.gui.updateTimeDoneSig.connect(
            lambda: self.worker.getAnswerStr(self.gui.show_answer_button.isChecked())
        )

        # app->worker start time thread signal
        self.startUpdateTimeThreadSig.connect(self.worker.startTimeThread)

        # Start time update thread after wait
        time.sleep(0.2)
        self.startUpdateTimeThreadSig.emit()
        

def main():
    # create app
    app = QApplication(sys.argv)
    myApp = MyApp(app)

    # start the app
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
