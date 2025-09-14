class AdBlocker:
    def __init__(self):
        self.ativo = False
        self.filtro = ["ads.", "doubleclick.net", "adservice.google.com"]

    def toggle(self, ativado=True):
        self.ativo = ativado
        print(f"🚫 Bloqueador de anúncios {'ativado' if self.ativo else 'desativado'}")

    def bloquear_url(self, url):
        if not self.ativo:
            return False
        return any(ad in url for ad in self.filtros)