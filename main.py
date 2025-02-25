import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
import io
from PyQt6 import uic

f = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="map">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>571</width>
      <height>541</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QLineEdit" name="coord1">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>10</y>
      <width>131</width>
      <height>20</height>
     </rect>
    </property>
    <property name="placeholderText">
     <string>Долгота</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="coord2">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>40</y>
      <width>131</width>
      <height>20</height>
     </rect>
    </property>
    <property name="placeholderText">
     <string>Широта</string>
    </property>
   </widget>
   <widget class="QPushButton" name="search_button">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>130</y>
      <width>201</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>Искать</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>730</x>
      <y>10</y>
      <width>61</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>Долгота</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>730</x>
      <y>40</y>
      <width>51</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>Широта</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="spn">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>70</y>
      <width>131</width>
      <height>20</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="placeholderText">
     <string>Долгота</string>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>726</x>
      <y>70</y>
      <width>61</width>
      <height>51</height>
     </rect>
    </property>
    <property name="text">
     <string>Масштаб</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="spn_2">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>100</y>
      <width>131</width>
      <height>20</height>
     </rect>
    </property>
    <property name="placeholderText">
     <string>Широта</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(io.StringIO(f), self)
        self.initUI()
        self.z = 15

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={self.c1},{self.c2}&spn={self.spn1},{self.spn2}'
        # Готовим запрос.

        map_request = f"{server_address}{ll_spn}&z={self.z}&apikey={api_key}"
        print(map_request)
        response = requests.get(map_request)

        if not response:
            raise Exception

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setWindowTitle('Yandex Maps')

        self.search_button.clicked.connect(self.search)

    def keyPressEvent(self, event2):
        if event2.key() == 16777238 and self.z < 21:
            self.spn1 += 1
            self.spn2 += 1
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.map.setPixmap(self.pixmap)
        if event2.key() == 16777239 and self.z > 0:
            self.spn1 -= 1
            self.spn2 -= 1
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.map.setPixmap(self.pixmap)

    def search(self):
        try:
            self.c1 = float(self.coord1.text())
            self.c2 = float(self.coord2.text())
            self.spn1 = float(self.spn.text())
            self.spn2 = float(self.spn_2.text())
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.map.setPixmap(self.pixmap)
        except Exception:
            print("Неверный формат данных/данной точки не существует")

    def closeEvent(self, event):
        os.remove(self.map_file)

#kk
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())