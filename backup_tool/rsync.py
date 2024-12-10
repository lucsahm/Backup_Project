import subprocess
from datetime import datetime
from tkinter import messagebox

class Rsync:
    def __init__(self, rsync_path):
        self.rsync_path = rsync_path

    def verificar_rsync(self):
        try:
            result = subprocess.run([self.rsync_path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print("rsync está instalado:", result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("rsync não encontrado. Certifique-se de que está instalado.")
            raise FileNotFoundError("rsync não encontrado no caminho especificado.")

    def executar_comando(self, origem, destino, parametros, log_file_path):
        try:
            comando = [self.rsync_path] + parametros + [origem, destino]
            result = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            with open(log_file_path, 'a') as log_file:
                log_file.write(result.stdout)
            messagebox.showinfo("Sucesso", "Operação concluída com sucesso!")
        except subprocess.CalledProcessError as e:
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"Erro: {e.stderr}")
            messagebox.showerror("Erro", "Erro durante a operação.")
