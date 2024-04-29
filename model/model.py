import copy

from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        #self.situazione = MeteoDao()
        self._costo_minimo = -1
        self._sequenza_ottima = []



    def get_situazione(self):
        return MeteoDao().get_all_situazioni()

    def calcola_sequenza(self, mese):
        situazioni_meta_mese = MeteoDao.get_situazioni_meta_mese(mese)


        self.ricorsione([], situazioni_meta_mese)

    def ricorsione(self, parziale, situazioni):

        #caso terminale
        if len(parziale) == 15:
            #calcola costo
            costo = self.calcola_costo(parziale)
            if self._costo_minimo == -1 or costo < self._costo_minimo:
                self._costo_minimo = costo
                self._sequenza_ottima = copy.deepcopy(parziale)
            print(parziale)

        else:
            day = len(parziale)+1
            for situazione in situazioni[(day-1)*3:day*3]:

                if self.vincoli_soddisfatti(parziale, situazione):
                    parziale.append(situazione)
                    self.ricorsione(parziale, situazioni)
                    parziale.pop()

    def vincoli_soddisfatti(self, parziale, situazione)->bool:
        #check che non sono gia stato 6 giorni nella citta
        counter=0
        for fermata in parziale:
            if fermata.localita == situazione.localita:
                counter+=1

        if counter>=6:
            return False

        #check che il tecnico si fermi almeno 3 giorni consecutivi
        if len(parziale) <= 2 and len(parziale)>0:
            if situazione.localita!= parziale[0].localita:
                return False

        elif len(parziale)>2:
            sequenza_finale = parziale[-3:] #ultimi 3 giorni in parziale
            prima_fermata = sequenza_finale[0].localita
            counter = 0
            for fermata in sequenza_finale:
                if fermata.localita == prima_fermata:
                    counter += 1
            if (counter < 3) and situazione.localita != prima_fermata:
                return False

        # ho soddisfato tutti i vincoli
        return True
    def calcola_costo(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            costo += parziale[i].umidita
            if i == 2:
                if parziale[i].localita != parziale[0].localita:
                    costo += 100
            else:
                ultima_fermate = parziale[i-2:i+1]
                if ultima_fermate[2].localita != ultima_fermate[0].localita or ultima_fermate[2].localita != ultima_fermate[1].localita:
                    costo += 100
        return costo