import os
import subprocess
import sys
from os.path import expanduser
from PyQt5.QtWidgets import *
from borb.pdf import Document, Page, Paragraph, PDF, SingleColumnLayout, FixedColumnWidthTable, TrueTypeFont
from borb.io.read.types import Decimal
from pathlib import Path

classes_dict = {0: 'cigarette', 1: 'helmet', 2: 'person'}


def results(run_args):
    result = subprocess.run(run_args, capture_output=True, text=True)
    folder_str = result.stderr.split()[-1]
    return folder_str[:folder_str.rfind('/')]


class DialogApp(QWidget):
    def __init__(self):
        super().__init__()
        self.run_args = ['python', '/Users/dudi/PycharmProjects/IllegalActions/yolov5/detect.py', '--weights',
                         '/Users/dudi/PycharmProjects/IllegalActions/yolov5/runs/train/exp1/best-2.pt', '--source',
                         'validation_set',
                         '--save-txt', '--project', 'currently_detected']
        self.resize(600, 400)
        self.folder_choose_btn = QPushButton('Select File')
        self.folder_choose_btn.clicked.connect(self.select_file)
        self.predict_btn = QPushButton('Predict')
        self.predict_btn.clicked.connect(self.predict)
        self.input_dir = ''
        self.results_dir = ''
        self.fines_count = 0
        self.total_fines = {}
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(['Image', 'Type of fine'])
        self.export_results_btn = QPushButton('Export Results')
        self.export_results_btn.clicked.connect(self.export)
        layout = QVBoxLayout()
        layout.addWidget(self.folder_choose_btn)
        layout.addWidget(self.predict_btn)
        layout.addWidget(self.table)
        layout.addWidget(self.export_results_btn)
        self.setLayout(layout)

    def select_file(self):
        self.input_dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', expanduser("~"))
        self.run_args[5] = self.input_dir

    def predict(self):
        self.results_dir = results(self.run_args)
        for i in os.listdir(f'{self.results_dir}/labels'):
            image_fines = []
            with open(f'{self.results_dir}/labels/{i}') as f:
                classes = [classes_dict[int(j.split()[0])] for j in f.readlines()]
                if 'person' in classes and 'cigarette' in classes:
                    self.fines_count += 1
                    image_fines.append('Fine for smoking')
                if 'person' in classes and 'helmet' not in classes:
                    self.fines_count += 1
                    image_fines.append('Fine for safety')
            self.total_fines[i] = image_fines
        self.table.setRowCount(self.fines_count)
        row_count = 0
        for i in self.total_fines.keys():
            for j, _ in enumerate(self.total_fines[i]):
                self.table.setItem(row_count, 0, QTableWidgetItem(i))
                self.table.setItem(row_count, 1, QTableWidgetItem(self.total_fines[i][j]))
                row_count += 1

    def export(self):
        monserrat = TrueTypeFont.true_type_font_from_file(Path('Montserrat/Montserrat-VariableFont_wght.ttf'))
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(Paragraph('Результаты обработки данных', font=monserrat, font_size=Decimal(30)))
        table_output = FixedColumnWidthTable(number_of_columns=2, number_of_rows=self.fines_count)
        for i in self.total_fines.keys():
            for j, _ in enumerate(self.total_fines[i]):
                table_output.add(Paragraph(f'{i[:str(i).rfind(".")]}'))
                table_output.add(Paragraph(f'{self.total_fines[i][j]}'))
        layout.add(table_output)
        with open(f'{self.input_dir}/report.pdf', 'wb') as f:
            PDF.dumps(f, pdf)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DialogApp()
    demo.show()
    sys.exit(app.exec_())
