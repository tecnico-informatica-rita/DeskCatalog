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


from src.view.historico_30_dias import Relatorio30DiasView
from src.view.historico_view import HistoricoView


def gerenciar_rotas(page: ft.Page):

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

    def route_change(e):
        # limpa a tela
        page.views.clear()

        # pega a view da rota ou home como padrão
        view_factory = rotas.get(page.route, home_view)

        # cria a view e monta a tela
        view = view_factory()
        view.main(page)

        page.update()

    return route_change
