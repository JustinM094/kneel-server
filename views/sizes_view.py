import sqlite3
import json


def list_sizes(url):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.carets,
            s.price
        FROM Sizes s    
        """)
        query_results = db_cursor.fetchall()

        sizes = []
        for row in query_results:
            sizes.append(dict(row))

        serialized_sizes = json.dumps(sizes)
    return serialized_sizes


def retrieve_size(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.carets,
            s.price
        FROM Sizes s
        WHERE s.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()
        dictionary_version_of_object = dict(query_results)
        serialized_size = json.dumps(dictionary_version_of_object)
    return serialized_size


def create_size(request_body):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Sizes Values (null, ?, ?)
        """, (request_body["carets"], request_body["price"]))
        single_size = db_cursor.fetchone()
        serialized_size = json.dumps(single_size)
    return serialized_size


def update_size(id, size_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Sizes
            SET
                carets = ?,
                price = ?
            WHERE id = ?
            """,
                          (size_data['carets'], size_data['price'], id)
                          )
    return True if db_cursor.rowcount > 0 else False


def delete_size(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Sizes WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
