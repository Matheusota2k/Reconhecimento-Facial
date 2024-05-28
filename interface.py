from main import reconhecimento_facial, capturar_rosto, cursor
import tkinter as tk
from tkinter import Toplevel
from tkinter.ttk import PanedWindow
import cv2
import TKinterModernThemes as TKMT

# Definição da classe principal da aplicação
class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("TKinter Custom Themes Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)
        
       
        self.create_widgets()
        self.debugPrint()
        self.run()

    def create_widgets(self):
        self.create_buttons()
        self.create_paned_window()
        
    def create_buttons(self):
        button_frame = self.addLabelFrame("Painel")
        button_frame.Button("Registrar Rosto", self.open_register_window)
        button_frame.Button("Ativar Reconhecimento", self.handle_recognition_button_click)

    def create_paned_window(self):
        self.paned_window = self.PanedWindow("Paned Window Test", rowspan=3)
        self.paned_window.addWindow()

    def open_register_window(self):
        register_window = Toplevel(self.master)
        RegisterApp(register_window)

    def handle_recognition_button_click(self):
        reconhecimento_facial()

class RegisterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Registrar Rosto")

        # Criação dos widgets da janela de registro
        self.create_widgets()

    # Método para criar os widgets da janela de registro
    def create_widgets(self):
        entry_frame = tk.LabelFrame(self.master, text="Registre seu Rosto")
        entry_frame.pack(padx=20, pady=20)

        self.name_label = tk.Label(entry_frame, text="Nome:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)

        self.name_entry = tk.Entry(entry_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.register_button = tk.Button(entry_frame, text="Registrar", command=self.handle_registration)
        self.register_button.grid(row=1, columnspan=2, padx=10, pady=5)

    # Método para lidar com o registro
    def handle_registration(self):
        nome = self.name_entry.get().strip()
        if nome:
            self.register_face(nome)
            self.master.destroy()
        else:
            print("Erro: Nome não pode estar vazio!")

    # Método para registrar um rosto
    def register_face(self, nome):
        # Obtém o próximo ID para o rosto
        novo_id = cursor.execute('SELECT MAX(face_id) FROM faces').fetchone()[0] + 1
        capturar_rosto(nome, novo_id)

if __name__ == '__main__':
    app = App(("park").lower(), ("dark").lower())
