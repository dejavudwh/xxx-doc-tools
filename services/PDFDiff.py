import ctypes
from PyQt6.QtCore import QThread, pyqtSignal

class DiffPDFWorker(QThread):
    finished = pyqtSignal()

    def setParams(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def run(self):
        try:
            print("开始对比PDF文件")
            dll = ctypes.CDLL('./backend/diff-pdf/build/ued_doc_tools-win-0.5.2/windist/msys-diff-pdf.dll')
            # dll = ctypes.CDLL('./msys-diff-pdf.dll')
            dll.export_diff_pdf(self.file1, self.file2, b'diff.pdf')
            self.finished.emit()  # 任务完成时发射完成信号
            print("结束")
        except Exception as e:
            print(f"Exception caught in thread: {e}")