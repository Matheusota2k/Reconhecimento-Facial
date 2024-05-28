from main import reconhecimento_facial, registrar_rosto;
import TKinterModernThemes as TKMT
from functools import partial
import tkinter as tk
import json


class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("TKinter Custom Themes Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)
        

        self.nextCol()
        self.button_frame = self.addLabelFrame("Painel")
        self.button_frame.Button("Registrar Rosto", self.handleButtonClick)
        self.button_frame.Button("Ativar Reconhecimento", self.handleButtonClick2)
        
        self.nextCol()
        self.panedWindow = self.PanedWindow("Paned Window Test", rowspan=3)
        self.pane1 = self.panedWindow.addWindow()

        self.debugPrint()
        self.run()

    def handleButtonClick(self):
        registrar_rosto()
       
    def handleButtonClick2(self):
        reconhecimento_facial()

if __name__ == '__main__':
    app = App(("park").lower(),("dark").lower())