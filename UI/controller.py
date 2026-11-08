import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

    def popola_dropdowns(self):
        """ Popola i controlli Dropdown della View richiedendo i dati al Model. """
        # Recupero i dati
        biblioteche = self._model.get_biblioteche()
        generi = self._model.get_generi()

        # 1. Ricostruisco la lista biblioteche da zero
        opz_biblio = [ft.dropdown.Option(key="None", text="Nessun filtro")]
        for b in biblioteche:
            opz_biblio.append(ft.dropdown.Option(key=str(b.id), text=b.nome))

        # 2. Ricostruisco la lista generi da zero
        opz_generi = [ft.dropdown.Option(key="None", text="Nessun filtro")]
        for g in generi:
            opz_generi.append(ft.dropdown.Option(key=g, text=g))

        # Assegno le liste complete ai Dropdown
        self._view.dd_biblioteca.options = opz_biblio
        self._view.dd_genere.options = opz_generi

        # Aggiorno l'interfaccia
        self._view.update()

    def handle_biblioteca_select(self, e):
        """ Callback quando viene selezionata una biblioteca """
        val = e.control.value
        if val == "None" or val is None:
            self.biblioteca_selezionata = None
        else:
            self.biblioteca_selezionata = int(val)

    def handle_genere_select(self, e):
        """ Callback quando viene selezionato un genere """
        val = e.control.value
        if val == "None" or val is None:
            self.genere_selezionato = None
        else:
            self.genere_selezionato = val

    def handle_mostra_libri(self, e):
        """ Azione scatenata dal pulsante 'Mostra Libri' """
        # Recupero i libri filtrati dal model
        libri = self._model.get_libri_filtrati(self.biblioteca_selezionata, self.genere_selezionato)

        # Pulisco la ListView attuale prima di riempirla
        self._view.lv_libri.controls.clear()

        # Gestisco il caso in cui non ci siano risultati
        if not libri:
            self._view.show_alert("Nessun libro trovato con questi filtri!")
        else:
            # Utilizzo il metodo __str__ del DTO Libro per la visualizzazione formattata
            for libro in libri:
                self._view.lv_libri.controls.append(ft.Text(str(libro)))

        self._view.update()