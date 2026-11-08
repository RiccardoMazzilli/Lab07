from database.DB_connect import DBConnect
from model.biblioteca_DTO import Biblioteca

"""
    Biblioteca DAO
    Gestisce le operazioni di accesso al database relative alle biblioteche.
"""


class BibliotecaDAO:
    def __init__(self):
        pass

    @classmethod
    def get_all_biblioteche(cls) -> list[Biblioteca]:
        """
        Recupera tutte le biblioteche dal database.
        Restituisce una lista di oggetti Biblioteca (DTO).
        """
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Errore: Impossibile connettersi al database.")
            return []

        result = []
        # Cursore impostato su dictionary=True e buffered=True per evitare "Unread result found"
        cursor = cnx.cursor(dictionary=True, buffered=True)
        query = "SELECT * FROM biblioteca ORDER BY nome"

        try:
            # L'istruzione corretta per lanciare la query è .execute()
            cursor.execute(query)
            for row in cursor:
                result.append(Biblioteca(row["id"], row["nome"], row["indirizzo"]))
        except Exception as e:
            print(f"Errore durante la query get_all_biblioteche: {e}")
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

        return result