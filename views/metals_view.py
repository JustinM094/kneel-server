import sqlite3
import json


def list_metals(url):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m    
        """)
        query_results = db_cursor.fetchall()

        metals = []
        for row in query_results:
            metals.append(dict(row))

        serialized_metals = json.dumps(metals)
    return serialized_metals


def retrieve_metal(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m
        WHERE m.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()
        dictionary_version_of_object = dict(query_results)
        serialized_metal = json.dumps(dictionary_version_of_object)
    return serialized_metal


def create_metal(request_body):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Metals Values (null, ?, ?)
        """, (request_body["metal"], request_body["price"]))
        single_metal = db_cursor.fetchone()
        serialized_metal = json.dumps(single_metal)
    return serialized_metal


def update_metal(id, metal_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Metals
            SET
                metal = ?,
                price = ?
            WHERE id = ?
            """,
                          (metal_data['metal'], metal_data['price'], id)
                          )
    return True if db_cursor.rowcount > 0 else False


def delete_metal(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Metals WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
