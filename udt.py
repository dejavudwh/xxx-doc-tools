import sys
from functools import partial
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QTreeWidget, 
                             QTreeWidgetItem, QSplitter, QFileDialog,
                             QWidget, QStackedWidget)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QAction
from views.PDFPreviewer import PDFPreviewer
from views.CompareDialog import CompareDialog
from views.OutputWidget import OutputWidget
from views.ProgressBar import ProgressBar, SimulateProcess
from views.BasicErrorCheckPanel import BasicErrorCheckPanel
from views.TableComparePanel import TableComparePanel
from config.config import WINDOWS_WIDTH, WINDOWS_HEIGHT

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print('aaa')
        self.init_ui()
        self.init_workers()

    def init_ui(self):
        self.setWindowTitle("UED Doc Tools")
        self.resize(WINDOWS_WIDTH, WINDOWS_HEIGHT)

        self.init_menu()
        self.init_widget()

        self.init_layout()

    def init_menu(self):
        menu_bar = self.menuBar()
        task_menu = menu_bar.addMenu("创建任务")
        setting_menu = menu_bar.addMenu("设置")
        help_menu = menu_bar.addMenu("帮助")
        about_menu = menu_bar.addMenu("关于")

        self.error_check = QAction("低错排查", self)
        self.doc_compare = QAction("文档对比", self)
        self.params_compare = QAction("参数表对比", self)
        self.preview_pdf = QAction("打开PDF", self)

        task_menu.addAction(self.error_check)
        task_menu.addAction(self.doc_compare)
        task_menu.addAction(self.params_compare)
        task_menu.addAction(self.preview_pdf)

        self.doc_compare.triggered.connect(self.show_doc_compare_dialog)
        self.error_check.triggered.connect(self.basic_error_check)
        self.params_compare.triggered.connect(self.param_table_compare)
        self.preview_pdf.triggered.connect(self.open_pdf)

    def init_widget(self):
        self.task_list_panel = QTreeWidget()
        self.task_list_panel.resize(int(WINDOWS_WIDTH * 2 / 12), WINDOWS_HEIGHT)
        self.task_list_panel.setHeaderLabel("任务列表")
        task_item = QTreeWidgetItem(["示例任务"])
        self.task_list_panel.addTopLevelItem(task_item)
        self.task_list_panel.setFont(QFont("Arial", 12))  # 设置字体和大小

        self.basic_error_check_panel = BasicErrorCheckPanel(self)
        self.basic_error_check_panel.resize(int(WINDOWS_WIDTH * 5 / 12), WINDOWS_HEIGHT)

        self.pdf_previewer = PDFPreviewer()
        self.pdf_previewer.resize(int(WINDOWS_WIDTH * 10 / 12), int(WINDOWS_HEIGHT * 3 / 5))
        self.pdf_previewer.setUrl(QUrl("https://www.inovance.com/portal/aboutus"))
        self.table_compare_panel = TableComparePanel()
        self.statcked_widget = QStackedWidget()
        self.statcked_widget.addWidget(self.pdf_previewer)
        self.statcked_widget.addWidget(self.table_compare_panel)

        self.output_panel = OutputWidget()
        self.output_panel.resize(int(WINDOWS_WIDTH * 10 / 12), int(WINDOWS_HEIGHT * 2 / 5))

    def init_layout(self):
        self.main_layout = QVBoxLayout()

        self.splitter1 = QSplitter(Qt.Orientation.Vertical)
        # self.splitter1.addWidget(self.pdf_previewer)
        self.splitter1.addWidget(self.statcked_widget)
        self.splitter1.addWidget(self.output_panel)
        self.splitter1.setStretchFactor(0, 2)  
        self.splitter1.setStretchFactor(1, 1)  

        self.splitter2 = QSplitter(Qt.Orientation.Horizontal)
        self.splitter2.addWidget(self.task_list_panel)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.setStretchFactor(0, 1)  
        self.splitter2.setStretchFactor(1, 1)  

        container = QWidget()
        container.setLayout(self.main_layout)
        self.main_layout.addWidget(self.splitter2)

        self.setCentralWidget(container)

    def init_workers(self):
        self.workers = {}
        self.workers['simulate'] = SimulateProcess()

    def basic_error_check(self):
        print("低错排查功能")
        self.splitter2.addWidget(self.basic_error_check_panel)
        self.splitter2.setStretchFactor(2, 1)

    def param_table_compare(self):
        self.statcked_widget.setCurrentIndex(1)
        print("参数表对比功能待开发，敬请期待")

    def show_doc_compare_dialog(self):
        print("文档对比功能")
        self.statcked_widget.setCurrentIndex(0)
        dialog = CompareDialog(self)
        result = dialog.exec()
    
    def start_progress(self):
        self.gray_overlay = QWidget(self)
        self.gray_overlay.setGeometry(self.rect())
        self.gray_overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);") 
        self.gray_overlay.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.gray_overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.gray_overlay.show()
        
        self.progress_widget = ProgressBar(self)
        self.progress_widget.show()

        self.centralWidget().setEnabled(False)
        self.menuBar().setEnabled(False)
        self.workers['simulate'].setParams(self.progress_widget)
        self.workers['simulate'].start()

    def close_progress(self):
        self.progress_widget.close_signal.emit()
        self.gray_overlay.hide()
        self.centralWidget().setEnabled(True)
        self.menuBar().setEnabled(True)
        self.workers['simulate'].stop()
        self.workers['simulate'].quit()

    def open_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "打开 PDF 文件", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.pdf_previewer.setUrl(QUrl(file_path))
            print(f"打开 PDF 文件: {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    from qt_material import apply_stylesheet
    apply_stylesheet(app, theme='dark_cyan.xml')

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
