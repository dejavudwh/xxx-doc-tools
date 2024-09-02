import sys
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QScrollArea, QWidget


class OutputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.output_text_edit = QTextEdit(self)
        self.output_text_edit.setReadOnly(True)  

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True) 
        self.scroll_area.setWidget(self.output_text_edit)

        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        # sys.stdout = self
        # sys.stderr = self

    def write(self, message):
        scrollbar = self.output_text_edit.verticalScrollBar()
        is_at_bottom = scrollbar.value() == scrollbar.maximum()

        self.output_text_edit.insertPlainText(message) 

        if is_at_bottom:
            self.output_text_edit.ensureCursorVisible()

    def flush(self):
        pass

    def restore_output(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def __del__(self):
        self.restore_output()