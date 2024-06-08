def query_ctgr_list():
    return """
    SELECT * FROM categories
    """
def query_add():
    return """
    INSERT INTO categories (name, description) VALUES (%s, %s)
    """


def query_edit():
    return """
    UPDATE categories SET name = %s, description = %s 
    WHERE category_id = %s
	"""


def query_delete_prm():
    return """
    DELETE FROM promotions WHERE target_category_id = %s
    """


def query_delete_p():
    return """
    DELETE FROM products WHERE category_id = %s
    """


def query_delete_c():
    return """
    DELETE FROM categories WHERE category_id = %s
    """
