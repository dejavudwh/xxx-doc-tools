from PyQt6.QtWidgets import (QDialog, QFileDialog, QVBoxLayout, QLineEdit, QMessageBox,
                             QPushButton, QHBoxLayout, QFormLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QUrl

from services.PDFDiff import DiffPDFWorker
from utils import utils

class CompareDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("创建任务")
        self.setFixedSize(500, 150)  # 设置对话框的固定大小

        self.file1_edit = QLineEdit()
        self.file1_edit.setPlaceholderText("对比文件1: 未选择")
        self.file1_edit.setReadOnly(True)  # 设置为只读
        self.file1_edit.setFixedWidth(350)  # 设置文本框的固定宽度
        self.file1_edit.setStyleSheet("background-color: black; color: white;")  # 设置文本框背景为黑色，字体为白色
        
        self.file2_edit = QLineEdit()
        self.file2_edit.setPlaceholderText("对比文件2: 未选择")
        self.file2_edit.setReadOnly(True)  # 设置为只读
        self.file2_edit.setFixedWidth(350)  # 设置文本框的固定宽度
        self.file2_edit.setStyleSheet("background-color: black; color: white;")  # 设置文本框背景为黑色，字体为白色

        self.select_file1_button = QPushButton("打开")
        self.select_file2_button = QPushButton("打开")

        self.ok_button = QPushButton("确定")
        self.ok_button.setFixedSize(80, 30)  # 设置 “确定” 按钮的大小
        self.ok_button.setStyleSheet("font-weight: bold;")  # 设置 “确定” 按钮的字体加粗

        self.select_file1_button.clicked.connect(self.select_file1)
        self.select_file2_button.clicked.connect(self.select_file2)
        self.ok_button.clicked.connect(self.submit_diff)  # 关闭对话框并返回结果

        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(10)  # 增加水平控件之间的间距

        file1_layout = QHBoxLayout()
        file1_layout.addWidget(self.file1_edit)
        file1_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))  # 添加空白
        file1_layout.addWidget(self.select_file1_button)
        file1_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 将文本框和按钮布局在左侧

        file2_layout = QHBoxLayout()
        file2_layout.addWidget(self.file2_edit)
        file2_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))  # 添加空白
        file2_layout.addWidget(self.select_file2_button)
        file2_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 将文本框和按钮布局在左侧

        form_layout.addRow(file1_layout)
        form_layout.addRow(file2_layout)

        button_layout = QHBoxLayout()
        button_layout.addStretch() 
        button_layout.addWidget(self.ok_button)
        button_layout.addStretch()  

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.worker = DiffPDFWorker()
        self.worker.finished.connect(self.on_diff_finish)

    def on_diff_finish(self):
        self.worker.quit()
        self.accept()
        self.parent.close_progress()
        self.parent.pdf_previewer.setUrl(QUrl("file:///./diff.pdf")) 

    def select_file1(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择对比文件1")

        if file_name:
            self.file1_edit.setText(file_name)
            print(f"选择了对比文件1: {file_name}")

    def select_file2(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择对比文件2")
    
        if file_name:
            self.file2_edit.setText(file_name)
            print(f"选择了对比文件2: {file_name}")

    def submit_diff(self):
        file1 = self.file1_edit.text()
        file2 = self.file2_edit.text()
        if not utils.is_file_of_format(file1, 'pdf') or not utils.is_file_of_format(file2, 'pdf'):
            QMessageBox.critical(self, "Error", "文件不存在或文件格式错误", QMessageBox.StandardButton.Ok)
            return
        
        self.worker.setParams(file1.encode('utf-8'), file2.encode('utf-8'))
        self.worker.start()
        self.parent.start_progress()
        self.setWindowOpacity(0)