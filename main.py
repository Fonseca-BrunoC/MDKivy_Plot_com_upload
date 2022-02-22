from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import os
import openpyxl
import pandas


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Main(FloatLayout):
    loadfile = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        df = pandas.read_excel(os.path.join(path, filename[0]))
        data = df.to_numpy()
        plot = self.plot(data)
        graph = self.Graph(plot)
        return graph

    def plot(self, data):
        t = data[:, 0]
        Cexp = data[:, 1:4]
        Cx = Cexp[:, 0]
        Cs = Cexp[:, 1]
        Cp = Cexp[:, 2]

        f1 = plt.figure()
        ax1 = f1.add_subplot(111)
        plt.rc('axes', titlesize=15)
        plt.rc('axes', labelsize=10)
        l1 = ax1.plot(t, Cx, color='r', label='Cx')
        l2 = ax1.plot(t, Cs, color='b', label='Cs')
        l3 = ax1.plot(t, Cp, color='g', label='Cp')
        ax1.set_title("Dados Experimentais", weight='bold')
        ax1.set_xlabel('t (h)', weight='bold')
        ax1.set_ylabel('g/L', weight='bold')
        plt.rc('legend', fontsize=13)
        ax1.legend()
        ax1.grid(True)
        f1.set_figheight(4)
        f1.set_figwidth(6)
        return f1

    def Graph(self, fig):
        graph = self.ids.graph
        graph.add_widget(FigureCanvasKivyAgg(fig))

Factory.register('Load', cls=Main)

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        Builder.load_file('main.kv')
        self.sera = Factory.Main()
        return self.sera



if __name__ == '__main__':
    MyApp().run()