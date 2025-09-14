from PyQt5.QtWidgets import QMainWindow, QTabWidget, QLineEdit, QToolBar, QAction, QMenu, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from vpn import simular_roteamento
from udp_streaming import baixar_video_udp
from favoritos import salvar_favorito, salvar_historico
from downloads import GerenciadorDownloads
from adblocker import AdBlocker
from fechar_aba import fechar_aba

VPN_ATIVADA = False

class Navegador(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Navegador Profissional")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(lambda index: fechar_aba(self.tabs, index))
        self.setCentralWidget(self.tabs)
        self.url_input = QLineEdit()
        self.downloads = GerenciadorDownloads()
        self.adblocker = AdBlocker()

        # Barra de ferramentas
        barra = QToolBar()
        barra.addWidget(self.url_input)
        self.addToolBar(barra)

        # Ações da barra
        acoes = [
            ("Nova Aba", lambda: self.nova_aba("https://google.com")),
            ("◀ Voltar", self.voltar),
            ("▶ Avançar", self.avancar),
            ("⟳ Atualizar", self.atualizar_aba),
            ("🚫 AdBlock", self.toggle_adblock)
        ]
        for nome, func in acoes:
            action = QAction(nome, self)
            action.triggered.connect(func)
            barra.addAction(action)

        self.btn_vpn = QAction("🔒 VPN", self)
        self.btn_vpn.setCheckable(True)
        self.btn_vpn.triggered.connect(self.toggle_vpn)
        barra.addAction(self.btn_vpn)

        # Atalho Ctrl+W para fechar aba
        atalho_fechar = QShortcut(QKeySequence("Ctrl+W"), self)
        atalho_fechar.activated.connect(lambda: fechar_aba(self.tabs))

        # Abre a primeira aba
        self.nova_aba("https://google.com")

    def toggle_vpn(self, checked):
        global VPN_ATIVADA
        VPN_ATIVADA = checked
        print(f"VPN {'ativada' if VPN_ATIVADA else 'desativada'}")

    def toggle_adblock(self):
        self.adblocker.toggle(not self.adblocker.ativo)

    def nova_aba(self, url):
        nav = QWebEngineView()
        nav.load(QUrl(url))
        index = self.tabs.addTab(nav, "Carregando...")
        self.tabs.setCurrentIndex(index)
        nav.urlChanged.connect(lambda: self.url_input.setText(nav.url().toString()))
        nav.titleChanged.connect(lambda title: self.tabs.setTabText(index, title[:30]))
        nav.page().profile().downloadRequested.connect(self.downloads.handle_download)
        nav.setContextMenuPolicy(Qt.CustomContextMenu)
        nav.customContextMenuRequested.connect(lambda pos: self.menu_contexto(pos, nav))

    def carregar_url(self):
        url = self.url_input.text().strip()
        if not url: return

        salvar_historico(url)

        if VPN_ATIVADA:
            html = simular_roteamento(url)
            aba = self.tabs.currentWidget()
            aba.setHtml(html, baseUrl=QUrl(url))
            return

        if self.adblocker.bloquear_url(url):
            print(f"🚫 URL bloqueada: {url}")
            return

        if "youtube" in url:
            arquivo = baixar_video_udp(url)
            print(f"🎬 Vídeo pronto: {arquivo}")

        if not url.startswith("http"):
            url = "https://" + url
        aba = self.tabs.currentWidget()
        aba.load(QUrl(url))

    def menu_contexto(self, pos, aba):
        menu = QMenu()
        menu.addAction("⭐ Adicionar Favorito", lambda: salvar_favorito(aba.url().toString()))
        menu.addAction("Abrir em nova aba", lambda: self.nova_aba(aba.url().toString()))
        menu.addAction("Copiar URL", lambda: QApplication.clipboard().setText(aba.url().toString()))
        menu.exec_(aba.mapToGlobal(pos))

    def voltar(self):
        aba = self.tabs.currentWidget()
        aba.back()

    def avancar(self):
        aba = self.tabs.currentWidget()
        aba.forward()

    def atualizar_aba(self):
        aba = self.tabs.currentWidget()
        aba.reload()
