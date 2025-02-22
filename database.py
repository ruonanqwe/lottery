import sqlite3
import random

def get_db():
    db = sqlite3.connect('lottery.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    cursor = db.cursor()
    
    # 首先创建数字表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS numbers (
        number INTEGER PRIMARY KEY,
        is_drawn BOOLEAN DEFAULT 0,
        drawn_at DATETIME,
        drawn_by_ip TEXT
    )
    ''')
    
    # 创建IP记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ip_records (
        ip TEXT PRIMARY KEY,
        drawn_at DATETIME
    )
    ''')
    
    # 检查是否需要初始化数字
    cursor.execute('SELECT COUNT(*) FROM numbers')
    if cursor.fetchone()[0] == 0:
        # 生成300个6位数
        numbers = random.sample(range(100000, 999999), 300)
        cursor.executemany(
            'INSERT INTO numbers (number) VALUES (?)',
            [(n,) for n in numbers]
        )
        db.commit()
    
    db.close() 