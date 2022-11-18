from PyQt5 import QtWidgets, QtCore, QtGui
import shapely.geometry as shap
import random as rnd
import sys

class Window(QtWidgets.QWidget):
    path = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Многоугольник алгоритмом Грэхема")
        self.setFont(QtGui.QFont('Arial', 12))
        self.resize(500, 300) 

        # Верхний layout
        self.label_dots = QtWidgets.QLabel("Количество точек")
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.slider.setRange(3, 103)
        self.slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
        self.build = QtWidgets.QPushButton("Построить")
        self.up_layout = QtWidgets.QHBoxLayout()
        self.up_layout.addWidget(self.label_dots, stretch=3)
        self.up_layout.addWidget(self.slider, stretch=3)
        self.up_layout.addWidget(self.build, stretch=3)

        # layout для рисования
        self.print = QtWidgets.QLabel()
        self.canvas = QtGui.QPixmap(self.size())
        self.canvas.fill(QtGui.QColor("white"))
        self.print.setPixmap(self.canvas)
        self.canvas_layout = QtWidgets.QVBoxLayout()
        self.canvas_layout.addWidget(self.print)

        # Нижний layout
        self.dot = QtWidgets.QPushButton("Вхождение")
        self.label_result = QtWidgets.QLabel("Результат:")
        self.down_layout = QtWidgets.QHBoxLayout()
        self.down_layout.addWidget(self.label_result, stretch=6)
        self.down_layout.addWidget(self.dot, stretch=3)

        # Отображение созданных layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.up_layout)
        self.main_layout.addLayout(self.canvas_layout)
        self.main_layout.addLayout(self.down_layout)

        # Назначаем функцию по нажатию
        self.build.clicked.connect(self.build_clicked)
        self.dot.clicked.connect(self.dot_entry_clicked)

    # Обработка кнопки для рисования многоугольника
    def build_clicked(self): 
        # Очищаем canvas от лишнего
        self.canvas.fill(QtGui.QColor("white"))
        self.print.setPixmap(self.canvas)
        self.label_result.setText("Результат:")
        # Вызываем функцию рисования многоугольника
        count = self.slider.value()
        self.graham_scan(count)

    # Обработки кнопки определения вхождения точки
    def dot_entry_clicked(self): 
        path = Window.path
        if not path:
            self.label_result.setText("Результат: Необходим многоугольник!")
            return
        # Очищаем canvas от лишнего
        self.canvas.fill(QtGui.QColor("white"))
        self.print.setPixmap(self.canvas)
        self.horizontal_beam(path)

    def get_limit_coords(self):
        min_xy = 10
        max_x = self.print.size().width() - 10
        max_y = self.print.size().height() - 10
        return min_xy, max_x, max_y

    def horizontal_beam(self, path):
        # Настраиваем ручку для рисования
        painter = QtGui.QPainter(self.print.pixmap())
        painter.setPen(get_pen(2, 'black'))

        # Рисуем многоугольник
        polygon = list_to_poly(path)
        painter.drawPolygon(polygon)

        # Определяем ограничения для координат
        min_xy, max_x, max_y = self.get_limit_coords()
        x = rnd.randint(min_xy, max_x)
        y = rnd.randint(min_xy, max_y)

        # Определяем количество пересечений 
        horizontal_line = shap.LineString([[x, y], [max_x, y]])
        count_intersection = 0
        for i in range(len(polygon)):
            # Определяем линию для проверки пересечения
            if i != len(polygon)-1:
                polygon_line = shap.LineString([path[i], path[i+1]])
            else:
                polygon_line = shap.LineString([path[i], path[0]])
            # Если есть пересечении между линиями
            if horizontal_line.intersects(polygon_line): 
                count_intersection += 1
                         
        # Рисуем сгенерированную точку
        if count_intersection%2 == 0: 
            painter.setPen(get_pen(4, 'red'))
            self.label_result.setText("Результат: Точка НЕ входит в многоугольник!")
        else:
            painter.setPen(get_pen(4, 'green'))
            self.label_result.setText("Результат: Точка входит в многоугольник!")
        painter.drawPoint(x, y)

        self.update()
        painter.end()

    def graham_scan(self, count):
        # Настраиваем ручку для рисования
        painter = QtGui.QPainter(self.print.pixmap())
        painter.setPen(get_pen(2, 'black'))
        # Определяем ограничения для координат
        min_xy, max_x, max_y = self.get_limit_coords()

        # Получаем список случайных точек
        points = []
        for i in range(count):
            x = rnd.randint(min_xy, max_x)
            y = rnd.randint(min_xy, max_y)
            point = [x, y]
            painter.drawPoint(x, y)
            points.append(point)

        # Определяем самую левую точку
        for i in range(1, count):
            if points[i][0] < points[0][0]:
                points[0], points[i] = points[i], points[0]

        # Сортируем список по степени левизны
        while True:
            is_sort = False
            for i in range(2, count):
                if rotate(points[0], points[i-1], points[i])>0:
                    points[i-1], points[i] = points[i], points[i-1]
                    is_sort = True
            if not is_sort: break

        # Определяем последовательность точек многоугольника
        path = [points[0], points[1]]
        for i in range(2, count):
            while rotate(path[-2], path[-1], points[i])>0:
                path.pop(-1)
            path.append(points[i])

        Window.path = path
        # Преобразуем список в QPolygon
        polygon = list_to_poly(path)
        # Рисуем многоугольник
        painter.drawPolygon(polygon)
        self.update()
        painter.end()

def list_to_poly(path):
    polygon = QtGui.QPolygon()
    for i in range(len(path)):
        point = QtCore.QPoint(path[i][0], path[i][1])
        polygon.append(point)
    return polygon

def get_pen(size, color):
    pen = QtGui.QPen()
    pen.setWidth(size)
    pen.setColor(QtGui.QColor(color))
    return pen

def rotate(A, B, C):
    return (B[0]-A[0])*(C[1]-B[1])-(B[1]-A[1])*(C[0]-B[0])

def main():
    app = QtWidgets.QApplication(sys.argv)  # новый экземпляр QApplication
    window = Window()  # создаём объект класса ExampleApp
    window.show()  # показываем окно
    app.exec_()  # запускаем приложение

# Если файл запущен напрямую
if __name__ == '__main__':
    main()