import db

def list_comments(db, position_id):
    sql = """ SELECT c.id,
                c.content,
                c.user_id,
                u.username
                    FROM comments c
                    JOIN users u ON u.id = c.user_id
                    WHERE c.position_id = ?
                    ORDER BY c.id DESC """
    return db.query(sql, [position_id])

def get_all_classes():
    sql = "SELECT type, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for type, value in result:
        if type not in classes:
            classes[type] = []
        classes[type].append(value)

    return classes

def add_position(user_id, stock_name, ex_dividend_date, record_date, payment_date, description, classes):
    sql = """INSERT INTO positions (user_id, stock_name, ex_dividend_date, record_date, payment_date, description) 
                VALUES (?, ?, ?, ?, ?, ?)"""
    position_id = db.execute(sql, [user_id, stock_name, ex_dividend_date, record_date, payment_date, description])
    
    for type, value in classes:
        sql = "INSERT INTO position_classes (position_id, type, value) VALUES (?, ?, ?)"
        db.execute(sql, [position_id, type, value])

def get_positions():
    sql = """SELECT positions.id, positions.stock_name, positions.ex_dividend_date, users.username, users.id AS user_id
                FROM positions
                JOIN users ON positions.user_id = users.id
                ORDER BY positions.id DESC"""
    return db.query(sql)

def get_classes(position_id):
    sql = "SELECT type, value FROM position_classes WHERE position_id = ?"
    return db.query(sql, [position_id])

def get_position(position_id):
    sql = """ SELECT positions.id, positions.stock_name, positions.ex_dividend_date, 
                    positions.record_date, positions.payment_date,
                    positions.description,
                    users.id AS user_id,
                    users.username
                FROM positions
                JOIN users ON positions.user_id = users.id
                WHERE positions.id = ?"""
    return db.query(sql, [position_id])[0]

def update_position(position_id, stock_name, ex_dividend_date, record_date, payment_date, description, classes):
    sql = """UPDATE positions SET stock_name = ?,
                ex_dividend_date = ?,
                record_date = ?,
                payment_date = ?,
                description = ?
                WHERE id = ? """
    db.execute(sql, [stock_name, ex_dividend_date, record_date, payment_date, description, position_id])
    db.execute("DELETE FROM position_classes WHERE position_id = ?",[position_id])
    for type, value in classes:
        db.execute(
            "INSERT INTO position_classes (position_id, type, value) VALUES (?, ?, ?)",
            [position_id, type, value])

def delete_position(position_id):
    db.execute("DELETE FROM comments WHERE position_id = ?", [position_id])
    db.execute("DELETE FROM position_classes WHERE position_id = ?", [position_id])
    db.execute("DELETE FROM positions WHERE id = ?", [position_id])

def find_positions(query):
    sql = """ SELECT id, stock_name FROM positions 
                WHERE stock_name LIKE ? or description LIKE ?
                ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def get_comment(comment_id):
    sql = "SELECT * FROM comments WHERE id = ?"
    return db.query(sql, [comment_id])[0]


def add_comment(position_id, user_id, content):
    sql = " INSERT INTO comments (position_id, user_id, content) VALUES (?, ?, ?)"
    db.execute(sql, [position_id, user_id, content])

def update_comment(comment_id, content):
    sql = "UPDATE comments SET content = ? WHERE id = ?"
    db.execute(sql, [content, comment_id])

def delete_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])