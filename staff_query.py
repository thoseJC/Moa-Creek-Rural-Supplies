def order_list_query():
    return """
                SELECT 
                o.*,
                u.first_name, 
                u.last_name 
                FROM 
                orders o
                JOIN 
                users u ON o.user_id = u.user_id
                WHERE
                o.order_date = query_date
                ORDER BY o.order_date DESC 
                """


def order_list_without_date_query():
    return """
   SELECT 
        o.*,
        u.first_name, 
        u.last_name, 
        u.email
        FROM 
        orders o
        JOIN 
        users u ON o.user_id = u.user_id
        ORDER BY o.order_date DESC 
        """


def update_order_status_query():
    return """
    UPDATE orders SET status = %s 
    WHERE 
    orders.order_id = %s
    """
