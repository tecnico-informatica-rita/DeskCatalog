import flet as ft
from view.home_modular.home_redesenhada import HomeView
from view.cadastro import cadastro_view
from view.emprestimo import emprestimo_view
from view.devolucao import devolucao_view
from view.imprimir_relatório import Relatorio30DiasView
from view.audio import audio_view
from view.informatica import informatica_view
from view.infraestrutura import infraestrutura_view
from view.outros import outros_view
from view.sala import sala_view
from view.mobiliario import mobiliario_view
from view.material import material_view
from view.seguranca import seguranca_view


# rotas.py
'''def gerenciar_rotas(page: ft.Page, conn):

    rotas = {
        "/": lambda: page.add(HomeView(conn).main_home(page)),
        "/cadastro": lambda: page.add(cadastro_view(conn).main_cadastro(page)),
        "/emprestimo": lambda: page.add(emprestimo_view(conn).main_emprestimo(page)),
        "/devolucao": lambda: page.add(devolucao_view(conn).main_devolucao(page)),
    }

    def route_change(e):
        # Limpa só o conteúdo da página, mantendo AppBar e Drawer
        page.controls.clear()

        # Chama a função da rota
        view_factory = rotas.get(page.route, lambda: HomeView(conn).build(page))
        view_factory()

        page.update()

    return route_change'''

def gerenciar_rotas(page: ft.Page, conn):
    rotas = {
        "/": lambda: HomeView(conn).main_home(page),
        "/cadastro": lambda: cadastro_view(conn).main_cadastro(page),
        "/emprestimo": lambda: emprestimo_view(conn).main_emprestimo(page),
        "/devolucao": lambda: devolucao_view(conn).main_devolucao(page),
        "/imprimir_relatório": lambda: Relatorio30DiasView(conn).main(page),

        # categorias
        "/audio": lambda: audio_view(conn).main(page),
        "/informatica": lambda: informatica_view(conn).main(page),
        "/infraestrutura": lambda: infraestrutura_view(conn).main(page),
        "/outros": lambda: outros_view(conn).main(page),
        "/sala": lambda: sala_view(conn).main(page),
        "/seguranca": lambda: seguranca_view(conn).main(page),
        "/material": lambda: material_view(conn).main(page),
        "/mobiliario": lambda: mobiliario_view(conn).main(page),
    }

    def route_change(e):
        page.controls.clear()  # limpa o conteúdo antigo
        view_factory = rotas.get(page.route, lambda: HomeView(conn).build_layout(page))
        layout = view_factory()  # pega o layout retornado
        print("Layout:", layout, type(layout))
        if layout is None:
            raise ValueError(f"A rota '{page.route}' retornou None")

        page.add(layout)         # adiciona à página
        page.update()

    return route_change


