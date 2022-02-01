import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [900, 450]
MAP_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.lon = "37.530887"
        self.lat = "55.703118"
        self.l = "map"
        self.delta = "0.002"
        self.size_map = "600,450"
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        param = {
            "ll": ",".join([self.lon, self.lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": self.l,
            "size": self.size_map
        }
        response = requests.get(map_request, params=param)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setFixedSize(*SCREEN_SIZE)
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('<MAPS.API>')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        pix = self.pixmap.scaled(*MAP_SIZE)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*MAP_SIZE)
        self.image.setPixmap(pix)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())