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
   <widget class="QDoubleSpinBox" name="coord1">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>10</y>
      <width>131</width>
      <height>22</height>
     </rect>
    </property>
    <property name="decimals">
     <number>6</number>
    </property>
    <property name="minimum">
     <double>-180.000000000000000</double>
    </property>
    <property name="maximum">
     <double>180.000000000000000</double>
    </property>
    <property name="singleStep">
     <double>0.500000000000000</double>
    </property>
   </widget>
   <widget class="QDoubleSpinBox" name="coord2">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>40</y>
      <width>131</width>
      <height>22</height>
     </rect>
    </property>
    <property name="decimals">
     <number>6</number>
    </property>
    <property name="minimum">
     <double>-180.000000000000000</double>
    </property>
    <property name="maximum">
     <double>180.000000000000000</double>
    </property>
    <property name="singleStep">
     <double>0.500000000000000</double>
    </property>
   </widget>
   <widget class="QDoubleSpinBox" name="spn">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>70</y>
      <width>131</width>
      <height>22</height>
     </rect>
    </property>
    <property name="decimals">
     <number>6</number>
    </property>
    <property name="minimum">
     <double>-180.000000000000000</double>
    </property>
    <property name="maximum">
     <double>180.000000000000000</double>
    </property>
    <property name="singleStep">
     <double>0.500000000000000</double>
    </property>
   </widget>
   <widget class="QDoubleSpinBox" name="spn_2">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>100</y>
      <width>131</width>
      <height>22</height>
     </rect>
    </property>
    <property name="decimals">
     <number>6</number>
    </property>
    <property name="minimum">
     <double>-180.000000000000000</double>
    </property>
    <property name="maximum">
     <double>180.000000000000000</double>
    </property>
    <property name="singleStep">
     <double>0.500000000000000</double>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="settings">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>21</height>
    </rect>
   </property>
   <widget class="QMenu" name="menu">
    <property name="title">
     <string>Настройки</string>
    </property>
    <widget class="QMenu" name="menu_2">
     <property name="title">
      <string>Тема</string>
     </property>
     <addaction name="light"/>
     <addaction name="dark"/>
    </widget>
    <addaction name="menu_2"/>
   </widget>
   <addaction name="menu"/>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
  <action name="light">
   <property name="text">
    <string>Светлая</string>
   </property>
  </action>
  <action name="dark">
   <property name="text">
    <string>Тёмная</string>
   </property>
  </action>
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
        self.theme = 'light'

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={self.c1},{self.c2}&spn={self.s1},{self.s2}'

        map_request = f"{server_address}{ll_spn}&theme={self.theme}&apikey={api_key}"
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
        self.light.triggered.connect(self.light_theme)
        self.dark.triggered.connect(self.dark_theme)

    def search(self):
        try:
            self.c1 = self.coord1.value()
            self.c2 = self.coord2.value()
            self.s1 = self.spn.value()
            self.s2 = self.spn_2.value()
            self.getImage()
            self.display()
        except Exception as e:
            print(e.__class__.__name__)

    def light_theme(self):
        self.theme = 'light'
        self.getImage()
        self.display()

    def dark_theme(self):
        self.theme = 'dark'
        self.getImage()
        self.display()

    def display(self):
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
