import db

def add_position(user_id, stock_name, ex_dividend_date, record_date, payment_date, description, classes):
    sql = """INSERT INTO positions (user_id, stock_name, 
             ex_dividend_date, record_date, 
             payment_date, description) VALUES (?, ?, ?, ?, ?, ?)"""
    position_id = db.execute(sql, [user_id, stock_name, ex_dividend_date, record_date, payment_date, description])
    
    for field, season in classes:
        sql = "INSERT INTO position_classes (position_id, field, season) VALUES (?, ?, ?)"
        db.execute(sql, [position_id, field, season])

def get_positions():
    sql = "SELECT id, stock_name FROM positions ORDER BY id DESC"
    return db.query(sql)

def get_classes(position_id):
    sql = "SELECT field, season FROM position_classes WHERE position_id = ?"
    return db.query(sql, [position_id])

def get_position(position_id):
    sql = """
        SELECT
            positions.id,
            positions.stock_name,
            positions.ex_dividend_date,
            positions.record_date,
            positions.payment_date,
            positions.description,
            users.id AS user_id,
            users.username
        FROM positions
        JOIN users ON positions.user_id = users.id
        WHERE positions.id = ?
    """
    return db.query(sql, [position_id])[0]

def update_position(position_id, stock_name, ex_dividend_date, record_date, payment_date, description):
    sql = """
        UPDATE positions
        SET stock_name = ?,
            ex_dividend_date = ?,
            record_date = ?,
            payment_date = ?,
            description = ?
        WHERE id = ?
        """
    db.execute(sql, [stock_name, ex_dividend_date, record_date, payment_date, description, position_id])

def delete_position(position_id):
    sql = "DELETE FROM positions WHERE id = ?"
    db.execute(sql, [position_id])

def find_positions(query):
    sql = """
        SELECT id, stock_name FROM positions
        WHERE stock_name LIKE ? or description LIKE ?
        ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])