def query_ctgr_list():
    return """
    SELECT * FROM categories WHERE active = TRUE
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


def query_deactivate_prm():
    return """
    UPDATE promotions SET active = 0 WHERE target_category_id = %s
    """

def query_deactivate_p():
    return """
    UPDATE products SET is_active = 0 WHERE category_id = %s
    """

def query_deactivate_c():
    return """
    UPDATE categories SET active = 0 WHERE parent_id=%s or category_id = %s
    """

