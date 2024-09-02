from PyQt6.QtCore import pyqtSignal, Qt, QThread
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QProgressBar
import sys
import time

class SimulateProcess(QThread):
    finished = pyqtSignal()

    def setParams(self, bar):
        self.bar = bar

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        count = 0
        while self.running:
            if count < 100:
                count = count + 1
            time.sleep(0.55)
            self.bar.update_progress(count)

class ProgressBar(QWidget):
    close_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.resize(400, 50)
        self.progress_bar.setTextVisible(False)  # 隐藏百分比文本
        
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid green;
                border-radius: 5px;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 20px;
            }
        """)

        self.layout.addWidget(self.progress_bar)
        self.setLayout(self.layout)

        self.close_signal.connect(self.close)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def show(self):
        self.center_on_main_window()
        super().show()

    def center_on_main_window(self):
        parent_geometry = self.parent().geometry()
        print(parent_geometry)
        popup_geometry = self.geometry()
        x = parent_geometry.width() // 2 - popup_geometry.width() // 2
        y = parent_geometry.height() // 2- popup_geometry.height() // 2
        print(popup_geometry)
        self.move(x, y)