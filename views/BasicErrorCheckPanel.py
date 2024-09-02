import os
from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QDialog, QLabel, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTreeWidgetItem, QTreeWidget, QFileDialog, QMessageBox
)
from PyQt6.QtCore import QUrl

from utils import utils
from services import PDFBasicErrorCheck

class BasicErrorCheckPanel(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.match_cond_number = 0
        self.target_file = ''
        self.target_output_path = ''

        main_layout = QVBoxLayout()

        self.submit_button = QPushButton("提交低错排查任务")
        self.submit_button.clicked.connect(self.submit_check)

        self.match_list = QTreeWidget()
        self.match_list.setHeaderLabel("匹配条件选择")

        bottom_layout = QHBoxLayout()
        self.delete_item_button = QPushButton("删除匹配")
        self.add_item_button = QPushButton("添加匹配")
        self.import_item_button = QPushButton("导入匹配")

        bottom_layout.addWidget(self.add_item_button)
        bottom_layout.addWidget(self.delete_item_button)
        bottom_layout.addWidget(self.import_item_button)

        self.add_item_button.clicked.connect(self.add_item)
        self.delete_item_button.clicked.connect(self.delete_item)
        self.import_item_button.clicked.connect(self.import_item)

        main_layout.addWidget(self.submit_button)
        main_layout.addWidget(self.match_list)
        main_layout.addLayout(bottom_layout)

        main_layout.setStretch(0, 1) 
        main_layout.setStretch(1, 9)  
        main_layout.setStretch(1, 1)  
        self.setLayout(main_layout)

    def add_item(self):
        dialog = AddItemDialog(self)
        dialog.exec()
    
    def delete_item(self):
        item = self.match_list.currentItem()
        if item is not None:
            parent_item = item.parent()
            print(parent_item)
            if parent_item:
                index = parent_item.indexOfChild(item)
                parent_item.takeChild(index)
            else:
                index = self.match_list.indexOfTopLevelItem(item)
                self.match_list.takeTopLevelItem(index)

    def import_item(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择要导入的Excel文件")

        if not utils.is_file_of_format(file_name, 'xlsx'):
            QMessageBox.critical(self, "Error", "文件不存在或文件格式错误", QMessageBox.StandardButton.Ok)
            return

        if file_name:
            print(f"Selected file: {file_name}")
            result = PDFBasicErrorCheck.import_item_from_excel(file_name)
            for match_cond, annot in result:
                root_item = QTreeWidgetItem(["匹配条件{}".format(self.match_cond_number)])
                self.match_cond_number = self.match_cond_number + 1
                QTreeWidgetItem(root_item, ["匹配：{}".format(match_cond)])
                QTreeWidgetItem(root_item, ["批注：{}".format(annot)])
                self.match_list.addTopLevelItem(root_item)

    def submit_check(self):
        dialog = SubmitDialog(self)
        result = dialog.exec()
        keywords_and_annot = {}
        if result == QDialog.DialogCode.Accepted:
            for i in range(self.match_list.topLevelItemCount()):
                item = self.match_list.topLevelItem(i)
                keywords_and_annot[item.child(0).text(0).split('：', 1)[1]] = item.child(1).text(0).split('：', 1)[1]
            PDFBasicErrorCheck.basic_error_check(self.target_file, self.target_output_path + "/ued-doc-tool(已批注).pdf", keywords_and_annot)
            self.parent.pdf_previewer.setUrl(QUrl("file:///{}".format(self.target_output_path + "/ued-doc-tool(已批注).pdf")))
        elif result == QDialog.DialogCode.Rejected:
            print("Dialog closed by reject()")

class SubmitDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("提交低错排查任务")
        self.setFixedSize(500, 150)  

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        self.target_file_edit = QLineEdit("选择目标手册")
        self.target_file_edit.setStyleSheet("background-color: black; color: white;") 
        self.select_tartget_file_button = QPushButton("打开")
        self.select_tartget_file_button.clicked.connect(self.select_target_file)
        top_layout.addWidget(self.target_file_edit)
        top_layout.addWidget(self.select_tartget_file_button)

        self.output_dir_edit = QLineEdit("选择输出目录")
        self.output_dir_edit.setStyleSheet("background-color: black; color: white;") 
        self.select_output_dir_button = QPushButton("设置")
        self.select_output_dir_button.clicked.connect(self.select_output_dir)
        bottom_layout.addWidget(self.output_dir_edit)
        bottom_layout.addWidget(self.select_output_dir_button)

        self.button_ok = QPushButton("确定")
        self.button_ok.clicked.connect(self.submit)  # 点击确定按钮时，接受对话框
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.addWidget(self.button_ok)

        self.setLayout(main_layout)

    def select_target_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择目标手册")

        if not utils.is_file_of_format(file_name, 'pdf'):
            QMessageBox.critical(self, "Error", "文件不存在或文件格式错误", QMessageBox.StandardButton.Ok)
            return

        if file_name:
            self.target_file_edit.setText(file_name)
            self.parent.target_file = file_name
            print(f"Selected file: {file_name}")

    def select_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "选择输出目录", os.getcwd())
        if directory:
            self.output_dir_edit.setText(directory)
            self.parent.target_output_path = directory
            print(f"Selected directory: {directory}")

    def submit(self):
        self.accept()

class AddItemDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("添加匹配条件和批注")
        self.setFixedSize(500, 150)  

        main_layout = QVBoxLayout()

        match_cond_layout = QHBoxLayout()
        anno_layout = QHBoxLayout()

        self.label_match = QLabel("匹配条件:")
        self.line_edit_match = QLineEdit()
        self.line_edit_match.setStyleSheet("background-color: black; color: white;") 
        match_cond_layout.addWidget(self.label_match)
        match_cond_layout.addWidget(self.line_edit_match)

        self.label_comment = QLabel("添加批注:")
        self.line_edit_comment = QLineEdit()
        self.line_edit_comment.setStyleSheet("background-color: black; color: white;") 
        anno_layout.addWidget(self.label_comment)
        anno_layout.addWidget(self.line_edit_comment)

        self.button_ok = QPushButton("确定")
        self.button_ok.clicked.connect(self.add_item)  # 点击确定按钮时，接受对话框
        main_layout.addLayout(match_cond_layout)
        main_layout.addLayout(anno_layout)
        main_layout.addWidget(self.button_ok)

        self.setLayout(main_layout)

    def add_item(self):
        root_item = QTreeWidgetItem(["匹配条件{}".format(self.parent.match_cond_number)])
        self.parent.match_cond_number = self.parent.match_cond_number + 1
        QTreeWidgetItem(root_item, ["匹配：{}".format(self.line_edit_match.text())])
        QTreeWidgetItem(root_item, ["批注：{}".format(self.line_edit_comment.text())])
        self.parent.match_list.addTopLevelItem(root_item)
        self.accept()