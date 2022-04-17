from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog,
                             QApplication, QCheckBox, QApplication, QHBoxLayout, QWidget,QMessageBox)

from PyQt5.QtCore import QUrl
import pandas as pd
from GU import Ui_MainWindow
import numpy as np
import os
import plotly
import plotly.express as px
import plotly.graph_objects as go
import moviepy.editor as mp
from PIL import Image
from io import BytesIO
from os import path


class Covid(Ui_MainWindow):
    def __init__(self,mainwindow):
        super(Covid,self).setupUi(mainwindow)
        self.cases.clicked.connect(self.cases_show)
        self.deaths.clicked.connect(self.deaths_show )
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'map.html' ))
        local_url = QUrl.fromLocalFile(file_path)
        self.plot_1.load(local_url)
        self.plot_1.show()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'scatter.html' ))
        local_url = QUrl.fromLocalFile(file_path)
        self.plot_2.load(local_url)
        self.plot_2.show()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'diff.html' ))
        local_url = QUrl.fromLocalFile(file_path)
        self.plot_4.load(local_url)
        self.plot_4.show()
        self.cases_show()
        self.data1 = pd.read_csv("covid-19.csv")
        self.actionMap.triggered.connect(self.prepareMap)
        self.actionScatter.triggered.connect(self.prepareBubble)
        self.actionCases.triggered.connect(self.prepareBarCases)
        self.actionDeaths.triggered.connect(self.prepareBarDeaths)

    def cases_show(self):
        self.plot_3.close()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'bar_cases.html' ))
        local_url = QUrl.fromLocalFile(file_path)
        self.plot_3.load(local_url)
        self.plot_3.show()
    def deaths_show(self):
        self.plot_3.close()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'bar_deaths.html' ))
        local_url = QUrl.fromLocalFile(file_path)
        self.plot_3.load(local_url)
        self.plot_3.show()

    def popup(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Please Wait")
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()
    def prepareMap(self):
        # filename = QtWidgets.QFileDialog.getSaveFileName("","open", "", "Track(*.wav)")
        # print(filename)
        self.popup("It might take 5 minutes or more ")
        df = px.data.gapminder().query("year==2007")
        fig = px.choropleth(self.data1, locations="Country", animation_frame="Date", animation_group="Country",
                                 locationmode='country names',
                                 hover_name="Country", color="Confirmed", color_continuous_scale="Sunset",
                                 range_color=[0, 150000])
        self.prepareImgs(fig, "map.gif")
    def prepareBubble(self):
        self.popup("It might take 5 minutes or more ")
        df = px.data.gapminder()
        fig = px.scatter(self.data1, x="Deaths", y="Recovered", animation_frame="Date", animation_group="Country",
                         size="Confirmed",size_max=70, log_x=True, range_y=[-25000, 285000], range_x=[1, 150000])

        self.prepareImgs(fig,"Bubble.gif")
    def prepareBarCases(self):
        self.popup("It might take 5 minutes or more ")
        df = px.data.gapminder()
        fig = px.bar(self.data1, x="Country", y="Confirmed", animation_frame="Date", color="Country",
                         animation_group="Country")
        fig.update_layout(xaxis={'categoryorder': 'total ascending'})

        self.prepareImgs(fig,"Barcases.gif")

    def prepareBarDeaths(self):
        self.popup("It might take 5 minutes or more ")
        df = px.data.gapminder()
        fig = px.bar(self.data1, x="Country", y="Deaths", animation_frame="Date", color="Country",
                     animation_group="Country")
        fig.update_layout(xaxis={'categoryorder': 'total ascending'})

        self.prepareImgs(fig, "Bardeaths.gif")

    def prepareImgs(self, figure, name):
        listOfImgs = []
        for frame in figure.frames:
            fig1 = go.Figure(frame.data, figure.layout)
            img_bytes = fig1.to_image(format="png")
            stream = BytesIO(img_bytes)
            image = Image.open(stream).convert("RGBA")
            stream.close()
            listOfImgs.append(image)
        listOfImgs[0].save(name, save_all=True, append_images=listOfImgs[1:],
                                     optimize=True, duration=100,loop=1)
        if path.exists(name):
            clip = mp.VideoFileClip(name)
            clip.write_videofile("video.mp4")
            os.remove(name)


if __name__ == "__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Covid(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())