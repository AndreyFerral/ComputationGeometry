import sys
import numpy as np
import random as rnd
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui

class Window(QtWidgets.QWidget):
    points = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кубический сплайн")
        self.setFont(QtGui.QFont('Arial', 12))
        max_x, max_y = 500, 400
        self.resize(max_x, max_y)

        # Верхний layout
        self.label_dots = QtWidgets.QLabel("Количество точек")
        self.button_build = QtWidgets.QPushButton("Построить")
        self.slider_dots = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.slider_dots.setRange(5, 25)
        self.slider_dots.setPageStep(5)
        self.slider_dots.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)

        self.up_layout = QtWidgets.QHBoxLayout()
        self.up_layout.addWidget(self.label_dots, stretch=1)
        self.up_layout.addWidget(self.slider_dots, stretch=1)
        self.up_layout.addWidget(self.button_build, stretch=1)

        # layout для отображения графика
        self.graph_widget = pg.PlotWidget()
        self.widget_layout = QtWidgets.QVBoxLayout()
        self.widget_layout.addWidget(self.graph_widget)

        # Нижний layout
        self.label_info = QtWidgets.QLabel()
        self.button_inter = QtWidgets.QPushButton("Интерполяция")
        self.down_layout = QtWidgets.QHBoxLayout()
        self.down_layout.addWidget(self.label_info, stretch=2)
        self.down_layout.addWidget(self.button_inter, stretch=1)

        # Отображение созданных layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.up_layout)
        self.main_layout.addLayout(self.widget_layout)
        self.main_layout.addLayout(self.down_layout)

        # Назначаем функции по нажатию
        self.button_build.clicked.connect(self.build_clicked)
        self.button_inter.clicked.connect(self.inter_clicked)

    def build_clicked(self):
        self.graph_widget.clear()
        self.label_info.clear()
        points_x, points_y = [], []
        # Получаем случайные значения для ломаной линии
        count_points = self.slider_dots.value()
        for i in range(count_points):
            points_x.append(i + 1)
            points_y.append(rnd.randint(0, count_points))
        # Отображаем ломаную линию
        self.graph_widget.plot(points_x, points_y, symbol='x', symbolSize=5)
        Window.points = [points_x, points_y]

    def inter_clicked(self):
        if not Window.points:
            self.label_info.setText("Постройте ломаную линию!")
            return

def main():
    app = QtWidgets.QApplication(sys.argv)  # новый экземпляр QApplication
    window = Window()  # создаём объект класса ExampleApp
    window.show()  # показываем окно
    app.exec_()  # запускаем приложение

# Если файл запущен напрямую
if __name__ == '__main__':
    main()