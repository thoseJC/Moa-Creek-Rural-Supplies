from flask import Blueprint, flash,request, redirect, url_for, jsonify, render_template, session
from datetime import datetime
from cursor import getCursor


news_page = Blueprint("news_page", __name__, static_folder="static", template_folder="templates/news")

# SQL query to fetch the list of news
def query_news_list():
    return """
    SELECT n.news_id, n.title, n.content, u.username, n.is_published, n.published_date
    FROM news n
    JOIN users u 
    ON n.created_by = u.user_id
    ORDER BY published_date DESC
    """

# SQL query to insert a new news article
def insert_news():
    return """
    INSERT INTO news (title, content, created_by, is_published, published_date)
    VALUES (%s, %s, %s, %s, %s)
    """

def get_logged_user():
    if not session.get('user_id'):
        flash('You need to login to add an address.', 'warning')
        return redirect(url_for('login_page.login'))
    else:
        return session['user_id']

@news_page.route('/news-management')
def get_news():
    try:
        news_list = []
        cursor = getCursor()
        sql_query = query_news_list()
        cursor.execute(sql_query)
        for news in cursor:
            news_list.append({
                "news_id": news[0],
                "title": news[1],
                "content": news[2],
                "created_by": news[3],
                "is_published": news[4],
                "published_date": news[5]
            })
        cursor.close()
        
        return render_template('news_management.html', news_list=news_list)
    except Exception as e:
        print("Error in news_management:", e)
        return render_template('news_management.html', error_msg="An error occurred while fetching news.")
    

@news_page.route('/add', methods=['GET', 'POST'])
def add_news():
    if not session.get('user_id'):
        flash('You need to login to add an address.', 'warning')
        return redirect(url_for('login_page.login'))
    else:
        user_id = session['user_id']
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        created_by = user_id 
        is_published = 'is_published' in request.form
        published_date = datetime.now() if is_published else None
        
        try:
            cursor = getCursor()
            sql_query = insert_news()
            cursor.execute(sql_query,(title, content, created_by, is_published, published_date))
            flash('news has been added successfully')
            return redirect(url_for('news_page.get_news'))
        except Exception as e:
            print("Error in add_news:", e)
            flash('failed to add news','error')
            return render_template('news/add_news.html', error=str(e))
    return render_template('add_news.html')


@news_page.route('/edit/<int:news_id>', methods=['GET', 'POST'])
def edit_news(news_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        is_published = 'is_published' in request.form
        published_date = datetime.now() if is_published else None

        try:
            cursor = getCursor()
            # Update the news with the new data
            if is_published:
                sql_query = """
                UPDATE news
                SET title = %s, content = %s, is_published = %s, published_date = %s
                WHERE news_id = %s
                """
                cursor.execute(sql_query, (title, content, is_published, published_date, news_id))
            else:
                sql_query = """
                UPDATE news
                SET title = %s, content = %s, is_published = %s, published_date = NULL
                WHERE news_id = %s
                """
                cursor.execute(sql_query, (title, content, is_published, news_id))
            return redirect(url_for('news_page.get_news'))
        except Exception as e:
            print("Error in edit_news:", e)
            return redirect(url_for('news_page.get_news'))
    else:
        try:
            cursor = getCursor()
            sql_query = "SELECT title, content, is_published FROM news WHERE news_id = %s"
            cursor.execute(sql_query, (news_id,))
            news = cursor.fetchone()
            cursor.close()

            if news:
                return render_template('edit_news.html', news_id=news_id, title=news[0], content=news[1], is_published=news[2])
            else:
                return render_template('edit_news.html', error_msg="News not found.", news_id=news_id)
        except Exception as e:
            print("Error in edit_news:", e)
            return render_template('edit_news.html', error_msg="An error occurred while fetching the news.", news_id=news_id)
