"""Helpers for building dynamic SQL queries"""


def validate_expand_params(expand_param, valid_expands=None):
    """
    Validate and parse expand parameters

    Args:
        expand_param: string or list of expand values from query params
        valid_expands: list of valid expand options (defaults to order expansions)

    Returns:
        tuple: (is_valid, expand_values or error_dict)
    """
    if valid_expands is None:
        valid_expands = ["metal", "size", "style", "customer"]

    # Parse expand parameter
    if isinstance(expand_param, list):
        expand_values = expand_param
    else:
        expand_values = (
            expand_param.split(",") if "," in expand_param else [expand_param]
        )

    # Validate
    for val in expand_values:
        if val not in valid_expands:
            error_response = {
                "error": f"Invalid expand parameter: {val}",
                "valid_options": valid_expands,
            }
            return False, error_response

    return True, expand_values


def build_order_object(row, expand_values):
    """
    Build an order dictionary from a database row with optional expansions

    Args:
        row: sqlite3.Row object from database query
        expand_values: list of strings indicating which related data to include

    Returns:
        Dictionary representing the order with requested expansions
    """
    order = {
        "id": row["id"],
        "metalId": row["metalId"],
        "sizeId": row["sizeId"],
        "styleId": row["styleId"],
        "customerId": row["customerId"],
    }

    if "metal" in expand_values:
        order["metal"] = {
            "id": row["metalId"],
            "metal": row["metalType"],
            "price": row["metalPrice"],
        }

    if "size" in expand_values:
        order["size"] = {
            "id": row["sizeId"],
            "carets": row["sizeCarets"],
            "price": row["sizePrice"],
        }

    if "style" in expand_values:
        order["style"] = {
            "id": row["styleId"],
            "name": row["styleType"],
            "price": row["stylePrice"],
        }

    if "customer" in expand_values:
        order["customer"] = {
            "id": row["customerId"],
            "name": row["customerName"],
            "email": row["customerEmail"],
            "address": row["customerAddress"],
        }

    return order


def build_expanded_query(expand_values, base_query, include_where=False):
    """
    Helper to build dynamic SQL with joins

    Args:
        expand_values: list of strings showing which tables to expand (e.g., ['metal', 'customer'])
        base_query: string indicating the base resource type ('orders', 'metals', 'customers', etc.)
        include_where: boolean to include WHERE clause for single record retrieval

    Returns:
        Complete SQL query string with dynamic joins based on expand values
    """

    # Determine the base table and alias based on base_query
    if base_query == "orders" or base_query == "order":
        base_table = "Orders o"
        select_fields = """
        o.id,
        o.metalId,
        o.sizeId,
        o.styleId,
        o.customerId
        """
        where_clause = "WHERE o.id = ?" if include_where else ""

    elif base_query == "metals" or base_query == "metal":
        base_table = "Metals m"
        select_fields = """
        m.id,
        m.metal,
        m.price
        """
        where_clause = "WHERE m.id = ?" if include_where else ""

    elif base_query == "customers" or base_query == "customer":
        base_table = "Customers c"
        select_fields = """
        c.id,
        c.name,
        c.email,
        c.address
        """
        where_clause = "WHERE c.id = ?" if include_where else ""

    elif base_query == "sizes" or base_query == "size":
        base_table = "Sizes s"
        select_fields = """
        s.id,
        s.carets,
        s.price
        """
        where_clause = "WHERE s.id = ?" if include_where else ""

    elif base_query == "styles" or base_query == "style":
        base_table = "Styles st"
        select_fields = """
        st.id,
        st.name,
        st.price
        """
        where_clause = "WHERE st.id = ?" if include_where else ""

    else:
        # Default to orders if unrecognized
        base_table = "Orders o"
        select_fields = """
        o.id,
        o.metalId,
        o.sizeId,
        o.styleId,
        o.customerId
        """
        where_clause = "WHERE o.id = ?" if include_where else ""

    joins = ""

    # Only add joins if we're querying orders (since orders have foreign keys)
    if base_query in ["orders", "order"]:
        if "metal" in expand_values:
            select_fields += """,
                    m.id metalId,
                    m.metal metalType,
                    m.price metalPrice"""
            joins += """
                    JOIN Metals m
                    ON m.id = o.metalId"""

        if "size" in expand_values:
            select_fields += """,
                    s.id sizeId,
                    s.carets sizeCarets,
                    s.price sizePrice"""
            joins += """
                    JOIN Sizes s
                    ON s.id = o.sizeId"""

        if "style" in expand_values:
            select_fields += """,
                    st.id styleId,
                    st.name styleType,
                    st.price stylePrice"""
            joins += """
                    JOIN Styles st
                    ON st.id = o.styleId"""

        if "customer" in expand_values:
            select_fields += """,
                    c.id customerId,
                    c.name customerName,
                    c.email customerEmail,
                    c.address customerAddress"""
            joins += """
                    JOIN Customers c
                    ON c.id = o.customerId"""

    # Build and return the complete query
    return f"""
            SELECT
            {select_fields}
            FROM {base_table}
            {joins}
            {where_clause}
            """
