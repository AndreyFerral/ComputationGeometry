import sys
import sympy as sp
import random as rnd
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui

class Window(QtWidgets.QWidget):
    points = []
    symbols = ['a', 'b', 'c', 'd']

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
        points = [1, 2, 4, 7], [2, 3, 1, 4]
        diff1, diff2 = [], []
        S1, S2 = [], []

        for i in range(len(points[0])-1):
            S = f'a{i}+b{i}*(x-x0)+c{i}*(x-x0)**2+d{i}*((x-x0)**3)'
            S = S.replace('x0', f'{points[0][i]}')
            diff1.append(sp.diff(S, 'x'))
            diff2.append(sp.diff(diff1[-1], 'x'))

            tempS1 = S.replace('x', f'{points[0][i]}')
            tempS2 = S.replace('x', f'{points[0][i+1]}')
            S1.append(sp.simplify(tempS1) - points[1][i])
            S2.append(sp.simplify(tempS2) - points[1][i+1])
            #print(S, S1[i], S2[i])

        eq1, eq2 = [], []   
        for i in range(len(diff1)-1):
            f1 = diff1[i] - 1 * diff1[i+1]
            f2 = diff2[i] - 1 * diff2[i+1]
            f1 = str(f1).replace('x', str(points[0][i+1]))
            f2 = str(f2).replace('x', str(points[0][i+1]))
            eq1.append(sp.simplify(f1))
            eq2.append(sp.simplify(f2))
            #print('eq', eq1[i], eq2[i])

        last1 = str(diff2[0]).replace('x', str(points[0][0]))
        last2 = str(diff2[-1]).replace('x', str(points[0][-1]))
        last1 = sp.simplify(last1)
        last2 = sp.simplify(last2)
        #print('last', last1, last2)

        print(S1, 'XXX', S2)
        print(eq1, 'XXX', eq2)
        print(last1, 'XXX', last2)



def main():
    app = QtWidgets.QApplication(sys.argv)  # новый экземпляр QApplication
    window = Window()  # создаём объект класса ExampleApp
    window.show()  # показываем окно
    app.exec_()  # запускаем приложение

# Если файл запущен напрямую
if __name__ == '__main__':
    main()