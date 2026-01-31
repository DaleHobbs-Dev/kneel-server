"""Module for handling order-related operations"""

import sqlite3
import json

from .helpers import build_expanded_query, build_order_object, validate_expand_params


def update_order(order_id, order_data):
    """Function to update an order by its primary key (id)"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Orders
            SET metalId = ?, sizeId = ?, styleId = ?, customerId = ?
            WHERE id = ?
            """,
            (
                order_data["metalId"],
                order_data["sizeId"],
                order_data["styleId"],
                order_data["customerId"],
                order_id,
            ),
        )

    return db_cursor.rowcount > 0  # Returns True if a row was updated


def retrieve_order(order_url):
    """Function to retrieve a single order by its primary key (id)"""
    pk = order_url["pk"]

    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if "_expand" in order_url["query_params"]:
            # Get the expand parameter list (could be single or multiple)
            expand_param = order_url["query_params"]["_expand"]

            # Handle if it's a single value or a list
            # isinstance method checks data type
            if isinstance(expand_param, list):
                expand_values = expand_param
            else:
                # Could also support comma-separated: "metal,customer"
                expand_values = (
                    expand_param.split(",") if "," in expand_param else [expand_param]
                )

            # Validate all expand values
            valid_expands = ["metal", "size", "style", "customer"]
            is_valid, result = validate_expand_params(expand_param, valid_expands)
            if not is_valid:
                return json.dumps(result)

            expand_values = result

            # Build the SQL query dynamically based on what's requested
            query = build_expanded_query(expand_values, "orders", include_where=True)

            db_cursor.execute(query, (pk,))
            row = db_cursor.fetchone()

            order = build_order_object(row, expand_values)

        # If no expansions requested, retrieve basic order info
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

            order = build_order_object(row, [])

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
            # Get the expand parameter list (could be single or multiple)
            expand_param = url["query_params"]["_expand"]

            # Handle if it's a single value or a list
            if isinstance(expand_param, list):
                expand_values = expand_param
            else:
                expand_values = (
                    expand_param.split(",") if "," in expand_param else [expand_param]
                )

            # Validate all expand values
            valid_expands = ["metal", "size", "style", "customer"]
            is_valid, result = validate_expand_params(expand_param, valid_expands)
            if not is_valid:
                return json.dumps(result)

            # Build the SQL query dynamically based on what's requested
            query = build_expanded_query(expand_values, "orders")

            db_cursor.execute(query)
            query_results = db_cursor.fetchall()

            # Build orders WITH expanded data
            orders = [build_order_object(row, expand_values) for row in query_results]

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
            """
            )

            query_results = db_cursor.fetchall()

            # Build orders WITHOUT expanded customer data
            orders = [build_order_object(row, []) for row in query_results]

        # Serialize Python list to JSON encoded string
        serialized_orders = json.dumps(orders)

    return serialized_orders


def create_order(new_order):
    """Function to create a new order in the database"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Orders
            (metalId, sizeId, styleId, customerId)
        VALUES
            (?, ?, ?, ?);
        """,
            (
                new_order["metalId"],
                new_order["sizeId"],
                new_order["styleId"],
                new_order["customerId"],
            ),
        )

        # The lastrowid property on the cursor will return the primary key of
        # the last thing that got added to the database
        new_id = db_cursor.lastrowid

        # Add the `id` property to the order dictionary that was sent by the client
        # So that the client sees the primary key in the response
        new_order["id"] = new_id

    return json.dumps(new_order)


def delete_order(order_id):
    """Function to delete an order by its primary key (id)"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM Orders
        WHERE id = ?
        """,
            (order_id,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
