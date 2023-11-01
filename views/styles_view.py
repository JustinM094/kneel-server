import sqlite3
import json


def list_styles(url):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.style,
            s.price
        FROM Styles s    
        """)
        query_results = db_cursor.fetchall()

        styles = []
        for row in query_results:
            styles.append(dict(row))

        serialized_styles = json.dumps(styles)
    return serialized_styles


def retrieve_styles(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.carets,
            s.price
        FROM Styles s
        WHERE s.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()
        dictionary_version_of_object = dict(query_results)
        serialized_style = json.dumps(dictionary_version_of_object)
    return serialized_style


def create_styles(request_body):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Styles Values (null, ?, ?)
        """, (request_body["style"], request_body["price"]))
        single_styles = db_cursor.fetchone()
        serialized_styles = json.dumps(single_styles)
    return serialized_styles


def update_styles(id, styles_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Styles
            SET
                style = ?,
                price = ?
            WHERE id = ?
            """,
                          (styles_data['style'], styles_data['price'], id)
                          )
    return True if db_cursor.rowcount > 0 else False


def delete_styles(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Styles WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
