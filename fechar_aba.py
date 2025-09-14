# fechar_aba.py
from PyQt5.QtWidgets import QTabWidget, QApplication

def fechar_aba(tabs: QTabWidget, index: int = None):
    """
    Fecha a aba especificada ou a aba atual se nenhum índice for fornecido.
    Se for a última aba, fecha o navegador inteiro.
    :param tabs: O QTabWidget do navegador.
    :param index: Índice da aba a ser fechada (opcional).
    """
    if tabs.count() == 0:
        QApplication.quit()  # Nenhuma aba, encerra o app
        return

    if index is None:
        index = tabs.currentIndex()

    if 0 <= index < tabs.count():
        if tabs.count() == 1:
            print("⚠ Última aba fechada → encerrando o navegador")
            QApplication.quit()
            return
        tabs.removeTab(index)
        print(f"🗑 Aba {index} fechada")
    else:
        print(f"⚠ Índice inválido: {index}")