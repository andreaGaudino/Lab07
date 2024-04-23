from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        self.situazione = MeteoDao()


    def get_situazione(self):
        return MeteoDao().get_all_situazioni()

