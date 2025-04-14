import sqlite3 as sq
from werkzeug.security import generate_password_hash, check_password_hash

#This function will create the database and the tables if they do not exist 
def create_database(): 
    con = sq.connect("banking.db") 
    cur = con.cursor() 
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL, 
            pin  INTEGER NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS bank (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            balance REAL NOT NULL DEFAULT 0, 
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')  
    con.commit()
    con.close()


def register(username, pin): 
    con = sq.connect("banking.db")
    cur = con.cursor() 
    #Registers the user into our new users table 
    try:
        hashed_password = generate_password_hash(pin)
        cur.execute("INSERT INTO users (username, pin) VALUES (?, ?)", (username, hashed_password))
        con.commit()
        return {"success": True, "message": "User registered successfully"} 
    except sq.IntegrityError:
        return False
    finally:
        con.close() 

def verify(username, pin): 
    con = sq.connect("banking.db")
    cur = con.cursor() 
    
    try:
        cur.execute("SELECT user_id, pin FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
     
    
        if user and check_password_hash(user[1], pin):
            return user[0]  
        return None 
    finally: 
        con.close()

#This function will check the balance of the user
def check_balance(user_id):
    con = sq.connect("banking.db")
    cur = con.cursor()
    try:
        cur.execute("SELECT balance FROM bank WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        if result:
            return {"success": True, "balance": result[0]}
        return {"success": False, "message": "account not found"}
    finally:
        con.close() 

#This function will deposit money into the user's account   
def deposit(user_id, amount):
    con = sq.connect("banking.db")
    cur = con.cursor()
    try:
        cur.execute("UPDATE bank SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        con.commit()
        return {"success": True, "message": "deposit successful!"}

    finally:
        con.close()

#This function will withdraw money from the user's account
def withdraw(user_id, amount):
    con = sq.connect("banking.db")
    cur = con.cursor()
    try:
        cur.execute("SELECT balance FROM bank WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        if result and result[0] >= amount:
            cur.execute("UPDATE bank SET balance = balance - ? WHERE user_id = ?", (amount, user_id))
            con.commit()
            return {"success": True, "message": "withdrawal successful!"}
        return {"success": False, "message": "insufficient funds :("}
    finally:
        con.close() 

#This function will delete the user's account (if they want to [idk why])
def delete_account(user_id):
    con = sq.connect("banking.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM bank WHERE user_id = ?", (user_id,))
        cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        con.commit()
        return {"success": True, "message": "account deleted successfully"}
    finally:
        con.close()

#This function will allow the user to modify their account
def modify_account(user_id, new_username, new_pin):
    con = sq.connect("banking.db")
    cur = con.cursor()
    try:
        hashed_password = generate_password_hash(new_pin)
        cur.execute("UPDATE users SET username = ?, pin = ? WHERE user_id = ?", (new_username, hashed_password, user_id))
        con.commit()
        return {"success": True, "message": "account modified successfully!"}
    finally:
        con.close()