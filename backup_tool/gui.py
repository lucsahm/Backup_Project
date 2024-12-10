import os
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Toplevel, Text, Scrollbar, Label, RIGHT, Y, END
from datetime import datetime
from .utils import Utils
from .rsync import Rsync
from .config import Config
import sys

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Backup de Fotos")
        self.rsync_path = Config.load_config()
        self.rsync = Rsync(self.rsync_path)

        # Verifica rsync
        try:
            self.rsync.verificar_rsync()
        except FileNotFoundError:
            messagebox.showerror("Erro", "Rsync não encontrado!")
            root.quit()

        # Campos e botões
        self.entry_origem = tk.Entry(root, width=50)
        self.entry_origem.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Selecionar Origem", command=self.selecionar_origem).grid(row=0, column=2, padx=10, pady=5)

        self.entry_destino = tk.Entry(root, width=50)
        self.entry_destino.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Selecionar Destino", command=self.selecionar_destino).grid(row=1, column=2, padx=10, pady=5)

        tk.Button(root, text="Inverter Origem e Destino", command=self.inverter_diretorios).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(root, text="Iniciar Backup", command=self.faz_backup).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(root, text="Sincronizar", command=self.sincroniza).grid(row=3, column=1, padx=10, pady=10)

        # Criação do menu "Ajuda"
        menu_bar = Menu(root)
        root.config(menu=menu_bar)

        menu_ajuda = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Ajuda", command=self.mostrar_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)

    # Função para exibir o conteúdo do README.md
    def mostrar_ajuda(self, event=None):
        # Determina o caminho para o README.md, considerando o modo de execução (script ou executável)
        if getattr(sys, 'frozen', False):  # Verifica se o código está rodando como executável
            base_dir = sys._MEIPASS  # Diretório temporário onde o PyInstaller extrai os arquivos
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do arquivo atual

        readme_path = os.path.join(base_dir, 'README.md')  # Caminho completo para README.md

        try:
            # Abre o arquivo README.md
            with open(readme_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
        except FileNotFoundError:
            conteudo = "Arquivo README.md não encontrado."

        # Cria uma janela para exibir o conteúdo do README
        janela_ajuda = Toplevel(self.root)
        janela_ajuda.title("Ajuda - README.md")

        text_area = Text(janela_ajuda, wrap='word')
        text_area.insert(END, conteudo)
        text_area.config(state='disabled')  # Impede que o texto seja editado

        scrollbar = Scrollbar(janela_ajuda, command=text_area.yview)
        text_area['yscrollcommand'] = scrollbar.set

        # Adiciona os componentes na janela
        text_area.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

    # Função para exibir informações de contato e versão
    def mostrar_sobre(self, event=None):
        sobre_texto = (
            "Nome: Lucas Sahm\n"
            "Email: lucassahm@gmail.com\n"
            "Data: 10/12/2024\n"
            "Versão: 2.0.0"
        )

        janela_sobre = Toplevel(self.root)
        janela_sobre.title("Sobre")

        label_sobre = Label(janela_sobre, text=sobre_texto, padx=10, pady=10)
        label_sobre.pack()

    def selecionar_origem(self):
        origem = filedialog.askdirectory()
        if origem:
            self.entry_origem.delete(0, tk.END)
            self.entry_origem.insert(0, origem)

    def selecionar_destino(self):
        destino = filedialog.askdirectory()
        if destino:
            self.entry_destino.delete(0, tk.END)
            self.entry_destino.insert(0, destino)

    def inverter_diretorios(self):
        origem = self.entry_origem.get()
        destino = self.entry_destino.get()
        self.entry_origem.delete(0, tk.END)
        self.entry_destino.delete(0, tk.END)
        self.entry_origem.insert(0, destino)
        self.entry_destino.insert(0, origem)

    def faz_backup(self):
        origem = Utils.ajustar_caminho_windows(self.entry_origem.get())
        destino = Utils.ajustar_caminho_windows(self.entry_destino.get())
        origem = Utils.ajustar_caminho_origem(origem)
        log_file_path = f"{self.entry_origem.get()}/backup.log"
        self.rsync.executar_comando(origem, destino, ['-ahvz', '--progress'], log_file_path)

    def sincroniza(self):
        origem = Utils.ajustar_caminho_windows(self.entry_origem.get())
        destino = Utils.ajustar_caminho_windows(self.entry_destino.get())
        origem = Utils.ajustar_caminho_origem(origem)
        log_file_path = f"{self.entry_origem.get()}/backup.log"
        self.rsync.executar_comando(origem, destino, ['-ahvz', '--delete', '--progress'], log_file_path)
