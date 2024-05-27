"""
Demo of all widgets
"""

from main import reconhecimento_facial, registrar_rosto;
import TKinterModernThemes as TKMT
from functools import partial
import tkinter as tk
import json

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("TKinter Custom Themes Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        # Separator

        self.nextCol()
        self.button_frame = self.addLabelFrame("Buttons")
        self.button_frame.Button("Button", self.handleButtonClick)
        self.button_frame.Button("Button", self.handleButtonClick2)
        self.button_frame.Button("Button", self.handleButtonClick2)

        # Menu for the Menubutton
        # Create a Frame for input widgets

        self.nextCol()
        self.panedWindow = self.PanedWindow("Paned Window Test", rowspan=3)
        self.pane1 = self.panedWindow.addWindow()

        # Define treeview data

        self.debugPrint()
        self.run()

    def handleButtonClick(self):
        registrar_rosto()
       
    def handleButtonClick2(self):
        reconhecimento_facial()
       
    # def handleButtonClick3(self):
    #     fechar()

    def textupdate(self, _var, _indx, _mode):
        print("Current text status:", self.textinputvar.get())

    def menuprint(self, item):
        if self == self:
            pass
        print("Menu item chosen: ", item)

    def validateText(self, text):
        if self == self:
            pass
        if 'q' not in text:
            return True
        print("The letter q is not allowed.")
        return False

if __name__ == '__main__':
    app = App(("park").lower(),("dark").lower())