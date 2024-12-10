import os

class Utils:
    @staticmethod
    def ajustar_caminho_windows(caminho):
        if os.name == 'nt':  # Verifica se está no Windows
            caminho_ajustado = caminho.replace(":", "").replace("\\", "/")
            return f"/cygdrive/{caminho_ajustado}"
        return caminho

    @staticmethod
    def ajustar_caminho_origem(caminho):
        if not caminho.endswith('/'):
            caminho += '/'
        return caminho

    @staticmethod
    def log_message(log_file_path, message):
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"{message}\n")
