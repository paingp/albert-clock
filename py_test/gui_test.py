import sys
import os
import time

from datetime import datetime
import threading

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5 import QtGui
from PyQt5 import QtCore

from alg_test import EquationAlg

from get_time import create_equation

import pigpio
from ir_hasher import hasher



class IRWorker(QtCore.QObject):

    cycle_time_mode_sig = QtCore.pyqtSignal()
    cycle_diff_mode_sig = QtCore.pyqtSignal()
    toggle_answer_flag_sig = QtCore.pyqtSignal()
    toggle_dark_mode_sig = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # start pigpiod
        os.system("sudo pigpiod")

        self.gpio_ir = 17

        self.pi = pigpio.pi()
        if (not self.pi.connected):
            print(f"Error: pigpio failed to connected")
            exit()
        
        self.hashes = {
            1902227973: '1',
            435909485: '2',
            2736323565: '3',
            430130277: '4',
        }

        self.ir = hasher(self.pi, self.gpio_ir, self.cbFunc)

        print("IR WORKER INITIALIZED")

    def _destroy(self):
        self.ir._destroy()

    def cbFunc(self, hash):
        clicked = "UNKNOWN"

        if (hash in self.hashes):
            clicked = self.hashes[hash]

            match (clicked):
                case '1': 
                    print("1 CLICKED")
                    print("Signal object ID at emit:", id(self.cycle_time_mode_sig))
                    self.cycle_time_mode_sig.emit()
                case '2':
                    print("2 CLICKED")
                    self.cycle_diff_mode_sig.emit()
                case '3':
                    print("3 CLICKED")
                    self.toggle_answer_flag_sig.emit()
                case '4':
                    print("4 CLICKED")
                    self.toggle_dark_mode_sig.emit()



class TimeWorker(QtCore.QObject):

    update_time_sig = QtCore.pyqtSignal(str)
    update_ans_sig = QtCore.pyqtSignal(str)
    update_dark_sig = QtCore.pyqtSignal(bool)

    def __init__(self, alg, parent=None):
        super().__init__(parent)

        self.work_flag = True
        self.work_flag_lock = threading.Lock()

        self.alg = alg

        self.time_modes = ['am', 'military']
        self.num_time_modes = len(self.time_modes)
        self.time_mode_ind = 0
        self.time_mode_ind_lock = threading.Lock()

        self.diff_modes = ['easy', 'hard']
        self.num_diff_modes = len(self.diff_modes)
        self.diff_mode_ind = 0
        self.diff_mode_ind_lock = threading.Lock()

        self.answer_flag = False
        self.answer_flag_lock = threading.Lock()

        self.dark_mode = False
        self.dark_mode_lock = threading.Lock()

        print("TIME WORKER INITIALIZED")

    # Get Methods w/ thread lock
    def getWorkFlag(self):
        work_flag = False

        self.work_flag_lock.acquire()
        work_flag = self.work_flag
        self.work_flag_lock.release()

        return work_flag

    def getTimeModeInd(self):
        time_mode_ind = -1

        self.time_mode_ind_lock.acquire()
        time_mode_ind = self.time_mode_ind
        self.time_mode_ind_lock.release()

        return time_mode_ind;

    def getTimeMode(self):
        time_mode = ""
        
        time_mode_ind = self.getTimeModeInd()

        if (time_mode_ind < self.num_time_modes):
            time_mode = self.time_modes[time_mode_ind]

        return time_mode

    def getDiffModeInd(self):
        diff_mode_ind = -1

        self.diff_mode_ind_lock.acquire()
        diff_mode_ind = self.diff_mode_ind
        self.diff_mode_ind_lock.release()

        return diff_mode_ind;

    def getDiffMode(self):
        diff_mode = ""
        
        diff_mode_ind = self.getDiffModeInd()

        if (diff_mode_ind < self.num_diff_modes):
            diff_mode = self.diff_modes[diff_mode_ind]

        return diff_mode

    def getAnswerFlag(self):
        answer_flag = False

        self.answer_flag_lock.acquire()
        answer_flag = self.answer_flag
        self.answer_flag_lock.release()

        return answer_flag

    def getDarkMode(self):
        dark_mode = False

        self.dark_mode_lock.acquire()
        dark_mode = self.dark_mode
        self.dark_mode_lock.release()

        return dark_mode

    # Set Methods w/ thread lock
    def setWorkFlag(self, work_flag:bool):
        self.work_flag_lock.acquire()
        self.work_flag = work_flag
        self.work_flag_lock.release()

    def setTimeModeInd(self, ind:int):
        if (ind < 0) or (ind >= self.num_time_modes): return

        self.time_mode_ind_lock.acquire()
        self.time_mode_ind = ind
        self.time_mode_ind_lock.release()

    def setDiffModeInd(self, ind:int):
        if (ind < 0) or (ind >= self.num_diff_modes): return

        self.diff_mode_ind_lock.acquire()
        self.diff_mode_ind = ind 
        self.diff_mode_ind_lock.release()

    def setAnswerFlag(self, answer_flag:bool):
        self.answer_flag_lock.acquire()
        self.answer_flag = answer_flag
        self.answer_flag_lock.release()

    def setDarkMode(self, dark_mode:bool):
        self.dark_mode_lock.acquire()
        self.dark_mode = dark_mode
        self.dark_mode_lock.release()

    # Update methods
    def IncrementTimeModeInd(self):
        next_ind = (self.getTimeModeInd() + 1) % self.num_time_modes
        setTimeMode(next_ind)

    def IncrementDiffModeInd(self):
        next_ind = (self.getDiffModeInd() + 1) % self.num_diff_modes
        setDiffMode(next_ind)

    # Send signal methods
    def sendUpdateTimeLabelSig(self, time_str:str):
        self.update_time_sig.emit(time_str)

    def sendUpdateAnsLabelSig(self, ans_time_str:str):
        self.update_ans_sig.emit(ans_time_str)

    def sendUpdateDarkModeSig(self, dark_mode:bool):
        self.update_dark_sig.emit(dark_mode)

    # Get time string methods
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
        diff_mode = self.getDiffMode()

        if (diff_mode == 'easy'):
            hour_eqn = create_equation(hour)
            min_eqn = create_equation(minute)
        elif (diff_mode == 'hard'):
            hour_eqn = self.alg.getRandomEqn(hour)
            min_eqn = self.alg.getRandomEqn(minute)

        time_str = f"{hour_eqn}  :  {min_eqn}" + meridian

        return time_str

    def getAnswerStr(self, show_answer_flag):
        time_str = ""

        if (show_answer_flag):
            now = datetime.now()
            meridian = f"  {now.strftime('%p')}"
            hour = now.hour
            minute = now.minute

            if (self.getTimeMode() == 'am'):
                if (hour != 12): hour = hour % 12
            else:
                meridian = ""

            time_str = f"{hour}  :  {minute}" + meridian

        return time_str

    # Process IR rx msgs
    def CycleTimeMode(self):
        print("HEREEEEE")
        self.IncrementTimeModeInd()
        print(f"UPDATING TIME_MODE TO {self.getTimeMode()}")

        time_str = self.getTimeEqnStr()
        self.sendUpdateTimeLabelSig(time_str)

        # sync answer's string to correct time_mode if it's being shown as well
        if (self.getAnswerFlag()):
            ans_time_str = self.getAnswerStr(answer_flag)
            self.sendUpdateAnsLabelSig(ans_time_str)

    def CycleDiffMode(self):
        self.IncrementDiffModeInd()
        print(f"UPDATING TIME_MODE TO {self.getDiffMode()}")

        time_str = self.getTimeEqnStr()
        self.sendUpdateTimeLabelSig(time_str)

    def toggleAnswerFlag(self):
        toggled = not (self.getAnswerFlag())
        self.setAnswerFlag(toggled)

        answer_flag = self.getAnswerFlag()
        print(f"UPDATING ANSWER_FLAG TO {answer_flag}")

        ans_time_str = self.getAnswerStr(answer_flag)
        self.sendUpdateAnsLabelSig(ans_time_str)
        
    def toggleDarkMode(self):
        toggled = not (self.getDarkMode())
        self.setDarkMode(toggled)

        dark_mode = self.getDarkMode()
        print(f"UPDATING DARK_MODE TO {dark_mode}")

        self.sendUpdateDarkModeSig(dark_mode)

    # Thread method for self update every minute
    def startTimeThread(self, eqn_period=60):
        print("STARTING TIME THREAD")
        self.setWorkFlag(True);

        while (self.getWorkFlag()):
            # wait till the start of next period
            cur_sec = datetime.now().second
            time.sleep(eqn_period - cur_sec)

            # update display
            time_str = self.getTimeEqnStr()
            self.update_time_sig.emit(time_str)

    def stopTimeThread(self):
        self.setWorkFlag(False);



class MyWindow(QWidget):

    def __init__(self):
        super().__init__()

        # SET UP WINDOW
        self.setWindowTitle("test clock")
        self.showMaximized()

        # WIDGETS
        # time label
        cur_time_str = datetime.now().strftime('%H:%M:%S %p')
        self.time_label = QLabel(cur_time_str, self)
        self.time_label.setFont(QtGui.QFont("Arial", 40))
        #self.time_label.setGeometry(0,0,500,100)

        # answer label
        self.answer_label = QLabel("", self)
        self.answer_label.setFont(QtGui.QFont("Arial", 30))
        #self.answer_label.setGeometry(0,0,500,100)

        # add all widgets to layout
        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.answer_label)

        # set layout
        self.setLayout(layout)

        print("WINDOW INITIALIZED")

    @QtCore.pyqtSlot(str)
    def updateTimeDisplay(self, time_str):
        self.time_label.setText(time_str)

    @QtCore.pyqtSlot(str)
    def updateAnsDisplay(self, time_str):
        self.answer_label.setText(time_str)

    # dark mode changing color theme
    @QtCore.pyqtSlot(bool)
    def updateDarkMode(self, dark_mode):
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

        if dark_mode:
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
            """)



class MyApp(QtCore.QObject):

    start_update_time_thread_sig = QtCore.pyqtSignal()

    def __init__(self, app, parent=None):
        super().__init__(parent)

        # Connect to app
        self.app = app

        # Create equation generator
        self.alg = EquationAlg()

        # Create gui
        self.gui = MyWindow()
        self.gui.show()

        # Configure IR daemon
        self.ir_worker = IRWorker()

        # Set up time worker thread
        self.time_worker = TimeWorker(self.alg)
        self.time_worker_thread = QtCore.QThread()

        self.runWorkerThreads()

        print("APP INITIALIZED")

    def _destroy(self):
        self.ir_worker._destroy()

        self.time_worker.stopTimeThread()
        self.time_worker_thread.wait()

    def runWorkerThreads(self):
        self.time_worker.moveToThread(self.time_worker_thread)
        self.time_worker_thread.start()

        # Connect worker threads
        self.connectWorkerThreads()

        # Start timer thread
        time.sleep(0.2)
        self.start_update_time_thread_sig.emit()

    def connectWorkerThreads(self):
        # IR -> TimeWorker
        self.ir_worker.cycle_time_mode_sig.connect(self.time_worker.CycleTimeMode)
        print("Signal object ID at connect:", id(self.ir_worker.cycle_time_mode_sig))
        self.ir_worker.cycle_diff_mode_sig.connect(self.time_worker.CycleDiffMode)
        self.ir_worker.toggle_answer_flag_sig.connect(self.time_worker.toggleAnswerFlag)
        self.ir_worker.toggle_dark_mode_sig.connect(self.time_worker.toggleDarkMode)

        # TimeWorker -> Gui
        self.time_worker.update_time_sig.connect(self.gui.updateTimeDisplay)
        self.time_worker.update_ans_sig.connect(self.gui.updateAnsDisplay)
        self.time_worker.update_dark_sig.connect(self.gui.updateDarkMode)

        # app->worker start time thread signal
        self.start_update_time_thread_sig.connect(self.time_worker.startTimeThread)

