import db

def add_position(user_id, stock_name, ex_dividend_date, record_date, payment_date, description):
    sql = """INSERT INTO positions (user_id, stock_name, 
             ex_dividend_date, record_date, 
             payment_date, description) VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [user_id, stock_name, ex_dividend_date, record_date, payment_date, description])

def get_positions():
    sql = "SELECT id, stock_name FROM positions ORDER BY id DESC"
    return db.query(sql)

def get_position(position_id):
    sql = """
        SELECT
            positions.stock_name,
            positions.ex_dividend_date,
            positions.record_date,
            positions.payment_date,
            positions.description,
            users.username
        FROM positions
        JOIN users ON positions.user_id = users.id
        WHERE positions.id = ?
    """
    return db.query(sql, [position_id])[0]