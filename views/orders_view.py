import sqlite3
import json


def list_orders(url):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id
        FROM Orders o
        """)
        query_results = db_cursor.fetchall()

        orders = []
        for row in query_results:
            orders.append(dict(row))

        serialized_orders = json.dumps(orders)
    return serialized_orders


def retrieve_order(url):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if url["query_params"] == {"_expand": ['metal']}:
            db_cursor.execute("""
                SELECT
                    o.id,
                    o.metal_id,
                    o.size_id,
                    o.style_id,
                    m.id metalId,
                    m.metal,
                    m.price
                FROM Orders o
                JOIN Metals m
                    ON m.id = o.metal_id
                WHERE o.id = ?
                """, (url["pk"],))
            query_results = db_cursor.fetchone()

            metal = {
                "id": query_results['metalId'],
                "metal": query_results['metal'],
                "price": query_results["price"]
            }
            order = {
                "id": query_results['id'],
                "metal_id": query_results['metal_id'],
                "size_id": query_results["size_id"],
                "style_id": query_results["style_id"],
                "metal": metal
            }
            serialized_order = json.dumps(order)

        elif url["query_params"] == {"_expand": ['size']}:
            db_cursor.execute("""
                SELECT
                    o.id,
                    o.metal_id,
                    o.size_id,
                    o.style_id,
                    s.id sizeId,
                    s.carets,
                    s.price
                FROM Orders o
                JOIN Sizes s
                    ON s.id = o.size_id
                WHERE o.id = ?
                """, (url["pk"],))
            query_results = db_cursor.fetchone()

            size = {
                "id": query_results['sizeId'],
                "carets": query_results['carets'],
                "price": query_results["price"]
            }
            order = {
                "id": query_results['id'],
                "metal_id": query_results['metal_id'],
                "size_id": query_results["size_id"],
                "style_id": query_results["style_id"],
                "size": size
            }
            serialized_order = json.dumps(order)

        elif url["query_params"] == {"_expand": ['style']}:
            db_cursor.execute("""
                SELECT
                    o.id,
                    o.metal_id,
                    o.size_id,
                    o.style_id,
                    s.id styleId,
                    s.style,
                    s.price
                FROM Orders o
                JOIN Styles s
                    ON s.id = o.style_id
                WHERE o.id = ?
                """, (url["pk"],))
            query_results = db_cursor.fetchone()

            style = {
                "id": query_results['styleId'],
                "style": query_results['style'],
                "price": query_results["price"]
            }
            order = {
                "id": query_results['id'],
                "metal_id": query_results['metal_id'],
                "size_id": query_results["size_id"],
                "style_id": query_results["style_id"],
                "style": style
            }
            serialized_order = json.dumps(order)

        else:
            db_cursor.execute("""
            SELECT
                o.id,
                o.metal_id,
                o.size_id,
                o.style_id
            FROM Orders o
            WHERE o.id = ?
            """, (url["pk"],))
            query_results = db_cursor.fetchone()

            dictionary_version_of_object = dict(query_results)
            serialized_order = json.dumps(dictionary_version_of_object)

    return serialized_order


def create_order(request_body):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Orders (metal_id, size_id, style_id) VALUES (?, ?, ?)
        """, (request_body["metal_id"], request_body["size_id"], request_body["style_id"]))
        conn.commit()
    return True


def update_order(id, order_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Orders
            SET
                metal_id = ?,
                size_id = ?,
                style_id = ?
            WHERE id = ?
            """,
                          (order_data['metal_id'], order_data['size_id'],
                           order_data['style_id'], id)
                          )
        conn.commit()
    return True if db_cursor.rowcount > 0 else False


def delete_order(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to delete the order
        db_cursor.execute("""
        DELETE FROM Orders WHERE id = ?
        """, (pk,))
        conn.commit()
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
