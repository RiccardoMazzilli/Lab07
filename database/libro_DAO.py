from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""


class LibroDAO:
    def __init__(self):
        pass

    @classmethod
    def get_all_generi(cls) -> list[str]:
        """
        Recupera tutti i generi letterari distinti presenti nel database
        per popolare la combobox dei generi.
        """
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Errore: Impossibile connettersi al database.")
            return []

        result = []
        cursor = cnx.cursor(dictionary=True, buffered=True)
        query = "SELECT DISTINCT genere FROM libro WHERE genere IS NOT NULL ORDER BY genere"

        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row["genere"])
        except Exception as e:
            print(f"Errore durante la query get_all_generi: {e}")
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

        return result

    @classmethod
    def get_libri_filtrati(cls, id_biblioteca: int = None, genere: str = None) -> list[Libro]:
        """
        Recupera i libri in base alla biblioteca e/o al genere.
        """
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Errore: Impossibile connettersi al database.")
            return []

        result = []
        cursor = cnx.cursor(dictionary=True, buffered=True)

        # Utilizzo della funzione SQL COALESCE() come suggerito per gestire le selezioni "Nessun filtro"[cite: 3]
        query = """
            SELECT * FROM libro 
            WHERE id_biblioteca = COALESCE(%s, id_biblioteca)
            AND genere = COALESCE(%s, genere)
            ORDER BY titolo
        """

        try:
            cursor.execute(query, (id_biblioteca, genere))
            for row in cursor:
                result.append(Libro(
                    row["id"],
                    row["titolo"],
                    row["autore"],
                    row["genere"],
                    row["anno_pubblicazione"],
                    row["id_biblioteca"]
                ))
        except Exception as e:
            print(f"Errore durante la query get_libri_filtrati: {e}")
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

        return result