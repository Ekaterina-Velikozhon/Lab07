import copy

from database.meteo_dao import MeteoDao
from model.situazione import Situazione


class Model:
    def __init__(self):
        self._sequenza_ottima = []
        self._costo_minimo = -1

    def get_umidita_media(self, mese):
        return MeteoDao.get_umidita_media(mese)

    def get_situazioni(self, mese):
        return MeteoDao.get_situazioni(mese)

    def get_sequenza_ottima(self, mese):
        self.__sequenza_ottima = []
        self._costo_minimo = -1
        self._ricorsione([], self.get_situazioni(mese))
        return self._sequenza_ottima, self._costo_minimo

    def _ricorsione(self, parziale, situazioni):
        #caso terminale:
        if len(parziale) == 15:
            print(parziale)
            costo = self._calcola_costo_percorso(parziale)
            if (self._costo_minimo == -1) or (costo < self._costo_minimo):
                self._costo_minimo = costo
                self._sequenza_ottima = copy.deepcopy(parziale)
        else:
            day = len(parziale)+1
            for situazione in situazioni[(day-1)*3:day*3]: #in base a miei vincoli in 3 giorni
                #if situazione.data.day == day:
                if self._verifica_ammissibilita(parziale, situazione):
                    parziale.append(situazione)
                    self._ricorsione(parziale, situazioni)
                    parziale.pop()

    def _calcola_costo_percorso(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            # 1) costo dell'umidita
            costo += parziale[i].umidita

            if i == 2:  # il terzo giorno
                if (parziale[i].localita != parziale[0].localita):
                    costo += 100
            elif i > 2:  # altri giorni
                ultime_fermate = parziale[i - 2:i + 1] #guardo due situazioni precedenti, пересмотреть
                if (ultime_fermate[2].localita != ultime_fermate[0].localita
                        or ultime_fermate[2].localita != ultime_fermate[1].localita):
                    costo += 100
        return costo


    def _verifica_ammissibilita(self, parziale, situazione):
        # Vincolo 1) check che non sono stato gia 6 giorni nella citta
        counter = 0
        for fermata in parziale:
            if fermata.localita == situazione.localita:
                counter += 1
        if counter >= 6:
            return False

        # Vincolo 2) check che  il tecnicno si fermi almeno tre giorni consecutivi
        if len(parziale) <= 2 and len(parziale) > 0:
            if situazione.localita != parziale[0].localita:
                return False
        # se la mia parziale ha almeno 3 elementi, devo controllare gli ultimi 3
        # e vedere se il tecnico si è fermato almeno tre giorni di fila nello stesso posto
        elif len(parziale) > 2:
            sequenza_finale = parziale[-3:]  # prendo gli ultimi 3 giorni in parziale, ovvero invero parziale per comodita'
            prima_fermata = sequenza_finale[0].localita  # < primo di questi ultimi tre giorni
            counter = 0
            for fermata in sequenza_finale:
                if fermata.localita == prima_fermata:
                    counter += 1
            if (counter < 3) and situazione.localita != sequenza_finale[-1].localita: #controllo situazione.localita che voglio aggiungere
                return False
        return True