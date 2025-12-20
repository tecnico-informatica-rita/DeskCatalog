import flet as ft

from src.view.home import home_view

from src.view.informatica import informatica_view
from src.view.sala import sala_view
from src.view.audio import audio_view
from src.view.outros import outros_view
from src.view.seguranca import seguranca_view
from src.view.infraestrutura import infraestrutura_view
from src.view.material import material_view
from src.view.mobiliario import mobiliario_view
#historico e relatorio 
from src.view.historico_30_dias import Relatorio30DiasView
from src.view.historico_view import HistoricoView
#IMPORTANTE DEFINIR AS PAGINAS COMO NAO MAIN PARA FUNCIOINAR E NAO SOBRESCREVER UMA AS OUTRAS



def gerenciar_rotas(page: ft.Page):
    # dict que define as rotas
    rotas = {
        "/": home_view,
        "/informatica": informatica_view,
        "/sala": sala_view,
        "/audio": audio_view,
        "/outros": outros_view,
        "/seguranca": seguranca_view,
        "/infraestrutura": infraestrutura_view,
        "/material": material_view,
        "/mobiliario": mobiliario_view,
        
        "/historico30": Relatorio30DiasView,
        "/historico": HistoricoView,
    }

    # Esta função limpa a tela e carrega a nova visualização
    def route_change(e):
        page.views.clear()

        view_factory = rotas.get(page.route, home_view)

        # Adiciona a nova View à lista de views da página
        page.views.append(view_factory(page))
        page.update()

    return route_change


