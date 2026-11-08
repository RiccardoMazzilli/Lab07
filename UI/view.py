import flet as ft
from UI.alert import AlertManager

'''
    VIEW:
    - Rappresenta l'interfaccia utente
    - Riceve i dati dal MODELLO e li presenta senza modificarli
'''

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab07"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # --- Sezione 1: Intestazione ---
        self.txt_titolo = ft.Text(value="Biblioteche di Torino", size=38, weight=ft.FontWeight.BOLD)


        self.dd_biblioteca = ft.Dropdown(
            label="Biblioteca",
            width=400,
            on_select=self.controller.handle_biblioteca_select  # Modificato qui
        )

        self.dd_genere = ft.Dropdown(
            label="Genere",
            width=300,
            on_select=self.controller.handle_genere_select  # Modificato qui
        )

        row_filtri = ft.Row(
            controls=[self.dd_biblioteca, self.dd_genere],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        # --- Sezione 3: Libri ---
        self.btn_mostra = ft.TextButton(
            "Mostra Libri",
            on_click=self.controller.handle_mostra_libri
        )

        self.lv_libri = ft.ListView(expand=True, spacing=10, padding=20)

        # Aggiungo un contenitore per la lista come nel layout
        container_lista = ft.Container(
            content=self.lv_libri,
            expand=True,
            padding=10
        )

        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            ft.Row([self.toggle_cambia_tema], alignment=ft.MainAxisAlignment.CENTER),

            # Sezione 1
            self.txt_titolo,
            ft.Divider(),

            # Sezione 2: Filtraggio
            row_filtri,

            # Pulsante indipendente al centro
            ft.Row([self.btn_mostra], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),

            # Sezione 3: Lista Libri
            container_lista
        )

        self.page.scroll = "adaptive"

        # Chiama il controller per popolare i dropdown con i dati del database
        # subito dopo aver montato l'interfaccia.
        if self.controller:
            self.controller.popola_dropdowns()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()