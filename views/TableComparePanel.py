from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QTextBrowser, QDialog, QHeaderView, QFileDialog, QScrollArea, QSizePolicy, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QPushButton
from services.PDFTableCompare import comapre_pdf_table
import difflib

class TextBrowserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(500, 200)
        self.text_browser = QTextBrowser(self)
        layout = QVBoxLayout()
        layout.addWidget(self.text_browser)
        self.setLayout(layout)

    def set_text(self, text):
        self.text_browser.setText(text)

class TableComparePanel(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()

        select_layout = QHBoxLayout()
        self.target_file = QLineEdit()
        self.select_target_file = QPushButton("上传手册")
        self.select_target_file.clicked.connect(self.upload_file)
        self.excel_file = QLineEdit()
        self.select_excel_file = QPushButton("上传参数表")
        self.select_excel_file.clicked.connect(self.upload_excel)
        select_layout.addWidget(self.target_file)
        select_layout.addWidget(self.select_target_file)
        select_layout.addWidget(self.excel_file)
        select_layout.addWidget(self.select_excel_file)

        self.tables_widget = QWidget()
        self.tables_layout = QVBoxLayout(self.tables_widget)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.tables_widget)

        submit_layout = QHBoxLayout()
        self.submit_page = QLineEdit()
        self.submit_button = QPushButton("对比此页")   
        self.submit_button.clicked.connect(self.submit_compare)
        # self.show_diff_button = QPushButton("显示详细对比")   
        # self.show_diff_button.clicked.connect(self.show_diff)
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.submit_page.setSizePolicy(size_policy)
        self.submit_button.setSizePolicy(size_policy)  
        submit_layout.addStretch(1)
        submit_layout.addWidget(self.submit_page, 0)
        submit_layout.addWidget(self.submit_button, 0)
        submit_layout.addStretch(1)

        self.layout.addLayout(select_layout, 0)
        self.layout.addWidget(self.scroll_area, 9)
        self.layout.addLayout(submit_layout, 0)

        self.setLayout(self.layout)
    
    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择目标手册")
        if file_name:
            self.target_file.setText(file_name)
            print(f"选择了目标文件: {file_name}")

    def upload_excel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择参数表")
        if file_name:
            self.excel_file.setText(file_name)
            print(f"选择了参数表: {file_name}")

    def submit_compare(self):
        page_number = int(self.submit_page.text())
        result = comapre_pdf_table(self.target_file.text(), self.excel_file.text(), page_number)
        for i in range(0, len(result), 3):
            data = [result[i], result[i + 1], result[i + 2]]
            headers = ["参数", "参数名称", "默认值", "设定范围", "参数说明"]
            self.add_table(data, headers)

    def cell_clicked(self, row, column):
        table = self.sender()
        column_data = []
        for i in range(table.rowCount() - 1):
            item = table.item(i, column)
            if item: 
                column_data.append(item.text())
        html_diff = difflib.HtmlDiff().make_file(column_data[0].splitlines(), column_data[1].splitlines(), fromdesc='Text 1', todesc='Text 2')
        dialog = TextBrowserDialog()
        dialog.set_text(html_diff)
        dialog.exec()

    def add_table(self, data, headers):
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        for row, rowData in enumerate(data):
            for column, item in enumerate(rowData):
                table.setItem(row, column, QTableWidgetItem(str(item)))

        table.cellClicked.connect(self.cell_clicked)

        table.setMinimumSize(600, 200)
        table.setAlternatingRowColors(True)

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table.setSizePolicy(size_policy)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.tables_layout.addWidget(table)