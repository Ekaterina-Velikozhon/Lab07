from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_umidita_media(mese):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
            return res
        else:
            cursor = cnx.cursor()
            query = """SELECT s.Localita, AVG(s.Umidita)
                        FROM situazione s 
                        WHERE MONTH(s.Data) = %s
                        GROUP BY s.Localita"""
            cursor.execute(query, (mese,))
            res = cursor.fetchall()
            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def get_situazioni(mese):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
            return res
        else:
            cursor  = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        WHERE MONTH(s.Data) = %s AND DAY(s.Data) <= 15
                        ORDER BY s.Data ASC"""
            cursor.execute(query, (mese,))

            for row in cursor:
                res.append(Situazione(row["Localita"],
                                      row["Data"],
                                      row["Umidita"]))
            cursor.close()
            cnx.close()
        return res


