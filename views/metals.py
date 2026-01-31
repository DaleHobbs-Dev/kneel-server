"""Module for handling metal-related operations"""

import json
import sqlite3


def retrieve_metal(url):
    """Function to retrieve a single metal by its primary key (id)"""

    metal_id = url["pk"]

    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                id,
                metal,
                price
            FROM Metals
            WHERE id = ?
            """,
            (metal_id,),
        )

        row = db_cursor.fetchone()

        if row:
            metal = {
                "id": row["id"],
                "metal": row["metal"],
                "price": row["price"],
            }
        else:
            metal = None

        serialize_metal = json.dumps(metal)

    return serialize_metal


def list_metals():
    """Function to list all metals"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                id,
                metal,
                price
            FROM Metals
            """
        )

        metals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            metal = {
                "id": row["id"],
                "metal": row["metal"],
                "price": row["price"],
            }
            metals.append(metal)

        serialize_metals = json.dumps(metals)

    return serialize_metals


def update_metal(metal_id, metal_data):
    """Function to update a metal by its primary key (id)"""
    try:
        with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                UPDATE Metals
                SET metal = ?, price = ?
                WHERE id = ?
                """,
                (metal_data["metal"], metal_data["price"], metal_id),
            )
            rows_affected = db_cursor.rowcount
            conn.commit()  # Explicitly commit the transaction

            return rows_affected > 0  # Returns True if a row was updated

    except KeyError as e:
        # Missing required field in metal_data
        print(f"Missing required field: {e}")
        return False
    except sqlite3.Error as e:
        # Database error
        print(f"Database error: {e}")
        return False
