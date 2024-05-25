from flask import Blueprint, flash,request, redirect, url_for, jsonify,render_template,session
from cursor import getCursor

promotion_page = Blueprint("promotion_page", __name__, static_folder="static", template_folder="templates/promotion")

@promotion_page.route("/promotions")
def get_promotions():
    try:
        promotions_list = []
        connection = getCursor()
        sql_query = """
        SELECT 
            p.promotion_id, 
            p.description, 
            p.promotion_type, 
            p.threshold_value, 
            p.discount_value, 
            c.name as category_name, 
            pr.name as product_name 
        FROM promotions p
        LEFT JOIN categories c ON p.target_category_id = c.category_id
        LEFT JOIN products pr ON p.target_product_id = pr.product_id
        """
        connection.execute(sql_query)
        for promotion in connection.fetchall():
            promotions_list.append({
                "promotion_id": promotion[0],
                "description": promotion[1],
                "promotion_type": promotion[2],
                "threshold_value": promotion[3],
                "discount_value": promotion[4],
                "category_name": promotion[5],
                "product_name": promotion[6]
            })
        connection.close()
        return render_template("promotion_management.html", promotions_list=promotions_list)
    except Exception as e:
        print("Error in promotions:", e)
        return render_template("promotion_management.html", error_msg="An error occurred while fetching promotions.")
    

@promotion_page.route("/add", methods=["GET", "POST"])
def add_promotion():
    try:
        connection = getCursor()
        if request.method == "POST":
            description = request.form["description"]
            promotion_type = request.form["promotion_type"]
            
            # Handle empty values for numeric fields
            threshold_value = request.form["threshold_value"]
            if threshold_value == "":
                threshold_value = None
                
            discount_value = request.form["discount_value"]
            if discount_value == "":
                discount_value = None

            target_category_id = request.form.get("target_category_id", None)
            if target_category_id == "":
                target_category_id = None
                
            target_product_id = request.form.get("target_product_id", None)
            if target_product_id == "":
                target_product_id = None
            all_products = request.form.get("all_products", None)

            if all_products == "on":
                target_category_id = None
                target_product_id = None

            sql_query = """
            INSERT INTO promotions (description, promotion_type, threshold_value, discount_value, target_category_id, target_product_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            connection.execute(sql_query, (description, promotion_type, threshold_value, discount_value, target_category_id, target_product_id))
            connection.close()

            flash("Promotion added successfully", "success")
            return redirect(url_for("promotion_page.get_promotions"))

        sql_categories = "SELECT category_id, name FROM categories"
        sql_products = "SELECT product_id, name FROM products"

        connection.execute(sql_categories)
        categories = connection.fetchall()

        connection.execute(sql_products)
        products = connection.fetchall()

        connection.close()
        return render_template("add_promotion.html", categories=categories, products=products)
    except Exception as e:
        print("Error in add_promotion:", e)
        return render_template("add_promotion.html", error_msg="An error occurred while adding promotion.")
    

@promotion_page.route("/edit/<int:promotion_id>", methods=["GET", "POST"])
def edit_promotion(promotion_id):
    try:
        connection = getCursor()
        if request.method == "POST":
            description = request.form["description"]
            promotion_type = request.form["promotion_type"]
            
            threshold_value = request.form["threshold_value"]
            if threshold_value == "":
                threshold_value = None
                
            discount_value = request.form["discount_value"]
            if discount_value == "":
                discount_value = None

            target_category_id = request.form.get("target_category_id", None)
            if target_category_id == "":
                target_category_id = None
                
            target_product_id = request.form.get("target_product_id", None)
            if target_product_id == "":
                target_product_id = None

            all_products = request.form.get("all_products", None)
            if all_products == "on":
                target_category_id = None
                target_product_id = None

            sql_query = """
            UPDATE promotions
            SET description = %s, promotion_type = %s, threshold_value = %s, discount_value = %s, target_category_id = %s, target_product_id = %s
            WHERE promotion_id = %s
            """
            connection.execute(sql_query, (description, promotion_type, threshold_value, discount_value, target_category_id, target_product_id, promotion_id))
            connection.close()

            flash("Promotion updated successfully", "success")
            return redirect(url_for("promotion_page.get_promotions"))

        sql_promotion = "SELECT * FROM promotions WHERE promotion_id = %s"
        connection.execute(sql_promotion, (promotion_id,))
        promotion = connection.fetchone()
        fetched_promotion = {
                "promotion_id": promotion[0],
                "description": promotion[1],
                "promotion_type": promotion[2],
                "threshold_value": promotion[3],
                "discount_value": promotion[4],
                "target_category_id": promotion[5],
                "target_product_id": promotion[6]
            }

        sql_categories = "SELECT category_id, name FROM categories"
        sql_products = "SELECT product_id, name FROM products"

        connection.execute(sql_categories)
        categories = connection.fetchall()

        connection.execute(sql_products)
        products = connection.fetchall()

        connection.close()
        return render_template("edit_promotion.html", promotion=fetched_promotion, categories=categories, products=products)
    except Exception as e:
        print("Error in edit_promotion:", e)
        return render_template("edit_promotion.html", error_msg="An error occurred while editing promotion.")
