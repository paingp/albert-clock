import sys
from datetime import datetime
import time
import threading

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5 import QtGui
from PyQt5 import QtCore

from alg_test import EquationAlg

from get_time import create_equation


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
            hour_eqn = create_equation(hour)
            min_eqn = create_equation(minute)
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
        self.showMaximized()

        # WIDGETS
        # time label
        cur_time_str = datetime.now().strftime('%H:%M:%S %p')
        self.time_label = QLabel(cur_time_str, self)
        self.time_label.setFont(QtGui.QFont("Arial", 40))
        #self.time_label.setGeometry(0,0,500,100)

        # change time mode button
        self.change_time_mode_button = QPushButton('Change Time Mode', self)
        self.change_time_mode_button.setCheckable(True)

        # change mode button
        self.change_diff_mode_button = QPushButton('Change Diff Mode', self)
        self.change_diff_mode_button.setCheckable(True)
        # dark mode button
        self.dark_mode_button = QPushButton('Dark Mode', self)
        self.dark_mode_button.setCheckable(True)
        # answer label
        self.answer_label = QLabel("", self)
        self.answer_label.setFont(QtGui.QFont("Arial", 30))
        #self.answer_label.setGeometry(0,0,500,100)

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
        layout.addWidget(self.dark_mode_button)

        # set layout
        self.setLayout(layout)

    @QtCore.pyqtSlot(str)
    def updateTimeDisplay(self, time_str):
        self.time_label.setText(time_str)
        self.updateTimeDoneSig.emit(time_str)

    @QtCore.pyqtSlot(str)
    def updateAnsDisplay(self, time_str):
        self.answer_label.setText(time_str)
        
      # dark mode changing color theme
    @QtCore.pyqtSlot()
    def toggleDarkMode(self):
        # the text kept going up and down when switching modes, so i had to set the font for everything again
        time_font = QtGui.QFont("Arial", 40)
        time_font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        time_font.setHintingPreference(QtGui.QFont.PreferNoHinting)
    
        answer_font = QtGui.QFont("Arial", 30)
        answer_font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        answer_font.setHintingPreference(QtGui.QFont.PreferNoHinting)
    
        # aligning the font and time consistently
        self.time_label.setFont(time_font)
        self.time_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.time_label.setContentsMargins(0, 0, 0, 0)
    
        self.answer_label.setFont(answer_font)
        self.answer_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.answer_label.setContentsMargins(0, 0, 0, 0)
    
        if self.dark_mode_button.isChecked():
            # dark mode stylesheet
            self.setStyleSheet("""
                QWidget {
                    background-color: #000000;
                    color: #ffffff;
                }
                QLabel {
                    background-color: transparent;
                    color: #ffffff;
                    margin: 0px;
                    padding: 0px;
                    border: 0px;
                }
                QPushButton {
                    background-color: #000000;
                    color: #ffffff;
                    border: 1px solid #333333;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:checked {
                background-color: #1a1a1a;
                }
                QPushButton:hover {
                    background-color: #0d0d0d;
                }
            """)
        else:
                # light mode stylesheet (kept showing the hover thing so i just added it so it's consistent)
                self.setStyleSheet("""
                    QWidget {
                        background-color: #ffffff;
                        color: #000000;
                    }
                    QLabel {
                        background-color: transparent;
                        color: #000000;
                        margin: 0px;
                        padding: 0px;
                        border: 0px;
                    }
                    QPushButton {
                        background-color: #f0f0f0;
                        color: #000000;
                        border: 1px solid #999999;
                        padding: 5px;
                        border-radius: 3px;
                    }
                    QPushButton:checked {
                        background-color: #dcdcdc;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """)
        

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
        
        # gui->dark mode toggle signal (switches between light and dark themes)
        self.gui.dark_mode_button.clicked.connect(self.gui.toggleDarkMode)
        
def main():
    # create app
    app = QApplication(sys.argv)
    myApp = MyApp(app)

    # start the app
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
