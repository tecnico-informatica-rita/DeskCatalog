import flet as ft

from view.home import home_view
from view.informatica import informatica_view
from view.sala import sala_view
from view.audio import audio_view
from view.outros import outros_view
from view.seguranca import seguranca_view
from view.infraestrutura import infraestrutura_view
from view.material import material_view
from view.mobiliario import mobiliario_view


from view.historico_30_dias import Relatorio30DiasView
from view.historico_view import HistoricoView


def gerenciar_rotas(page: ft.Page, conn):

    rotas = {
        "/": home_view,
        "/informatica": informatica_view(conn),
        "/sala": sala_view(conn),
        "/audio": audio_view(conn),
        "/outros": outros_view(conn),
        "/seguranca": seguranca_view(conn),
        "/infraestrutura": infraestrutura_view(conn),
        "/material": material_view(conn),
        "/mobiliario": mobiliario_view(conn),
        
        "/relatorio30": Relatorio30DiasView(conn),
        "/historico": HistoricoView(conn),
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
