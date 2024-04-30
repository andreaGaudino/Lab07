import random

import flet as ft

import model.model
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
        def cerca_percorso(dizio, citta_iniziale):

            '''elif len(dizio)==0:
                migliore = None
                for situa in situazioni:
                    if situa.data.month == self._mese:
                        if migliore is None or (situa.data<=migliore.data and situa.umidita<migliore.umidita):
                            migliore = situa
                dizio[migliore.data] = (migliore, 1)
                for situa in situazioni:
                    if situa.data.month == self._mese:
                        if situa.localita == migliore.localita and (situa.data-list(dizio.keys())[-1]).days == 1 and list(dizio.values())[-1][1] <=3 :
                            dizio[situa.data] = (situa, list(dizio.values())[-1][1]+1)
                return cerca_percorso(dizio)
            else:
                ultima_data = list(dizio.keys())[-1]
                migliore = None
                for situa in situazioni:
                    if situa.data.month == self._mese and situa.data>ultima_data:
                        if migliore is None or (situa.data>ultima_data and situa.data<=migliore.data and situa.umidita<migliore.umidita):
                            numero = 0
                            for situazione in dizio:
                                if situazione.localita == situa.localita:
                                    numero = dizio[situazione][1]
                            if numero < 6:
                                migliore = (situa, numero)
                            else:
                                return cerca_percorso(dizio)

                dizio[migliore.data] = migliore
                print(len(dizio))
                return cerca_percorso(dizio)'''
            new_situazioni = {}
            for situa in situazioni:
                if situa.data.month == self._mese:
                    if situa.data in list(new_situazioni.keys()):
                        new_situazioni[situa.data].append(situa)
                    else:
                        new_situazioni[situa.data] = [situa]
            ultima = None
            ultima_data = None
            if len(dizio) >= 15:
                return dizio
            elif len(dizio) == 0:
                citta = None
                for i in list(new_situazioni.values())[0]:
                    if i.localita == citta_iniziale:
                        citta = i
                if citta is not None:
                    dizio[citta.data] = (citta, 1)
                    for j in range(1,3):
                        for i in list(new_situazioni.values())[j]:
                            if i.localita==citta.localita and ((i.data-citta.data).days==1 or (i.data-citta.data).days==2):
                                dizio[i.data] = (i, list(dizio.values())[-1][1]+1)
                #print(dizio)
                else:
                    altre_localita = []
                    for i in list(new_situazioni.values())[0]:
                        altre_localita.append(i)
                    citta = random.choice(altre_localita)
                    dizio[citta.data] = (citta, 1)
                    for j in range(1, 3):
                        for i in list(new_situazioni.values())[j]:
                            if i.localita == citta.localita and (
                                    (i.data - citta.data).days == 1 or (i.data - citta.data).days == 2):
                                dizio[i.data] = (i, list(dizio.values())[-1][1] + 1)
                return cerca_percorso(dizio, citta_iniziale)
            else:
                ultima = list(dizio.values())[-1]
                ultima_data = ultima[0].data
                migliore = None
                if ultima[1] < 6 and len(dizio)<3:
                    for data in new_situazioni:
                        if (ultima_data-data).days==1:
                            for i in new_situazioni[data]:
                                if i.localita == ultima[0].localita:
                                    dizio[i.data] = (i, ultima[1]+1)
                    #print(dizio)
                    return cerca_percorso(dizio, citta_iniziale)
                elif ultima[1]<6 and len(dizio)>=3:
                    ultime_3 = [list(dizio.values())[-1][0].localita, list(dizio.values())[-2][0].localita,list(dizio.values())[-3][0].localita]
                    if ultime_3[0] == ultime_3[1] and ultime_3[1] == ultime_3[2]:
                        for data in new_situazioni:
                            if (ultima_data-data).days==-1:
                                for i in new_situazioni[data]:
                                    if migliore is None or (i.umidita<migliore.umidita):
                                        migliore = i
                                count = 0
                                for j in list(dizio.values()):
                                    if j[0].localita == migliore.localita:
                                        count += 1
                                dizio[migliore.data] = (migliore, count+1)
                    else:
                        for data in new_situazioni:
                            if (ultima_data-data).days==-1:
                                for i in new_situazioni[data]:
                                    if i.localita == ultima[0].localita:
                                        dizio[i.data] = (i, ultima[1]+1)
                    #print(dizio)
                    return cerca_percorso(dizio, citta_iniziale)
                else:
                    da_evitare = ultima[0].localita
                    for data in new_situazioni:
                        if (ultima_data - data).days == -1:
                            for i in new_situazioni[data]:
                                if i.localita != da_evitare:
                                    if migliore is None or (i.umidita < migliore.umidita):
                                        migliore = i
                            count = 0
                            for j in list(dizio.values()):
                                if j[0].localita == migliore.localita:
                                    count += 1
                            dizio[migliore.data] = (migliore, count + 1)
                    return cerca_percorso(dizio, citta_iniziale)





        costo_minimo = float('inf')
        citta_migliore = ""
        for citta in ["Torino", "Milano", "Genova"]:
            costo = 0
            count = 0
            prec = None
            d = cerca_percorso({}, citta)
            for i in d:
                costo += d[i][0].umidita
                count += 1
                if count > 1 and prec.localita != d[i][0].localita:
                    costo += 100
                    prec = d[i][0]
                if count == 1 :
                    prec = d[i][0]
            if costo < costo_minimo:
                costo_minimo = costo
                citta_migliore = citta

        risultato = cerca_percorso({}, citta_migliore)
        self._view.lst_result.controls.append(ft.Text(f"Il percorso con costo minimo ha costo: {costo_minimo}"))
        for i in risultato:
            self._view.lst_result.controls.append(ft.Text(f"[{risultato[i][0].localita} - {risultato[i][0].data}] Umidità = {risultato[i][0].umidita}"))
        self._view.update_page()


    def read_mese(self, e):
        self._mese = int(e.control.value)


    def handle_sequenza_2(self, e):
        if self._mese == 0:
            self._view.create_alert("mese non valido riprova")
            return
        sequenza, costo = self._model.calcola_sequenza(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Il costo della sequenza è {costo}"))
        for fermata in sequenza:
            self._view.lst_result.controls.append(ft.Text(fermata))
        self._view.update_page()

