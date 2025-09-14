from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem

class GerenciadorDownloads:
    def __init__(self):
        self.lista_downloads = []

    def handle_download(self, item: QWebEngineDownloadItem):
        item.accept()
        self.lista_downloads.append((item.url().toString(), item.path()))
        print(f"⬇️ Download iniciado: {item.url().toString()} → {item.path()}")