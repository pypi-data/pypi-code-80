#!/usr/bin/env python3

# Copyright (C) 2021 Vasco Costa (gluon) <vascomacosta at gmail dot com>
#
# This file is part of glueather.
#
# glueather is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# glueather is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

import json
import pathlib
import sys
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from glueather.ui_mainwindow import Ui_MainWindow
from glueather.weathermanager import WeatherManager, WeatherError

CONF_PATH    = '.glueather.conf'
ICON_PATH    = 'icons/glueather.ico'
WINDOW_TITLE = 'glueather'

class WeatherWorker(QObject):
    finished = pyqtSignal(object)

    def __init__(self, api_key, units, location, current, hourly, daily):
        super().__init__()
        self.api_key = api_key
        self.units = units
        self.location = location
        self.current = current
        self.hourly = hourly
        self.daily = daily

    def run(self):
        result = {}
        try:
            wm = WeatherManager(self.api_key, self.units)
            if self.current:
                current_weather = wm.current(self.location)
                result['current_weather'] = current_weather
            if self.hourly:
                hourly_weather = wm.hourly(self.location)
                result['hourly_weather'] = hourly_weather
            if self.daily:
                daily_weather = wm.daily(self.location)
                result['daily_weather'] = daily_weather
            self.finished.emit(result)
        except WeatherError as e:
            result['error'] = e.message
            self.finished.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.textEdit.setReadOnly(True)
        self.ui.textEdit.zoomIn(2)
        self.ui.lineEdit.returnPressed.connect(self.fetch_weather)
        self.ui.pushButton.clicked.connect(self.fetch_weather)
        self.conf = {'api_key': '0', 'location': 'London', 'units': 'C'}
        self.load_conf()
        self.fetch_weather()

    def load_conf(self):
        try:
            with open(pathlib.Path.home() / CONF_PATH, 'r') as f:
                self.conf = json.load(f)
            self.ui.lineEdit.setText(self.conf['location'])
            if self.conf['units'].lower() in ('f', 'fahrenheit'):
                self.ui.radioButton_2.setChecked(True)
        except FileNotFoundError:
            self.save_conf()
            QMessageBox.warning(self, "Error", "No configuration file found. Creating new one.")
        except Exception:
            QMessageBox.critical(self, "Error", "Problem reading configuration file.")

    def save_conf(self):
        api_key = self.conf['api_key']
        location = self.ui.lineEdit.text() or self.conf['location']
        if self.ui.radioButton.isChecked():
            units = 'C'
        else:
            units = 'F'
        conf = {'api_key': api_key, 'location': location, 'units': units}
        try:
            with open(pathlib.Path.home() / CONF_PATH, 'w') as f:
                json.dump(conf, f, ensure_ascii=False, indent=4)
        except Exception:
            QMessageBox.critical(self, "Error", "Problem writing configuration file.")

    def closeEvent(self, event):
        self.save_conf()
        event.accept()

    def update_weather(self, result):
        self.ui.lineEdit.setEnabled(True)
        self.ui.pushButton.setEnabled(True)
        if 'error' in result.keys():
            QMessageBox.warning(self, "Error", result['error'])
            return
        output = ""
        if 'current_weather' in result.keys():
            output += f"<h1>Current weather at - {result['current_weather']['location']}</h1>" + \
                      f"<hr>" + \
                      f"<table border='1' width='100%' cellpadding='10'>" + \
                      f"<tr><td><b>Conditions</b></td><td>{result['current_weather']['description']}</td></tr>" + \
                      f"<tr><td><b>Temperature</b></td><td>{result['current_weather']['temperature']}</td></tr>" + \
                      f"<tr><td><b>Humidity</b></td><td>{result['current_weather']['humidity']}</td></tr>" + \
                      f"<tr><td><b>Pressure</b></td><td>{result['current_weather']['pressure']}</td></tr>" + \
                      f"<tr><td><b>Wind</b></td><td>{result['current_weather']['wind']}</td></tr>" + \
                      f"</table>"
            self.ui.textEdit.setHtml(output)
        if 'hourly_weather' in result.keys():
            output += f"<h1>Hourly forecast for - {result['hourly_weather'][0]['location']}</h1>" + \
                      f"<hr>" + \
                      f"<table border='1' cellpadding='10' width='100%'>" + \
                      f"<tr><td><b>Time</b></td><td><b>Conditions</b></td><td><b>Temperature</b></td><td><b>Humidity</b></td><td><b>Pressure</b></td><td><b>Wind</b></td></tr>"
            for i, forecast in enumerate(result['hourly_weather'], start=1):
                output += f"<tr><td>{3*i} hours</td>" + \
                          f"<td>{forecast['description']}</td>" + \
                          f"<td>{forecast['temperature']}</td>" + \
                          f"<td>{forecast['humidity']}</td>" + \
                          f"<td>{forecast['pressure']}</td>" + \
                          f"<td>{forecast['wind']}</td></tr>"
            output += f"</table>"
            self.ui.textEdit.setHtml(output)
        if 'daily_weather' in result.keys():
            output += f"<h1>Daily forecast for - {result['daily_weather'][0]['location']}</h1>" + \
                      f"<hr>" + \
                      f"<table border='1' cellpadding='10' width='100%'>" + \
                      f"<tr><td><b>Day</b></td><td><b>Conditions</b></td><td><b>Max</b></td><td><b>Min</b></td><td><b>Humidity</b></td><td><b>Pressure</b><td><b>Wind</b></td></tr>"
            for i, forecast in enumerate(result['daily_weather'], start=1):
                output += f"<tr><td>{forecast['day']}</td>" + \
                          f"<td>{forecast['description']}</td>" + \
                          f"<td>{forecast['max']}</td>" + \
                          f"<td>{forecast['min']}</td>" + \
                          f"<td>{forecast['humidity']}</td>" + \
                          f"<td>{forecast['pressure']}</td>" + \
                          f"<td>{forecast['wind']}</td></tr>"
            self.ui.textEdit.setHtml(output)

    def fetch_weather(self):
        self.ui.lineEdit.setDisabled(True)
        self.ui.pushButton.setDisabled(True)
        output = "Updating..."
        location = self.ui.lineEdit.text()
        if self.ui.radioButton_2.isChecked():
            units = 'f'
        else:
            units = 'c'
        current = hourly = daily = False
        if self.ui.checkBox.isChecked():
            current = True
        if self.ui.checkBox_2.isChecked():
            hourly = True
        if self.ui.checkBox_3.isChecked():
            daily = True
        self.thread = QThread()
        self.worker = WeatherWorker(self.conf['api_key'], units, location, current, hourly, daily)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.update_weather)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle(WINDOW_TITLE)
    window.setWindowIcon(QIcon(ICON_PATH))
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
