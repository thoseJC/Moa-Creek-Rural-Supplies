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

def get_all_products_with_inventory():
    return """
        SELECT 
            p.product_id,
            p.name,
            p.is_active,
            i.inventory_id,
            i.quantity
        FROM 
            products p
        INNER JOIN 
            inventory i ON p.product_id = i.product_id;
    """

def get_product_with_inventory():
    return """
        SELECT 
            p.name,
            p.description,
            p.price,
            p.pd_image_path,
            p.is_active,
            i.inventory_id,
            i.quantity
        FROM 
            products p
        INNER JOIN 
            inventory i ON p.product_id = i.product_id
        WHERE 
            p.product_id=%s;
    """