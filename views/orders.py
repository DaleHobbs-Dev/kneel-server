"""Module for handling order-related operations"""

import sqlite3
import json


def retrieve_order(order_url):
    pk = order_url["pk"]

    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if "_expand" in order_url["query_params"]:
            db_cursor.execute(
                """
                    SELECT
                        o.id,
                        o.metalId,
                        o.sizeId,
                        o.styleId,
                        o.customerId,
                        c.id customerId,
                        c.name customerName,
                        c.email customerEmail,
                        c.address customerAddress,
                        m.id metalId,
                        m.metal metalType,
                        m.price metalPrice,
                        s.id sizeId,
                        s.carets sizeCarets,
                        s.price sizePrice,
                        st.id styleId,
                        st.name styleType,
                        st.price stylePrice
                    FROM Orders o
                    JOIN Customers c
                        ON c.id = o.customerId
                    JOIN Metals m
                        ON m.id = o.metalId
                    JOIN Sizes s
                        ON s.id = o.sizeId
                    JOIN Styles st
                        ON st.id = o.styleId
                    WHERE o.id = ?
                """,
                (pk,),
            )

            row = db_cursor.fetchone()
            customer = {
                "id": row["customerId"],
                "name": row["customerName"],
                "email": row["customerEmail"],
                "address": row["customerAddress"],
            }
            metal = {
                "id": row["metalId"],
                "metal": row["metalType"],
                "price": row["metalPrice"],
            }
            size = {
                "id": row["sizeId"],
                "carets": row["sizeCarets"],
                "price": row["sizePrice"],
            }
            style = {
                "id": row["styleId"],
                "name": row["styleType"],
                "price": row["stylePrice"],
            }
            order = {
                "id": row["id"],
                "metalId": row["metalId"],
                "sizeId": row["sizeId"],
                "styleId": row["styleId"],
                "customerId": row["customerId"],
                "metal": metal,
                "size": size,
                "style": style,
                "customer": customer,
            }

        else:
            db_cursor.execute(
                """
            SELECT
                o.id,
                o.metalId,
                o.sizeId,
                o.styleId,
                o.customerId
            FROM Orders o
            WHERE o.id = ?
            """,
                (pk,),
            )
            row = db_cursor.fetchone()

            order = dict(row)

        # Serialize Python list to JSON encoded string
        serialized_order = json.dumps(order)

    return serialized_order


def list_orders(url):
    """Function to list all orders, with optional expansion of related hauler data"""
    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if "_expand" in url["query_params"]:
            db_cursor.execute(
                """
                    SELECT
                        s.id,
                        s.name,
                        s.hauler_id,
                        h.id haulerId,
                        h.name haulerName,
                        h.dock_id
                    FROM Ship s
                    JOIN Hauler h
                        ON h.id = s.hauler_id
                """
            )

            query_results = db_cursor.fetchall()

            # Build ships WITH expanded hauler data
            ships = []
            for row in query_results:
                hauler = {
                    "id": row["haulerId"],
                    "name": row["haulerName"],
                    "dock_id": row["dock_id"],
                }
                ship = {
                    "id": row["id"],
                    "name": row["name"],
                    "hauler_id": row["hauler_id"],
                    "hauler": hauler,
                }
                ships.append(ship)

        else:
            db_cursor.execute(
                """
            SELECT
                s.id,
                s.name,
                s.hauler_id
            FROM Ship s
            """
            )

            query_results = db_cursor.fetchall()

            # Build ships WITHOUT expanded hauler data
            ships = []
            for row in query_results:
                ships.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_ships = json.dumps(ships)

    return serialized_ships
