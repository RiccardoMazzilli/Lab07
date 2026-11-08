
from database.DB_connect import DBConnect
from model.biblioteca_DTO import Biblioteca

"""
    Biblioteca DAO
    Gestisce le operazioni di accesso al database relative alle biblioteche (Effettua le Query).
"""

class BibliotecaDAO:
    def __init__(self):
        pass

    @classmethod
    def get_all_biblioteche(cls) -> list[Biblioteca]:
        # Recupera tutte le biblioteche dal database
        # Restituisce una lista di oggetti di Biblioteca

        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Errore: impossibile connettersi al database")
            return []
        result = []
        cursor = cnx.cursor(dictionary=True, buffered=True)
        query = "SELECT * FROM biblioteca ORDER BY nome"

        try:
            cursor.execute(query)
            for row in cursor():
                result.append(Biblioteca(row["id"], row["nome"], row["indirizzo"]))
        except Exception as e:
            print(f"Errore durante la query get_all_biblioteche: {e}")
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

        return result