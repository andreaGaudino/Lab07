import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.clean()
        self._view.update_page()

        self._mese = int(self._view.dd_mese.value)
        situazioni = Model().get_situazione()


        dizio = {"Torino":[], "Milano":[], "Genova":[]}
        for elem in situazioni:
            if elem.data.month == self._mese:
                dizio[elem.localita].append(elem.umidita)

        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selezionato è:"))
        for citta in dizio:
            somma = 0
            for i in dizio[citta]:
                somma+=i
            media = somma/len(dizio[citta])
            dizio[citta] = media
        for i in dizio:
            self._view.lst_result.controls.append(ft.Text(f"{i}: {round(dizio[i], 3)}"))
        self._view.update_page()






    def handle_sequenza(self, e):
        self._view.lst_result.clean()
        self._view.update_page()

        self._mese = int(self._view.dd_mese.value)
        situazioni = Model().get_situazione()
        def cerca_percorso(dizio):
            if len(dizio) == 15:
                return dizio
            elif len(dizio)==0:
                migliore = None
                for situa in situazioni:
                    if situa.data.month == self._mese:
                        if migliore is None or (situa.data<=migliore.data and situa.umidita<migliore.umidita):
                            migliore = situa
                dizio[migliore.data] = migliore
                return cerca_percorso(dizio)
            else:
                ultima_data = list(dizio.keys())[-1]
                migliore = None
                for situa in situazioni:
                    if situa.data.month == self._mese:
                        if migliore is None or (situa.data>ultima_data and situa.data<=migliore.data and situa.umidita<migliore.umidita):
                            migliore = situa
                dizio[migliore.data] = migliore
                return cerca_percorso(dizio)
        d = cerca_percorso({})
        for i in d:
            self._view.lst_result.controls.append(ft.Text(f"{i}, {d[i]}"))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

