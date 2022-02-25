from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import os
import openpyxl
import pandas as pd
import shutil


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    open_result = ObjectProperty(None)

class ResultDialog(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        grafico = self.ids.grafico
        grafico.add_widget(Main().resultados())
    #show = ObjectProperty(None)
    cancel2 = ObjectProperty(None)


class Main(FloatLayout):
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup, open_result = self.show_result)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        #self._popup.bind(on_dismiss= self.show_result)
        self._popup.open()


    def load(self, path, filename):
        path_splited = path.split()
        filename2 =''
        for i in path_splited:
            filename2 = filename[0].replace(i, '')


        caminho = rf'{os.path.join(path, filename[0])}'
        destino = r'C:\Users\user\Documents\Bruno\Kivy_Estudos\KivyMD_Plot_2'

        shutil.copy2(caminho,destino)
        filename2 = destino + filename2
        file_oldname = os.path.join(destino, filename2)
        file_newname_newfile = os.path.join(destino, 'Dados.xlsx')

        shutil.move(file_oldname, file_newname_newfile)


    def dismiss_popup2(self):
        self.popup.dismiss()

    def show_result(self):
        content2 = ResultDialog(cancel2=self.dismiss_popup2)
        self.popup = Popup(title="Resultados", content=content2,
                            size_hint=(0.9, 0.9), background='lightgray',title_color=(0,0,0,1) )
        self.popup.open()

    def resultados(self):
        self.df = pd.read_excel('Dados.xlsx')
        data = self.df.to_numpy()
        plot = self.plot(data)
        result = self.Graph(plot)
        return result

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
        f1.set_figheight(2)
        f1.set_figwidth(4)
        return f1

    def Graph(self, fig):
        return FigureCanvasKivyAgg(fig)

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        Builder.load_file('main2.kv')
        return Main()



if __name__ == '__main__':
    MyApp().run()
